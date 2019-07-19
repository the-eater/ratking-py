from ..rat_version import RatVersion
from copy import deepcopy


class GenericClause:
    def test(self, value):
        pass

    def __repr__(self):
        return self.__class__.__name__ + '()'

    def to_dict(self):
        return {
            'type': self.__class__.__name__
        }

    def to_str(self):
        return ''


class AnyClause(GenericClause):
    def test(self, value):
        return True

    def to_str(self):
        return '*'


class UnionClause(GenericClause):
    left = None
    right = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.left) + ', ' + str(self.right) + ')'

    def to_dict(self):
        our_dict = super().to_dict()
        our_dict['left'] = self.left.to_dict()
        our_dict['right'] = self.right.to_dict()

        return our_dict

    def to_str(self):
        return '{} {} {}'.format(self.left.to_str(), "and" if self is AndClause else "or", self.right.to_str())


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

    def to_dict(self):
        our_dict = super().to_dict()
        our_dict['op'] = self.op
        our_dict['version'] = str(self.version)

        return our_dict

    def to_str(self):
        return "{}{}".format(self.op if self.op != "=" else "", self.version.to_str())


class AboutClause(AndClause):
    about_op = None
    about_version = None

    def __init__(self, op, version):
        self.about_op = op
        self.about_version = version

        if version.parts[0].is_numeric:
            new_version = deepcopy(version)
            while len(new_version.parts[0].parts) <= 2:
                new_version.parts[0].parts.append(0)

            if op == '^':
                new_version.parts[0].parts[1] = '*'
                new_version.parts[0].parts[2] = '*'
            else:
                new_version.parts[0].parts[2] = '*'

            version = new_version

        super().__init__(SimpleClause('=', version), SimpleClause('>=', self.about_version))

    def __repr__(self):
        return self.__class__.__name__ + '(' + self.to_str() + ' -> ' + self.left.to_str() + ' and ' + self.right.to_str() + '>'

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'op': self.about_op,
            'version': str(self.about_version)
        }

    def to_str(self):
        return "{}{}".format(self.about_op, self.about_version.to_str())


class InverseClause(GenericClause):
    clause = None

    def __init__(self, clause):
        self.clause = clause

    def test(self, value):
        return not self.clause.test(value)

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.clause) + ')'

    def to_dict(self):
        our_dict = super().to_dict()
        our_dict['clause'] = self.clause.to_dict()

        return our_dict

    def to_str(self):
        return "not {}".format(self.clause.to_str())


def from_dict(clause_dict):
    clause_type = clause_dict['type']

    if clause_type == 'SimpleClause':
        return SimpleClause(clause_dict['op'], RatVersion.from_str(clause_dict['version']))

    if clause_type == 'AboutClause':
        return AboutClause(clause_dict['op'], RatVersion.from_str(clause_dict['version']))

    if clause_type == 'InverseClause':
        return InverseClause(from_dict(clause_dict['clause']))

    if clause_type == 'AndClause':
        return AndClause(from_dict(clause_dict['left']), from_dict(clause_dict['right']))

    if clause_type == 'OrClause':
        return OrClause(from_dict(clause_dict['left']), from_dict(clause_dict['right']))

    return AnyClause()
