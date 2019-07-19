from .union_repository import UnionRepository


class CachingRepository(UnionRepository):
    cache_repositories = None

    def __init__(self, repositories=None, cache_repositories=None):
        self.repositories = [] if repositories is None else repositories
        self.cache_repositories = [] if cache_repositories is None else cache_repositories

    def load(self):
        for repo in self.repositories:
            repo.load()

        for repo in self.cache_repositories:
            repo.load()

    def add_cache_repository(self, repository):
        self.cache_repositories.append(repository)

    def get_versions(self, name):
        for cache_repo in self.cache_repositories:
            rats = cache_repo.get_versions(name)

            if len(rats) > 0:
                return rats

        versions = super().get_versions(name)

        for version in versions:
            self.put(version)

        return versions

    def get(self, name, version):
        for cache_repo in self.cache_repositories:
            rat = cache_repo.get(name, version)

            if rat is not None:
                return rat

        rat = super().get(name, version)
        if rat is not None:
            self.put(rat)

        return rat

    def save(self):
        for repo in self.cache_repositories:
            repo.save()

    def put(self, rat):
        for repo in self.cache_repositories:
            repo.put(rat)
