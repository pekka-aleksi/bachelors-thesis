from fastbin.exp import fast_power
from generator_finder.trial import find_generator_ZnZstar
from prime_factors.trial_division import get_factors
from shanks.bsgs import bsgs
from sympy.ntheory.modular import crt
import time

def ph(generator, target, modulo):

    start_time = time.time()

    groupsize = modulo - 1
    qe_dict = get_factors(groupsize)

    g = {q: fast_power(generator, groupsize // fast_power(q, e, modulo), modulo) for q, e in qe_dict.items()}
    h = {q: fast_power(target, groupsize // fast_power(q, e, modulo), modulo) for q, e in qe_dict.items()}

    congruences = {}
    for (Q, E), lhs, rhs in zip(qe_dict.items(), g.values(), h.values()):
        result = bsgs(g=lhs, Y=rhs, N=modulo)
        congruences[Q ** E] = result

    moduli = congruences.keys()
    residues = congruences.values()

    results = crt(moduli, residues)

    for result in results:
        print(result, ":", generator ** result % modulo, "=", target % modulo)

    print(time.time() - start_time, "seconds")

    return congruences


if __name__ == '__main__':
    print(ph(generator=find_generator_ZnZstar(11251), target=9689, modulo=11_251))
    print("-"*80)
    print(ph(generator=find_generator_ZnZstar(100057), target=9689, modulo=100_057))
    print("-" * 80)
    print(ph(generator=find_generator_ZnZstar(1000081), target=9689, modulo=1_000_081))
    print("-" * 80)
    print(ph(generator=find_generator_ZnZstar(10000139), target=10000137, modulo=10_000_139))
    #print("-" * 80)
    #print(ph(generator=find_generator_ZnZstar(100000073), target=10000137, modulo=100_000_073))




