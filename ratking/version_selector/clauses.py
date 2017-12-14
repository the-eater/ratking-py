class GenericClause:
    def test(self, value):
        pass

    def __repr__(self):
        return self.__class__.__name__ + '()'


class AnyClause(GenericClause):
    def test(self, value):
        return True


class UnionClause(GenericClause):
    left = None
    right = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.left) + ', ' + str(self.right) + ')'


class OrClause(UnionClause):
    def test(self, value):
        if self.left.test(value):
            return True

        return self.right.test(value)


class AndClause(UnionClause):
    def test(self, value):
        return self.left.test(value) and self.right.test(value)


class SimpleClause(GenericClause):
    op = None
    version = None

    def __init__(self, op, version):
        self.op = op
        self.version = version

    def test(self, value):
        if self.op == '>':
            return value > self.version

        if self.op == '<':
            return value < self.version

        if self.op == '=':
            return value == self.version

        if self.op == '>=':
            return value >= self.version

        if self.op == '<=':
            return value <= self.version

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.op) + ', ' + str(self.version) + ')'


class InverseClause(GenericClause):
    clause = None

    def __init__(self, clause):
        self.clause = clause

    def test(self, value):
        return not self.clause.test(value)

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.clause) + ')'
