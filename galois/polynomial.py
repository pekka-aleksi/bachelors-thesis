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

    def __str__(self):
        return f"{self.X}"

    def get_degree(self):
        return self.X.get_degree()


class Monomial:

    def __init__(self, new_coefficient=Coefficient(), new_indeterminate=Indeterminate()):
        self.a: Coefficient = new_coefficient
        self.x: Indeterminate = new_indeterminate

    def __str__(self):
        if self.a == 0:
            return ""
        elif self.x == 0:
            return f"{self.a}"

        elif self.x == 1:
            return f"{self.a}X"
        else:
            return f"{self.a}X^{self.x}"

        return f"{self.a}*X^{self.x}"

    def __add__(self, other):
        if isinstance(other, Monomial):
            if self.x == other.x:  # same degree
                new_coefficient = self.a + other.a  # add coefficients
                return Monomial(new_coefficient=new_coefficient,
                                new_indeterminate=Indeterminate(new_degree=Degree(new_value=self.x.get_degree())))
            else:  # different degree
                return other

    def __sub__(self, other):
        if self.x == other.x:
            new_coefficient = self.a - other.a
            return Monomial(new_coefficient=new_coefficient,
                            new_indeterminate=Indeterminate(new_degree=Degree(new_value=self.x.get_degree())))

    def __mul__(self, other):
        if isinstance(other, Monomial):
            new_coefficient = self.a * other.a
            new_indeterminate = self.x * other.x

            return Monomial(new_coefficient=new_coefficient, new_indeterminate=new_indeterminate)

    def __truediv__(self, other):
        new_coeff = self.a / other.a
        new_indeterm = self.x / other.x

        new_monomial = Monomial(new_coefficient=new_coeff,
                                new_indeterminate=new_indeterm)
        return new_monomial

    def __bool__(self):
        return bool(self.a)

    def get_degree(self):
        return self.x.get_degree()

    def get_coefficient(self):
        return self.a.get_coefficient()


class Polynomial:
    _TOKEN = object()

    @classmethod
    def from_tuples(cls, new_coefficients: tuple[int, ...]):
        monomials = tuple(
            Monomial(new_coefficient=Coefficient(new_value=coefficient),
                     new_indeterminate=Indeterminate(new_degree=Degree(new_value=degree)))
            for degree, coefficient in enumerate(new_coefficients)
        )

        # print(monomials)
        return cls(monomials, _token=Polynomial._TOKEN)

    @classmethod
    def from_monomials(cls, new_monomials: tuple[Monomial, ...]):

        max_degree = max(monomial.get_degree() for monomial in new_monomials)
        LEN = len(new_monomials)

        print("max_degree", max_degree, "LEN", LEN)
        if LEN != max_degree + 1:
            print("we're missing some degree(s) from:", *new_monomials)

            poly = Polynomial.get_empty_degree_n(max_degree+1)

            sorted_new_monomials = sorted(new_monomials, key=lambda m: m.get_degree(), reverse=False)





            print(new_monomials)

        return cls(new_monomials, _token=Polynomial._TOKEN)

    @classmethod
    def get_empty_degree_n(cls, n):
        monomials = tuple(Monomial(new_coefficient=Coefficient(),
                                   new_indeterminate=Indeterminate(new_degree=Degree(new_value=i))) for i in
                          range(n + 1))
        return Polynomial.from_monomials(monomials)

    @classmethod
    def summate(cls, values):
        new_values_for_poly = list()
        new_dict = dict.fromkeys(monomial.get_degree() for monomial in values)

        for monomial in values:
            deg = monomial.get_degree()
            coeff_list = new_dict.get(deg)
            if not coeff_list:
                new_dict[deg] = list()
            new_dict[deg].append(monomial.get_coefficient())

        for degree, coefficients_list in new_dict.items():
            new_coeff_value = sum(coefficients_list)

            new_monomial = Monomial(new_coefficient=Coefficient(new_value=new_coeff_value),
                                    new_indeterminate=Indeterminate(new_degree=Degree(new_value=degree)))
            new_values_for_poly.append(new_monomial)

        return new_values_for_poly

    def __init__(self, values, *, _token=None):
        if _token is not self._TOKEN:
            raise TypeError("Use Polynomial.from_tuples or Polynomial.from_monomials")

        new_monomials_for_poly = Polynomial.summate(values)

        if not new_monomials_for_poly:
            new_monomials_for_poly = [Monomial()]

        self.monomials = tuple(new_monomials_for_poly)

    def __add__(self, other):

        new_monomials = []

        if isinstance(other, Polynomial):
            for monomial in other.monomials:
                new_monomials.append(self.monomials[monomial.get_degree()] + monomial)

            return Polynomial.from_monomials(tuple(new_monomials))

    def __sub__(self, other):
        new_monomials = []

        for monomial in other.monomials:
            new_monomials.append(self.monomials[monomial.get_degree()] - monomial)

        return Polynomial.from_monomials(tuple(new_monomials))

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

        new_monomials = list()
        for aXn in self.monomials:
            for bXm in other.monomials:
                result = aXn * bXm
                new_monomials.append(result)
        return Polynomial.from_monomials(tuple(new_monomials))

    def get_monomials_from_highest_deg(self):

        values = tuple(monomial for monomial in self.monomials)
        return sorted(values, key=lambda x: x.get_degree(), reverse=True)

    def get_two_leading_terms(self):
        highest = self.get_monomials_from_highest_deg()

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

        print(remainder, type(remainder))

        # huom. tyhjä polynomi ei vertaannu. lisäksi vertailuoperaattoreita puuttuu ==
        while remainder != Zero and remainder.get_degree() >= DEN.get_degree():

            monomials_num = Polynomial.from_monomials(NUM.monomials).get_monomials_from_highest_deg()
            monomials_den = Polynomial.from_monomials(DEN.monomials).get_monomials_from_highest_deg()

            try:
                tmp = Polynomial.from_monomials(tuple([monomials_num[0] / monomials_den[0]]))
                print(tmp)
            except IndexError:
                tmp = Polynomial.from_tuples((0,))
            except ZeroDivisionError:
                return quotient, Zero

            quotient = quotient + tmp  # tmp tulee järjestetystä polysta, mutta DEN tulee järjestämättömästä
            remainder = remainder - tmp * DEN  # tässä kerrotaan kenties väärinpäin kokonaan?

            print("REMAINDER", quotient, tmp, DEN, remainder, remainder != Zero, remainder == Zero)
            NUM.monomials = NUM.monomials[1:]
            DEN.monomials = DEN.monomials[1:]

        return quotient, remainder

    def get_degree(self):
        try:
            highest = max(monomial.get_degree() for monomial in self.monomials)
        except ValueError:
            highest = 0
        return highest

    def __str__(self):

        to_print = []

        for monomial in self.monomials:
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

    C = Monomial(Coefficient(new_value=1), Indeterminate(Degree(0)))
    X = Monomial(Coefficient(new_value=1), Indeterminate(Degree(1)))
    X2 = Monomial(Coefficient(new_value=1), Indeterminate(Degree(2)))

    poly1 = Polynomial.from_monomials((X, X2))
    poly2 = Polynomial.from_monomials((X2,))

    print(poly1 + poly2)

    # q, r = divmod(a, b)

    # print("q", q, type(q))
    # print("r", r, type(r))
