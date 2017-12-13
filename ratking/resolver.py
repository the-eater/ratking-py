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

        if current_selection[selector.name] is not None:
            if selector.matches(current_selection[selector.name]):
                return self.resolve(selector[1:], current_selection)
            else:
                return None

        rats = self.repo.get_by_selector(selector)

        for rat in rats:
            current_selection[rat.name] = rat
            result = self.resolve(selector[1:] + rat.needs, current_selection)

            if result is not None:
                return result

        return None
