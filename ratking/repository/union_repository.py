from .generic_repository import GenericRepository


class UnionRepository(GenericRepository):
    repositories = None

    def __init__(self, repositories=None):
        if repositories is None:
            repositories = []

        self.repositories = repositories

    def load(self):
        for repo in self.repositories:
            repo.load()

        self.loaded = True

    def get_versions(self, name):
        versions = []
        for repo in self.repositories:
            versions.extend(repo.get_versions(name))

        return versions

    def get(self, name, version):
        for repo in self.repositories:
            rat = repo.get(name, version)
            if rat is not None:
                return rat

        return None

    def add_repository(self, repository, load=True):
        if not repository.loaded and load:
            repository.load()

        self.repositories.append(repository)
