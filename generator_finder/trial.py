from fastbin.exp import fast_power
from prime_factors.trial_division import get_factors
import collections


def totient(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p

        # result *= (1 - 1/p)
        result -= result // p
        p += 1

    if n > 1:
        result -= result // n

    return result


def find_generator_ZnZstar(N):
    groupsize = N - 1
    primes = get_factors(groupsize)

    prime_results = collections.defaultdict(list)

    for g in range(2, N):
        for q in primes:
            R = fast_power(g, groupsize // q, N)
            if R != 1:
                prime_results[g].append(R)
            if len(prime_results[g]) == len(primes):
                return g



if __name__ == '__main__':
    print(find_generator_ZnZstar(7))
    print(find_generator_ZnZstar(100057))
    print(find_generator_ZnZstar(1000081))
    print(find_generator_ZnZstar(10000139))
    print(find_generator_ZnZstar(100000073))