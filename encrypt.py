import pathlib
import customtypes
import base64
import math
import os
from program_config import get_public


def write_encrypt(c):
    index = sum([len(files) for r, d, files in os.walk("./encrypt")])
    with open("./encrypt/cipher{}".format(index), "wb") as f:
        f.write(base64.b32encode(customtypes.type_bytes(c)))


def encrypt_inter():
    p = input("Please specify path to the public key: ")
    p = pathlib.Path(p)
    while not p.exists():
        p = input("Cannot find such file. Please try again: ")
        p = pathlib.Path(p)
    with p.open('r') as f:
        cipher = get_public(f)
    m = input("Please specify the message: ")
    m = bytes(m, 'utf-8')
    while len(m) * 8 > cipher.n:
        m = input("Sorry, but the message is too long for the cipher. Please specify message again: ")
        m = bytes(m, 'utf-8')
    m = customtypes.type_int(m)
    c = cipher.encrypt(m)
    write_encrypt(c)


def encrypt_cli(file, m):
    cipher = get_public(file)
    file.close()
    m = customtypes.type_int(m)
    if math.log2(m) > cipher.n:
        exit("Too long message for the encryprion.")
    c = cipher.encrypt(m)
    write_encrypt(c)
    print("Done.")
