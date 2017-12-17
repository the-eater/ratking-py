from .version_selector import parse_version_selector


class RatSelector:
    name = None
    version_selector = None

    def __init__(self, name, version_selector):
        self.name = name
        self.version_selector = version_selector

    def matches(self, rat):
        if rat.name != self.name:
            return False

        return self.version_selector.test(rat.version)

    def __repr__(self):
        return self.name + '=' + str(self.version_selector)

    @staticmethod
    def from_str(rat_str):
        parts = rat_str.split('=', maxsplit=1)

        name = parts[0]
        version_selector = parts[1] if len(parts) > 1 else 'any'

        return RatSelector.from_str_pair(name, version_selector)


    @staticmethod
    def from_str_pair(name, selector):
        return RatSelector(
            name,
            parse_version_selector(selector)
        )

    @staticmethod
    def get_collection(collection):
        if isinstance(collection, dict):
            return [RatSelector.from_str_pair(name, selector) for (name, selector) in collection.items()]

        return [RatSelector.from_str(selector) for selector in collection]