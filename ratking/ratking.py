from .repository import UnionRepository


class Ratking:
    repositories = []
    union_repo = UnionRepository([])

    def add_repository(self, repo):
        self.union_repo.add_repository(repo)

    def resolve(self, hints=None):
        pass
