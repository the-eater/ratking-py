from .generic_repository import GenericRepository
from .. import Rat, RatVersion, RatSelector, RatProvider
from ..version_selector.clauses import SimpleClause

class MemoryRepository(GenericRepository):
    name = None
    rats = None

    def __init__(self, rats, name='In-memory repo'):
        self.rats = rats
        self.name = name

    def index_name(self, rat, name):
        if name not in self.rats:
            self.rats[name] = []

        self.rats[name].append(rat)

    def index(self, rat):
        self.index_name(rat, rat.name)

        for provide in rat.provides:
            self.index_name(provide, provide.name)

    def get(self, name, version):
        if name not in self.rats:
            return None

        for rat in self.rats[name]:
            if rat.name == name and rat.version == version:
                return rat

        return None

    def get_versions(self, name):
        return self.rats[name] if name in self.rats else []

    def put(self, rat):
        self.index(rat)