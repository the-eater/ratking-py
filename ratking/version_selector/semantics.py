from .grammar import SelectorSemantics

class VersionSelectorSemantics(SelectorSemantics):
    def or_op(self, ast):
        return '|'

    def and_op(self, ast):
        return '&'

    def binary_op(self, ast):
        if ast == 'not':
            return '!'

        return ast

    def exact_op(self, ast):
        return '='

    def about_op(self, ast):
        return '~'

    def greater_than_equals_op(self, ast):
        return '>='

    def greater_than_op(self, ast):
        return '>'

    def less_than_equals_op(self, ast):
        return '<='

    def less_than_op(self, ast):
        return '<'

    def union(self, ast):
        return [ast.mid, ast.left, ast.right]