from .repository import UnionRepository
from .resolver import Resolver


class Ratking:
    repositories = None
    union_repo = None

    def __init__(self):
        self.repositories = []
        self.union_repo = UnionRepository([])

    def add_repository(self, repo):
        self.union_repo.add_repository(repo)

    def resolve(self, selectors):
        return Resolver(self.union_repo).resolve(selectors)
