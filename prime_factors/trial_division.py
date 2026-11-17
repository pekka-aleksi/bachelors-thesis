import collections


def get_factors(n):

    factors = collections.Counter()

    while n % 2 == 0:
        factors[2] += 1
        n //= 2

    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] += 1
            n //= i
        i += 2

    if n > 2:  # the previous parts found no factors, so we append the prime itself
        factors[n] += 1

    return factors

def get_subgroup_sizes(factors):
    return [prime**exp for prime, exp in factors.items()]
