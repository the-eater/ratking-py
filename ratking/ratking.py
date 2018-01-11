from .repository import CachingRepository, MemoryRepository
from .resolver import Resolver
from .rat_provider import RatProvider


class Ratking:
    remote_repo = None
    local_repo = None

    def __init__(self, local_repo=None):
        self.local_repo = local_repo if local_repo is not None else MemoryRepository(rats=[])
        self.remote_repo = CachingRepository([self.local_repo], [])

    def add_repository(self, repo, load=True):
        self.remote_repo.add_repository(repo, load=load)

    def add_cache_repository(self, repo):
        self.remote_repo.add_cache_repository(repo)

    def resolve(self, selectors):
        if not self.remote_repo.loaded:
            self.remote_repo.load()

        return Resolver(self.remote_repo).resolve(selectors)

    def resolve_missing(self, selectors):
        fulfillments = self.resolve(selectors)

        if fulfillments is None:
            return None

        missing = {}

        for key, fulfillment in fulfillments.items():
            rat = fulfillment.rat

            if isinstance(rat, RatProvider):
                continue

            if fulfillment.repo is self.local_repo or self.local_repo.get(rat.name, rat.version):
                continue

            missing[key] = fulfillment

        return missing