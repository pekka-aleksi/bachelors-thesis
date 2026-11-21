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


"""
class Indeterminate:
    def __init__(self, new_degree=Degree()):
        self.X: Degree = new_degree

    def __mul__(self, other):
        new_degree = self.X + other.X
        return Indeterminate(new_degree=new_degree)

    def __eq__(self, other):
        if isinstance(other, Indeterminate):
            return self.X == other.X
        elif isinstance(other, Degree):
            return self.X == other
        elif isinstance(other, int):
            return self.X == Degree(new_value=other)

    def __truediv__(self, other):
        new_degree = self.X / other.X
        return Indeterminate(new_degree=new_degree)

    def __gt__(self, other):
        return self.X > other.X

    def __str__(self):
        return f"{self.X}"

    def get_degree(self):
        return self.X.get_degree()
"""


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
                return other

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

        max_degree = max(new_monomials)
        LEN = len(new_monomials)

        #print("max_degree", max_degree, "LEN", LEN)

        if LEN != max_degree + 1:
            #print("we're missing some degree(s) from:", *new_monomials.items())

            poly = Polynomial.get_empty_degree_n(max_degree + 1)

            #print(new_monomials)

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
        new_monomials = {}

        for degree, B in other.monomials.items():
            A = self.monomials[degree]
            new_monomials[degree] = A - B

        return Polynomial.from_monomials(new_monomials)

    def __ne__(self, other):

        A = self.get_monomials_from_highest_deg()
        B = other.get_monomials_from_highest_deg()

        NA = len(A)
        NB = len(B)

        if NA != NB:
            return True

        for i in range(NA):
            if A[i] != B[i]:
                return True

        return False

    def __mul__(self, other):

        new_monomials = {}

        for aXn in self.monomials.values():
            for bXm in other.monomials.values():
                result = aXn * bXm
                print("multiplication result for", aXn, "*", bXm, "=", result, "is degree", result.get_degree())
                new_monomials[result.get_degree()] = result
        return Polynomial.from_monomials(new_monomials)

    def get_monomials_from_highest_deg(self):
        return sorted(self.monomials.items(), key=lambda x: x[0], reverse=True)

    def get_two_leading_terms(self):
        highest = self.get_monomials_from_highest_deg()
        return highest[0:2]

    def __divmod__(self, other):

        deg_num = self.get_degree()
        deg_den = other.get_degree()

        if deg_num < deg_den:
            return 0, other

        import copy

        NUM = copy.deepcopy(self)
        DEN = copy.deepcopy(other)

        quotient = Polynomial.from_tuples((0,))
        Zero = Polynomial.from_tuples((0,))
        remainder = Polynomial.from_monomials(self.monomials)

        #print(remainder, type(remainder))

        # huom. tyhjä polynomi ei vertaannu. lisäksi vertailuoperaattoreita puuttuu ==
        while remainder != Zero and remainder.get_degree() >= DEN.get_degree():

            monomials_num = Polynomial.from_monomials(NUM.monomials)
            monomials_den = Polynomial.from_monomials(DEN.monomials)

            try:
                tmp = Polynomial.from_monomials(tuple([monomials_num[0] / monomials_den[0]]))
                #print(tmp)
            except IndexError:
                tmp = Polynomial.from_tuples((0,))
            except ZeroDivisionError:
                return quotient, Zero

            quotient = quotient + tmp
            remainder = remainder - tmp * DEN  # tässä kerrotaan kenties väärinpäin kokonaan?

            #print("REMAINDER", quotient, tmp, DEN, remainder, remainder != Zero, remainder == Zero)
            NUM.monomials = NUM.monomials[1:]
            DEN.monomials = DEN.monomials[1:]

        return quotient, remainder

    def get_degree(self):
        try:
            highest = max(self.monomials)
        except ValueError:
            highest = 0
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

    print("double:", poly1 + poly1)
    print("zero:", poly1 - poly1)

    t = poly0 + poly1 + poly2

    print("constant", poly0 * poly0)
    print("mult", poly1 * poly2, poly1.get_degree())
    print("linear", poly1 + poly1)
    print("second", poly2 + poly2)
    print("full second degree", t)

    # q, r = divmod(a, b)

    # print("q", q, type(q))
    # print("r", r, type(r))
