import customtypes
from calc import pow
from fractions import Fraction


def build_base(w, s, n):
    b = [[0 for i in range(n + 1)] for i in range(n + 1)]
    for i in range(n):
        for j in range(n):
            if i == j:
                b[i][j] = 1
        b[i][n] = - w[i]
    b[n][n] = s
    return b


def dot(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def vector_sum(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def vector_koef(a, k):
    return [a[i] * k for i in range(len(a))]


def norm(a):
    return sum((elem ** 2) ** 0.5 for elem in a)


def norm_step(a):
    return sum(elem ** 2 for elem in a)


def to_fraction(a):
    return [Fraction(a[i]) for i in range(len(a))]


def proj(a, b):
    return Fraction(dot(a, b), dot(b, b))


def tilde_base(b, n):
    tilde_b = [[0 for i in range(n + 1)] for i in range(n + 1)]
    for i in range(n + 1):
        #print(i)
        projection = [0 for i in range(n + 1)]
        for j in range(i):
            #print(Decimal(dot(tilde_b[j], tilde_b[j])))
            k = proj(b[i], tilde_b[j])
            projection = vector_sum(projection, vector_koef(tilde_b[j], k))
        projection = vector_koef(projection, -1)
        tilde_b[i] = vector_sum(b[i], projection)
    return tilde_b


'''def build_mu(b, tilde_b):
    mu = [[0 for j in range(i)] for i in range(len(b))]
    for i in range(len(b)):
        for j in range(i):
            mu[i][j] = proj(b[i], tilde_b[j])
    return mu


def update_mu(b, tilde_b, mu, i):
    print(type(i))
    for j in range(i):
        mu[i][j] = proj(b[i], tilde_b[j])
    return mu'''


'''def swap_update(b, tilde_b, mu, k):
    for i in [k - 1, k]:
        projection = [0 for i in range(len(b))]
        for j in range(i):
            c = mu[i][j] if j < k - 1 else proj(b[i], tilde_b[j])
            projection = vector_sum(projection, vector_koef(tilde_b[j], c))
        projection = vector_koef(projection, -1)
        tilde_b[i] = vector_sum(b[i], projection)
    mu = update_mu(b, tilde_b, mu, k - 1)
    mu = update_mu(b, tilde_b, mu, k)
    return tilde_b, mu'''


def reduction(b, tilde_b, n):
    for i in range(1, n):
        for j in range(i - 1, -1, -1):
            k = proj(b[i], tilde_b[j])
            if abs(k) > 0.5:
                k = round(proj(b[i], tilde_b[j]))
                b[i] = vector_sum(b[i], vector_koef(b[j], -k))
    return b


def swap(b, tilde_b, n, delta):
    i = 0
    while i < n - 1:
        v_1 = vector_koef(tilde_b[i], proj(b[i + 1], tilde_b[i]))
        v_1 = vector_sum(v_1, tilde_b[i + 1])
        if delta * norm_step(tilde_b[i]) > norm_step(v_1):
            tmp = b[i + 1]
            b[i + 1] = b[i]
            b[i] = tmp
            print("Swap at {} position".format(i))
            break
        i += 1
    if i == n - 1:
        return b, False
    return b, True


def lll(b, n):
    delta = 0.75
    flag = True
    while flag:
        tilde_b = tilde_base(b, n)
        b = reduction(b, tilde_b, n + 1)
        print("done reduction.")
        tilde_b = tilde_base(b, n)
        b, flag = swap(b, tilde_b, n + 1, delta)
        print("done swap.")
    return b


def hack(w, n, c):
    b = build_base(w, c, n)
    b_res = lll(b, n)
    m = None
    is_0_1 = False
    for i in range(len(w)):
        j = 0
        while j < len(b_res[i]) - 1 and b_res[i][j] in [0, 1]:
            j += 1
        if j == len(b_res) - 1:
            if b_res[i][j] == 0:
                b_res = b_res[i]
                is_0_1 = True
                break
    if is_0_1:
        m = 0
        for j in range(len(b_res) - 1):
            m = m * 2 + b_res[j]
    else:
        print("Unable to achieve result on the first try. Replacing 'S'.")
        b = build_base(w, sum(w[i] for i in range(len(w))) - c, n)
        b_res = lll(b, n)
        j = 0
        is_0_1 = False
        for i in range(len(w)):
            j = 0
            while j < len(b_res[i]) - 1 and b_res[i][j] in [0, 1]:
                j += 1
            if j == len(b_res) - 1:
                if b_res[i][j] == 0:
                    b_res = b_res[i]
                    is_0_1 = True
                    break
        if is_0_1:
            m = 0
            for j in range(len(b_res) - 1):
                m = m * 2 + (1 - b_res[j])
        else:
            exit("Unable to find short vector.")
    return None if m is None else customtypes.type_bytes(m)
