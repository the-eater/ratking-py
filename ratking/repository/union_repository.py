from .generic_repository import GenericRepository


class UnionRepository(GenericRepository):
    repositories = []

    def __init__(self, repositories):
        self.repositories = repositories

    def load(self):
        for repo in self.repositories:
            repo.load()

        self.loaded = True

    def get_versions(self, name):
        for repo in self.repositories:
            yield from repo.get_versions(name)

    def get(self, name, version):
        for repo in self.repositories:
            rat = repo.get(name, version)
            if rat is not None:
                return rat

        return None

    def add_repository(self, repository):
        if not repository.loaded:
            repository.load()

        self.repositories.append(repository)
