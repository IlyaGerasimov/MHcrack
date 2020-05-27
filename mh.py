import random
import math
import customtypes


def reverse(a, b):
    n = b
    res = 1
    prev = 0
    i = 0
    while a != 1:
        temp = res
        res = res * (b // a) + prev
        prev = temp
        a_1 = b%a
        b = a
        a = a_1
        i += 1
    return res if i % 2 == 0 else -res+n


def search(u, s, n):
    k = n - 1
    m = [0] * n
    while k >= 0:
        if s >= u[k]:
            m[k] = 1
        else:
            m[k] = 0
        s = s - m[k] * u[k]
        k = k - 1
    if s == 0:
        return m
    return None


class MH:

    def __init__(self, n=None, b=None, u=None, w=None, a=None, k=None):
        if u and a and k and n:
            self.u = u
            sum = 0
            for i in range(len(self.u)):
                self.u[i] = customtypes.type_int(self.u[i], True)
                if self.u[i] < sum:
                    exit('Not "superfast" sequence.')
                sum += self.u[i]
            self.a = customtypes.type_int(a, True)
            self.k = customtypes.type_int(k, True)
            self.n = customtypes.type_int(n, True)
        elif w and n:
            self.w = w
            for i in range(len(self.w)):
                self.w[i] = customtypes.type_int(self.w[i], True)
            self.n = customtypes.type_int(n, True)
        else:
            u = list([(1 << (b - 1)) + random.getrandbits(b - 1)])
            summ = u[0]
            flag = False
            for i in range(n):
                tmp = random.randint(summ + 1, (1 << (b + i)) - 1)
                u.append(tmp)
                summ += tmp
            k = random.randint(summ + 1, (1 << (b + n)) - 1)
            a = random.randint(2, k - 1)
            while math.gcd(a, k) != 1:
                a = random.randint(2, k - 1)
            a_1 = reverse(a, k)
            w = [0] * len(u)
            for i in range(len(u)):
                w[i] = (a_1 * u[i]) % k
            self.u = u
            self.w = w
            self.a = a
            self.k = k
            self.n = n
            self.b = b

    def encrypt(self, m):
        bits = bin(m)[2:]
        if len(bits) > self.n:
            exit("Message does not have required length")
        while len(bits) < self.n:
            bits = '0' + bits
        c = 0
        for i in range(len(bits)):
            c += int(bits[i]) * self.w[i]
        return c

    def decrypt(self, c):
        s = self.a * c % self.k
        m = search(self.u, s, self.n)
        res = 0
        for i in range(len(m)):
            res = 2 * res + m[i]
        return res
