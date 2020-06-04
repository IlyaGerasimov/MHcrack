import customtypes
from lll import hack
from program_config import get_public, get_private


def decrypt_hack(c, file):
    cipher = get_public(file)
    if type(cipher) is str:
        exit(cipher)
    file.close()
    c = customtypes.type_int(c, True)
    m = hack(cipher.w, cipher.n, c)
    print("Found possible m in bytes:", m)
    try:
        print("The result is:", m.decode("utf-8"))
    except UnicodeDecodeError:
        exit("Cannot represent the possible result in UTF-8.")


def decrypt_pure(c, file):
    cipher = get_private(file)
    if type(cipher) is str:
        exit(cipher)
    file.close()
    c = customtypes.type_int(c, True)
    m = cipher.decrypt(c)
    print(m)
    print(customtypes.type_bytes(m).decode('utf-8'))