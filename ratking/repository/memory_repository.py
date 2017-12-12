from .generic_repository import GenericRepository
import toml


class MemoryRepository(GenericRepository):
    name = None
    rats = []

    def __init__(self, rats, name='In-memory repo'):
        self.rats = rats
        self.name = name

    def get(self, name, version):
        for rat in self.rats:
            if rat.name == name and rat.version == version:
                return rat

        return None

    def get_versions(self, name):
        for rat in self.rats:
            if rat.name == name:
                yield rat
