import customtypes
from decimal import Decimal


def build_base(w, s, n):
    b = [[0 for i in range(n + 1)] for i in range(n + 1)]
    for i in range(n):
        for j in range(n):
            if i == j:
                b[i][j] = 1
        b[i][n] = - w[i]
    b[n][n] = s
    return b


def close_int(q):
    return int(q) if q - int(q) <= 0.5 else int(q) + 1


def scalar(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def vector_sum(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def vector_koef_dec(a, k):
    return [Decimal(a[i] * k) for i in range(len(a))]


def vector_koef(a, k):
    return [a[i] * k for i in range(len(a))]


def norm(a):
    return sum((elem ** 2) ** 0.5 for elem in a)


def norm_step(a):
    return sum(elem ** 2 for elem in a)


def tilde_base(b, n):
    tilde_b = [[0 for i in range(n + 1)] for i in range(n + 1)]
    for i in range(n + 1):
        proection = [0 for i in range(n + 1)]
        for j in range(i):
            k = Decimal(scalar(b[i], tilde_b[j])) / Decimal(scalar(tilde_b[j], tilde_b[j]))
            proection = vector_sum(proection, vector_koef_dec(tilde_b[j], k))
        proection = vector_koef_dec(proection, -1)
        tilde_b[i] = vector_sum(b[i], proection)
    return tilde_b


def reduction(b, tilde_b, n):
    for i in range(1, n):
        for j in range(i - 1, -1, -1):
            k = close_int(Decimal(scalar(b[i], tilde_b[j])) / Decimal(scalar(tilde_b[j], tilde_b[j])))
            b[i] = vector_sum(b[i], vector_koef(b[j], -k))
    return b


def swap(b, tilde_b, n, delta):
    i = 0
    while i < n:
        v_1 = vector_koef_dec(tilde_b[i], Decimal(scalar(b[i + 1], tilde_b[i])) / Decimal(scalar(tilde_b[i], tilde_b[i])))
        v_1 = vector_sum(v_1, tilde_b[i + 1])
        if Decimal(delta) * norm_step(tilde_b[i]) > norm_step(v_1):
            tmp = b[i + 1]
            b[i + 1] = b[i]
            b[i] = tmp
            print(i)
            break
        i += 1
    if i == n:
        return b, False
    return b, True


def lll(b, n):
    delta = 0.75
    tilde_b = tilde_base(b, n)
    flag = True
    while flag:
        b = reduction(b, tilde_b, n + 1)
        print("done reduction")
        b, flag = swap(b, tilde_b, n, delta)
        print("done swap")
    return b[0]


def hack(w, n, c):
    b = build_base(w, c, n)
    max_norm = max(norm(elem) for elem in b)
    d_w = n / max_norm
    if d_w >= 0.646:
        exit("Cannot decrypt: d(W) is too big: {}".format(d_w))
    b_res = lll(b, n)
    print(b_res)
    i = 0
    m = None
    is_0_1 = False
    while i < len(b_res) - 1 and b_res[i] in [0, 1]:
        i += 1
    print(b)
    if i == len(b_res) - 1:
        if b_res[i] == 0:
            is_0_1 = True
    if is_0_1:
        m = 0
        for j in range(len(b) - 1, 0, -1):
            m = m * 2 + b_res[j]
    else:
        print("ANOTHER")
        b = build_base(w, n, sum(elem for elem in w) - c)
        b_res = lll(b, n)
        print(b_res)
        i = 0
        is_0_1 = False
        while i < len(b_res) - 1 and b_res[i] in [0, 1]:
            i += 1
        if i == len(b_res) - 1:
            if b_res[i] == sum(elem for elem in w) - 2 * c:
                is_0_1 = True
        if not is_0_1:
            exit("Unable to find short vector.")
        else:
            m = 0
            for j in range(len(b_res) - 1, 0, -1):
                m = m * 2 + b_res[j]
    return None if m is None else customtypes.type_bytes(m)
