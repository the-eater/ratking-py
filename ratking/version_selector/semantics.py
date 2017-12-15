from .grammar import SelectorSemantics
from .clauses import *
from ..rat_version import RatVersion


class VersionSelectorSemantics(SelectorSemantics):
    def or_op(self, ast):
        return '|'

    def and_op(self, ast):
        return '&'

    def binary_op(self, ast):
        if ast == 'not':
            return '!'

        return ast

    def version(self, ast):
        return RatVersion(ast)

    def exact_op(self, ast):
        return '='

    def about_op(self, ast):
        if ast == '^':
            return '^'

        return '~'

    def greater_than_equals_op(self, ast):
        return '>='

    def greater_than_op(self, ast):
        return '>'

    def less_than_equals_op(self, ast):
        return '<='

    def less_than_op(self, ast):
        return '<'

    def any_op(self, ast):
        return AnyClause()

    def union(self, ast):
        if ast.mid == '&':
            return AndClause(ast.left, ast.right)

        return OrClause(ast.left, ast.right)

    def invert(self, ast):
        if isinstance(ast[1], InverseClause):
            return ast[1].clause

        return InverseClause(ast[1])

    def version_selector(self, ast):
        if ast[0] in ['~', '^']:
            return AboutClause(ast[0], ast[1])

        return SimpleClause(ast[0], ast[1])

    def range_op(self, ast):
        inclusive = ast[0] == 'from'

        if inclusive:
            return AndClause(SimpleClause('>=', ast[1]), SimpleClause('<=', ast[3]))

        return AndClause(SimpleClause('>', ast[1]), SimpleClause('<', ast[3]))
