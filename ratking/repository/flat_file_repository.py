from .memory_repository import MemoryRepository
import toml


class FlatFileRepository(MemoryRepository):
    file = None
    name = None
    read_only = True
    rats = []

    def __init__(self, file, read_only=True):
        super().__init__([], None)
        self.file = file
        self.read_only = read_only

    def save(self):
        if self.read_only:
            return

        rats_file = open(self.file, 'w+')
        toml.dump(
            {
                'rats': self.rats,
                'name': self.name
            },
            rats_file
        )

        rats_file.close()

    def load(self):
        rats_file = open(self.file, 'r+')
        repo = toml.load(rats_file)
        self.rats = repo.rats
        self.name = repo.name
        rats_file.close()
        self.loaded = True
