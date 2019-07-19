from toml.encoder import TomlEncoder

from .memory_repository import MemoryRepository
from ratking import Rat
import toml
import os


class FlatFileRepository(MemoryRepository):
    file = None
    name = None
    read_only = True

    def __init__(self, file, read_only=True):
        super().__init__({}, None)
        self.file = file
        self.read_only = read_only
        self.name = "Nameless flat-file repo"

    def save(self):
        if self.read_only:
            return

        big_dict = {
            'name': self.name,
            'rats': [rat.to_dict() for versions in self.rats.values() for rat in versions]
        }

        rats_file = open(self.file, 'w+')
        toml.dump(
            big_dict,
            rats_file
        )

        rats_file.close()

    def load(self):
        if not os.path.exists(self.file):
            if not self.read_only:
                self.save()

            self.loaded = None
            return

        rats_file = open(self.file, 'r+')
        repo = toml.load(rats_file)
        rats = repo['rats'] if 'rats' in repo else []
        for rat in rats:
            self.index(Rat.from_dict(rat))

        self.name = repo['name'] if 'name' in repo else "Nameless flat-file repo"
        rats_file.close()
        self.loaded = True
