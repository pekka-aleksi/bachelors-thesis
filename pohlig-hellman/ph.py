from fastbin.exp import fast_power
from prime_factors.trial_division import get_factors
from shanks.bsgs import bsgs
from sympy.ntheory.modular import crt


def ph(generator, target, modulo):
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

    return congruences


if __name__ == '__main__':
    print(ph(generator=23, target=9689, modulo=11251))
