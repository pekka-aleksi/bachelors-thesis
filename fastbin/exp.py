def fast_power(x, n, MOD=7):
    if n == 0:
        return 1

    if n == 1:
        return x % MOD

    E = [0] + list(bin(n)[2:])

    l = [1 for _ in E]

    i = 1

    while i < len(l):
        if E[i] == '1':
            l[i] = ((l[i - 1] * l[i - 1]) * x) % MOD  # multiply from right
        else:  # we run into zero
            l[i] = (l[i - 1] * l[i - 1]) % MOD  # no multiplication
        i += 1

    return l[-1]


if __name__ == '__main__':
    MOD = 17

    testdata = [
        (5, 3, (5 ** 3) % MOD),
        (8, 13, (8 ** 13) % MOD)
    ]

    for x, y, r in testdata:
        print(fast_power(x, y, MOD))
