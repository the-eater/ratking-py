#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}  # type: ignore


class SelectorBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(SelectorBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class SelectorParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=SelectorBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(SelectorParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    def _start_(self):  # noqa
        self._expression_()
        self._check_eof()

    @tatsumasu()
    def _version_(self):  # noqa
        self._pattern(r'v?[0-9][a-z0-9-*_\.]*')

    @tatsumasu()
    def _and_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('&')
            with self._option():
                self._token('and')
            with self._option():
                self._token('but')
            self._error('no available options')

    @tatsumasu()
    def _or_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('|')
            with self._option():
                self._token('or')
            self._error('no available options')

    @tatsumasu()
    def _comb_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._or_op_()
            with self._option():
                self._and_op_()
            self._error('no available options')

    @tatsumasu()
    def _binary_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('!')
            with self._option():
                self._token('not')
            self._error('no available options')

    @tatsumasu()
    def _version_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._greater_than_equals_op_()
            with self._option():
                self._greater_than_op_()
            with self._option():
                self._less_than_equals_op_()
            with self._option():
                self._less_than_op_()
            with self._option():
                self._about_op_()
            with self._option():
                self._exact_op_()
            with self._option():
                self._binary_op_()
            self._error('no available options')

    @tatsumasu()
    def _exact_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('==')
            with self._option():
                self._token('=')
            with self._option():
                self._token('exact')
            with self._option():
                self._token('is')
            self._error('no available options')

    @tatsumasu()
    def _about_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('~')
            with self._option():
                self._token('about')
            with self._option():
                self._token('abt')
            self._error('no available options')

    @tatsumasu()
    def _greater_than_equals_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('>=')
            with self._option():
                self._token('greater')
                self._token('than')
                with self._optional():
                    self._token('or')
                self._token('equals')
            with self._option():
                self._token('gte')
            self._error('no available options')

    @tatsumasu()
    def _less_than_equals_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('>=')
            with self._option():
                self._token('less')
                self._token('than')
                with self._optional():
                    self._token('or')
                self._token('equals')
            with self._option():
                self._token('lte')
            self._error('no available options')

    @tatsumasu()
    def _greater_than_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('>')
            with self._option():
                self._token('greater')
                self._token('than')
            with self._option():
                self._token('gt')
            self._error('no available options')

    @tatsumasu()
    def _less_than_op_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('<')
            with self._option():
                self._token('less')
                self._token('than')
            with self._option():
                self._token('lt')
            self._error('no available options')

    @tatsumasu()
    def _expression_(self):  # noqa
        with self._choice():
            with self._option():
                self._union_()
            with self._option():
                self._selector_()
            self._error('no available options')

    @tatsumasu()
    def _union_(self):  # noqa
        self._selector_()
        self.name_last_node('left')
        self._comb_op_()
        self.name_last_node('mid')
        self._expression_()
        self.name_last_node('right')
        self.ast._define(
            ['left', 'mid', 'right'],
            []
        )

    @tatsumasu()
    def _selector_(self):  # noqa
        with self._choice():
            with self._option():
                self._version_op_()
                self._version_()
            with self._option():
                self._binary_op_()
                self._selector_()
            with self._option():
                self._version_()
            with self._option():
                self._token('(')
                self._expression_()
                self.name_last_node('@')
                self._token(')')
            self._error('no available options')


class SelectorSemantics(object):
    def start(self, ast):  # noqa
        return ast

    def version(self, ast):  # noqa
        return ast

    def and_op(self, ast):  # noqa
        return ast

    def or_op(self, ast):  # noqa
        return ast

    def comb_op(self, ast):  # noqa
        return ast

    def binary_op(self, ast):  # noqa
        return ast

    def version_op(self, ast):  # noqa
        return ast

    def exact_op(self, ast):  # noqa
        return ast

    def about_op(self, ast):  # noqa
        return ast

    def greater_than_equals_op(self, ast):  # noqa
        return ast

    def less_than_equals_op(self, ast):  # noqa
        return ast

    def greater_than_op(self, ast):  # noqa
        return ast

    def less_than_op(self, ast):  # noqa
        return ast

    def expression(self, ast):  # noqa
        return ast

    def union(self, ast):  # noqa
        return ast

    def selector(self, ast):  # noqa
        return ast


def main(filename, start='start', **kwargs):
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = SelectorParser()
    return parser.parse(text, start=start, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, SelectorParser, name='Selector')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()

