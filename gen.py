import customtypes
import base64
import os
from mh import MH


def gen(n, b):
    cipher = MH(n=n, b=b)
    print(cipher.u, cipher.w, cipher.a, cipher.k)
    with open("./keys/private", 'wb') as f:
        f.write(b'-----BEGIN PRIVATE KEY-----' +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.n)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.k)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.a)) +
                bytes(os.linesep, "ascii")
                )
        for i in range(n):
            f.write(base64.b32encode(customtypes.type_bytes(cipher.u[i])) + bytes(os.linesep, "ascii"))
        f.write(b'-----END PRIVATE KEY-----')
    with open("./keys/public", "wb") as f:
        f.write(b'-----BEGIN PUBLIC KEY-----' +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.n)) +
                bytes(os.linesep, "ascii")
                )
        for i in range(n):
            f.write(base64.b32encode(customtypes.type_bytes(cipher.w[i])) + bytes(os.linesep, "ascii"))
        f.write(b'-----END PUBLIC KEY-----')
    print("Done.")
