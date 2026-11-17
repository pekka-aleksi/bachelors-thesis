import math

from euclidean.eea import inverse
from fastbin.src.my_file import fast_power


def bsgs(Y, g, N):

    sqrt_N = int(math.floor(math.sqrt(N - 1)))
    d = {fast_power(x=g, n=i, MOD=N): i for i in range(sqrt_N + 1)}

    g_inverse = inverse(g, N)
    u = fast_power(g_inverse, sqrt_N, MOD=N)

    h = Y
    for j in range(1, sqrt_N + 1):
        y_trial = (h * fast_power(u, j, MOD=N)) % N
        if y_trial in d:
            return j * sqrt_N + d[y_trial]


if __name__ == '__main__':
    result1 = bsgs(Y=20, g=5, N=53)
    print("->", result1, "->", 5**result1 % 53)
    result2 = bsgs(Y=2, g=6, N=41)
    print("->", result2, "->", 6**result2 % 41)
    # print(5**11 % 53)


