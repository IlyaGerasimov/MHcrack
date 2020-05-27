import base64
import os
import customtypes
from mh import MH


def get_public(f):
    # f with "r" mode
    title = f.readline().strip('\n')
    if title != '-----BEGIN PUBLIC KEY-----':
        return None, None
    n = f.readline().strip('\n')
    w = [0] * customtypes.type_int(n, True)
    for i in range(customtypes.type_int(n, True)):
        w[i] = f.readline().strip('\n')
    title = f.readline().strip('\n')
    if title != '-----END PUBLIC KEY-----':
        return None, None
    return MH(n=n, w=w)


def get_private(f):
    # f with "r" mode
    title = f.readline().strip('\n')
    if title != '-----BEGIN PRIVATE KEY-----':
        return "Wrong format."
    n = f.readline().strip('\n')
    k = f.readline().strip('\n')
    a = f.readline().strip('\n')
    u = [0] * customtypes.type_int(n, True)
    for i in range(customtypes.type_int(n, True)):
        u[i] = f.readline().strip('\n')
    title = f.readline().strip('\n')
    if title != '-----END PRIVATE KEY-----':
        return "Wrong format."
    return MH(u=u, a=a, k=k, n=n)


'''def get_test():
    return MH(w=[82, 123, 287, 83, 248, 373, 10, 471], n=8)


print(get_private(open('./keys/private', 'r')).__dict__)'''
