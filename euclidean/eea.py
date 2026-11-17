def eea(a, b):
    quotients = [None, None]
    remainders = [a, b]

    s = [1, 0]
    t = [0, 1]

    index = 2
    while remainders[-1] != 0:
        print(remainders)
        next_q, next_r = divmod(remainders[index - 2], remainders[index - 1])
        remainders.append(next_r)
        quotients.append(next_q)
        next_s = s[index - 2] - next_q * s[index - 1]
        next_t = t[index - 2] - next_q * t[index - 1]
        s.append(next_s)
        t.append(next_t)
        index += 1

    return s[-2], t[-2], remainders[-2]


def inverse(a, n):
    t, newt = 0, 1
    r, newr = n, a

    while newr != 0:
        quotient = r // newr

        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr

    if r > 1:
        raise Exception(f"{a} is not invertible mod {n}")
    if t < 0:
        t = t + n

    return t

if __name__ == '__main__':
    a, b = 15, 3

    X, Y, GCD = eea(a, b)

    print(X * a + Y * b, GCD)


