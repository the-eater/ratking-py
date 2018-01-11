from .rat_fulfillment import RatFulfillment

class Resolver:
    repo = None

    def __init__(self, repo):
        self.repo = repo

    def resolve(self, selectors, current_selection=None):
        if current_selection is None:
            current_selection = {}

        if len(selectors) == 0:
            return current_selection

        selector = selectors[0]

        if selector.name in current_selection:
            if selector.matches(current_selection[selector.name].rat):
                return self.resolve(selectors[1:], current_selection)
            else:
                return None

        rats = self.repo.get_by_selector(selector)

        for rat in rats:
            if rat.version.channel == 'devel':
                continue

            current_selection[selector.name] = RatFulfillment(rat=rat, manual=selector.manual)
            result = self.resolve(selectors[1:] + rat.needs, current_selection)

            if result is not None:
                return result

        return None
