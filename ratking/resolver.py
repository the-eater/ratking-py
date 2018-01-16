from .rat_fulfillment import RatFulfillment


class Resolver:
    @staticmethod
    def resolve(selectors, repo, current_selection=None, local_repo=None):
        if current_selection is None:
            current_selection = {}

        if len(selectors) == 0:
            return current_selection

        selector = selectors[0]

        if selector.name in current_selection:
            if selector.matches(current_selection[selector.name].rat):
                return Resolver.resolve(selectors[1:], repo, current_selection, local_repo=local_repo)
            else:
                return None

        if local_repo is not None:
            rats = local_repo.get_by_selector(selector)
            result = Resolver.resolve_from_selection(rats, selector, selectors, repo, current_selection, local_repo=local_repo)
            if result is not None:
                return result

        rats = repo.get_by_selector(selector)

        return Resolver.resolve_from_selection(rats, selector, selectors, repo, current_selection, local_repo=local_repo)

    @staticmethod
    def resolve_from_selection(rats, selector, selectors, repo, current_selection=None, local_repo=None):
        current_selection = {} if current_selection is None else current_selection

        for rat in rats:
            if rat.version.channel == 'devel':
                continue

            current_selection[selector.name] = RatFulfillment(rat=rat, manual=selector.manual)
            result = Resolver.resolve(selectors[1:] + rat.needs, repo, current_selection, local_repo=local_repo)

            if result is not None:
                return result

        return None
