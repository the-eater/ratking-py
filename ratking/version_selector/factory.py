from .semantics import VersionSelectorSemantics
from .grammar import SelectorParser
from .clauses import AnyClause
from tatsu.exceptions import FailedParse

cache = dict()
parser = SelectorParser(semantics=VersionSelectorSemantics())


def parse_version_selector(version_selector, fail_any=False):
    if version_selector not in cache:
        try:
            cache[version_selector] = parser.parse(version_selector)
        except FailedParse:
            if fail_any:
                return AnyClause()

            print('Failed to parse selector: ' + version_selector)
            raise

    return cache[version_selector]
