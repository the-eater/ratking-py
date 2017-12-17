from .repository import CachingRepository
from .resolver import Resolver


class Ratking:
    union_repo = None

    def __init__(self):
        self.union_repo = CachingRepository([], [])

    def add_repository(self, repo):
        self.union_repo.add_repository(repo)

    def add_cache_repository(self, repo):
        self.union_repo.add_cache_repository(repo)

    def resolve(self, selectors):
        if not self.union_repo.loaded:
            self.union_repo.load()

        return Resolver(self.union_repo).resolve(selectors)
