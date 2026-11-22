import copy


class Coefficient:
    def __init__(self, new_value=0):
        self.value: int = new_value

    def __add__(self, other):
        new_value = self.value + other.value
        return Coefficient(new_value=new_value)

    def __sub__(self, other):
        new_value = self.value - other.value
        return Coefficient(new_value=new_value)

    def __mul__(self, other):
        new_value = self.value * other.value
        return Coefficient(new_value=new_value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, Coefficient):
            return self.value == other.get_coefficient()

    def __truediv__(self, other):
        new_value = self.value / other.value
        return Coefficient(new_value=new_value)

    def __bool__(self):
        return bool(self.value)

    def __str__(self):
        return f"{self.value}"

    def get_coefficient(self):
        return self.value

    def __ne__(self, other):

        diff = abs(self.value - other.value)
        return diff >= 1e-7


class Degree:
    def __init__(self, new_value=0):
        self.value: int = new_value

    def __add__(self, other):
        new_value = self.value + other.value
        return Degree(new_value=new_value)

    def __mul__(self, other):
        new_value = self.value + other.value
        return Degree(new_value=new_value)

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, Degree):
            return self.value == other.get_degree()

    def __truediv__(self, other):
        new_value = self.value - other.value
        return Degree(new_value=new_value)

    def __str__(self):
        return f"{self.value}"

    def get_degree(self):
        return self.value

    def __ne__(self, other):
        return self.value != other.value


class Monomial:

    def __init__(self, new_coefficient=Coefficient(), new_degree=Degree()):
        self.a: Coefficient = new_coefficient
        self.degree: Degree = new_degree

    def __str__(self):
        if self.a == 0:
            return ""
        elif self.degree == 0:
            return f"{self.a}"

        elif self.degree == 1:
            return f"{self.a}X"
        else:
            return f"{self.a}X^{self.degree}"

        return f"{self.a}*X^{self.degree}"

    def __add__(self, other):
        if isinstance(other, Monomial):
            if self.degree == other.degree:  # same degree
                new_coefficient = self.a + other.a  # add coefficients
                return Monomial(new_coefficient=new_coefficient,
                                new_degree=Degree(new_value=self.degree.get_degree()))
            else:  # different degree
                return copy.deepcopy(other)

    def __sub__(self, other):
        if self.degree == other.degree:
            new_coefficient = self.a - other.a
            return Monomial(new_coefficient=new_coefficient,
                            new_degree=Degree(new_value=self.degree.get_degree()))

    def __mul__(self, other):
        if isinstance(other, Monomial):
            new_coefficient = self.a * other.a
            new_degree = self.degree * other.degree

            return Monomial(new_coefficient=new_coefficient, new_degree=new_degree)

    def __truediv__(self, other):
        new_coeff = self.a / other.a
        new_degree = self.degree / other.degree

        new_monomial = Monomial(new_coefficient=new_coeff,
                                new_degree=new_degree)
        return new_monomial

    def __gt__(self, other):
        return self.degree > other.degree

    def __bool__(self):
        return bool(self.a)

    def __ne__(self, other):
        different_degree = self.degree != other.degree
        different_coeff = self.a != other.a

        return different_coeff or different_degree

    def get_degree(self):
        return self.degree.get_degree()

    def get_coefficient(self):
        return self.a.get_coefficient()


class Polynomial:
    _TOKEN = object()

    @classmethod
    def from_tuples(cls, new_coefficients: tuple[int, ...]):
        monomials = {
            degree: Monomial(new_coefficient=Coefficient(new_value=coefficient),
                             new_degree=Degree(new_value=degree))
            for degree, coefficient in enumerate(new_coefficients)
        }

        # print(monomials)
        return cls(monomials, _token=Polynomial._TOKEN)

    @classmethod
    def from_monomials(cls, new_monomials: dict[int, Monomial]):

        return cls(new_monomials, _token=Polynomial._TOKEN)

    @classmethod
    def get_empty_degree_n(cls, n):
        monomials = {i: Monomial(new_coefficient=Coefficient(), new_degree=Degree(new_value=i)) for i in range(n + 1)}
        return Polynomial.from_monomials(monomials)

    @classmethod
    def summate(cls, values):
        new_values_for_poly = {}

        new_dict = {}

        for degree, monomial in values.items():
            deg = monomial.get_degree()
            coeff_list = new_dict.get(deg)
            if not coeff_list:
                new_dict[degree] = list()
            new_dict[degree].append(monomial.get_coefficient())

        for degree, coefficients_list in new_dict.items():
            new_coeff_value = sum(coefficients_list)

            new_monomial = Monomial(new_coefficient=Coefficient(new_value=new_coeff_value),
                                    new_degree=Degree(new_value=degree))
            new_values_for_poly[degree] = new_monomial

        return new_values_for_poly

    def __init__(self, values, *, _token=None):
        if _token is not self._TOKEN:
            raise TypeError("Use Polynomial.from_tuples or Polynomial.from_monomials")

        new_monomials_for_poly = Polynomial.summate(values)

        if not new_monomials_for_poly:
            new_monomials_for_poly = {0: Monomial()}

        self.monomials = new_monomials_for_poly

    def __add__(self, other):

        new_monomials = copy.deepcopy(self.monomials)

        if isinstance(other, Polynomial):
            for degree, B in other.monomials.items():
                A = self.monomials.get(degree)
                if A is None:
                    A = Monomial(Coefficient(0), new_degree=Degree(degree))
                new_monomials[degree] = A + B

            return Polynomial.from_monomials(new_monomials)

    def __sub__(self, other):
        new_monomials = copy.deepcopy(self.monomials)

        for degree, B in other.monomials.items():
            A = self.monomials.get(degree)
            if A is None:
                A = Monomial(Coefficient(0), new_degree=Degree(degree))
            new_monomials[degree] = A - B

        return Polynomial.from_monomials(new_monomials)


    def __ne__(self, other):

        #        ax^3 + bx + c
        # dx^4 +        cx

        #  both_keys = {1}
        #  a_zeros = {0, 3}
        #  b_zeros = {4}

        both_keys = self.monomials.keys() & other.monomials.keys()
        # print(both_keys)
        a_zeros = tuple(self.monomials.keys() - both_keys)
        b_zeros = tuple(other.monomials.keys() - both_keys)

        # nollas aste ei ole ongelma, vaan nollakerroin

        for degree in a_zeros:
            if self.monomials[degree] != Monomial(Coefficient(0), new_degree=Degree(degree)):
                return True

        for degree in b_zeros:
            if other.monomials[degree] != Monomial(Coefficient(0), new_degree=Degree(degree)):
                return True

        for degree in both_keys:
            A = self.monomials[degree]
            B = other.monomials[degree]
            print("A", A, "B", B)
            if A != B:
                return True

        return False

    def __mul__(self, other):

        new_monomials = {}

        for aXn in self.monomials.values():
            for bXm in other.monomials.values():
                result = aXn * bXm
                new_monomials[result.get_degree()] = result
        return Polynomial.from_monomials(new_monomials)

    def get_monomials_from_highest_deg(self, nonzero=True):
        return sorted(filter(lambda x: x[1], self.monomials.items()), key=lambda x: x[0], reverse=True)

    def get_n_leading_terms(self, n):
        highest = self.get_monomials_from_highest_deg()
        return highest[0:n+1]

    def __divmod__(self, other):

        Zero = Polynomial.from_tuples((0,))

        deg_num = self.get_degree(nonzero=True)
        deg_den = other.get_degree(nonzero=True)

        if deg_num < deg_den:
            return 0, copy.deepcopy(other)

        numerator = copy.deepcopy(self)

        zeros = Polynomial.get_empty_degree_n(numerator.get_degree(nonzero=True))
        # print(len(numerator.monomials))
        numerator = numerator + zeros
        # print(len(numerator.monomials))
        #divisor = copy.deepcopy(other)

        remainder = copy.deepcopy(other)
        # print("Remainder:", *remainder.monomials.values(), "vs. Zero items():", *Zero.monomials.values())

        # print("divisor.get_degree()", divisor.get_degree())
        # print("remainder != Zero", remainder != Zero, remainder == Zero)
        print(remainder, type(remainder))
        quotient = Polynomial.from_tuples((0,))

        print("Remainder degree", remainder.get_degree(), "divisor degree", other.get_degree())
        #print(remainder != Zero, remainder == Zero)

        i = 0
        NUM_terms = numerator.get_n_leading_terms(deg_num)


        remainder = copy.deepcopy(self)
        denominator = copy.deepcopy(other)

        _, jakava_termi = denominator.get_n_leading_terms(deg_den)[0]

        while remainder != Zero and remainder.get_degree() >= denominator.get_degree():

            _, jaettava_termi = remainder.get_n_leading_terms(remainder.get_degree())[0]

            print("while loop, Remainder:", remainder, "vs. Zero items():",
                  *Zero.monomials.values())

            # we always divide by the same thing, but
            # the next term to divide comes from the previous round

            uusi_termi = jaettava_termi / jakava_termi
            new_polyterm = Polynomial.from_monomials({uusi_termi.get_degree(): uusi_termi})

            print("\tjaettava termi", jaettava_termi, "ja remainderin aste", remainder.get_degree())
            print("\tjakava_termi", jakava_termi)
            print("-"*80)
            print("\tnew_polyterm", new_polyterm)
            print("\tquotient", quotient)#, "divisor", divisor)
            quotient = quotient + new_polyterm
            print("\tquotient+new_polyterm:", quotient)
            print("\tremainder", remainder)
            remainder = remainder - new_polyterm * Polynomial.from_monomials({jakava_termi.get_degree(): jakava_termi})
            print("\tremainder - new_polyterm*quotient", remainder)
            #print("REMAINDER", remainder, "JAETTAVA DEGREE", remainder.get_degree(nonzero=True), "ja", denominator.get_degree(nonzero=True))
            print()

        return quotient, remainder

    def get_degree(self, nonzero=True):

        if nonzero:
            data = {degree: monomial.get_coefficient() for degree, monomial in self.monomials.items() if monomial}
        else:
            data = self.monomials

        #try:
        highest = max(data)
        #except ValueError:
        #    highest = 0
        return highest

    def __str__(self):

        to_print = []

        for monomial in self.monomials.values():
            if monomial:
                to_print.append(f"{monomial}")

        return " + ".join(to_print)


if __name__ == '__main__':
    # poly1 = Polynomial.from_tuples((1, 1, -2, 0, 0, 5))
    # poly2 = Polynomial.from_tuples((-1, -1, -2, 0, 0, 5))

    # print(poly1)
    # print(poly2)
    # t = poly1 * poly2
    # print(poly1)
    # print(poly2)
    # print(t)
    # a = Polynomial.from_tuples((2, 2))
    # b = Polynomial.from_tuples((2,))

    C = Monomial(Coefficient(new_value=1), Degree(0))
    X = Monomial(Coefficient(new_value=1), Degree(1))
    X2 = Monomial(Coefficient(new_value=1), Degree(2))

    poly0 = Polynomial.from_monomials({0: C})
    poly1 = Polynomial.from_monomials({1: X})
    poly2 = Polynomial.from_monomials({2: X2})

    # print("double:", poly1 + poly1)
    # print("zero:", poly1 - poly1)

    # t = poly0 + poly1 + poly2

    # print("constant", poly0 * poly0)
    # print("mult", poly1 * poly2, poly1.get_degree())
    # print("linear", poly1 + poly1)
    # print("second", poly2 + poly2)
    # print("full second degree", t)


    #B = poly1
    A = poly0 + poly1 + poly2
    B = poly1

    #print(poly2.get_degree(nonzero=True))
    q, r = divmod(A, B)

    print(f"({A}) / {B} = ({q}) * ({B}) + {r}")


    # print("q", q, type(q))
    # print("r", r, type(r))
