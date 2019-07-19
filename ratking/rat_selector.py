from .version_selector import parse_version_selector, clause_from_dict


class RatSelector:
    manual = False
    name = None
    version_selector = None

    def __init__(self, name, version_selector, manual=False):
        self.name = name
        self.version_selector = version_selector
        self.manual = manual

    def matches(self, rat):
        if rat.name != self.name and self.name not in rat.provides:
            return False

        return self.version_selector.test(rat.version)

    def __repr__(self):
        return 'RatSelector("%s", %s)' % (self.name, str(self.version_selector))

    def to_dict(self):
        return {
            'name': self.name,
            'selector': self.version_selector.to_str()
        }

    @staticmethod
    def from_dict(selector_dict):
        return RatSelector(selector_dict['name'], clause_from_dict(selector_dict['selector']))

    @staticmethod
    def from_str(rat_str, manual=False):
        parts = rat_str.split('=', maxsplit=1)

        name = parts[0]
        version_selector = parts[1] if len(parts) > 1 else 'any'

        return RatSelector.from_str_pair(name, version_selector, manual=manual)

    @staticmethod
    def from_str_pair(name, selector, manual=False):
        return RatSelector(
            name,
            parse_version_selector(selector),
            manual=manual
        )

    @staticmethod
    def get_collection(collection):
        if isinstance(collection, dict):
            return [RatSelector.from_str_pair(name, selector) for (name, selector) in collection.items()]

        return [RatSelector.from_str(selector) if isinstance(selector, str) else RatSelector.from_dict(selector) for
                selector in collection]
