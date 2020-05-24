import customtypes
from lll import hack
from program_config import get_public


def decrypt_hack(c, file):
    cipher = get_public(file)
    file.close()
    c = customtypes.type_int(c, True)
    m = hack(cipher.w, cipher.n, c)
    print(m)
    print(m.decode("utf-8"))