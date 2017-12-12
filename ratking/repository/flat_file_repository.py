from .generic_repository import GenericRepository
import toml


class FlatFileRepository(GenericRepository):
    file = None
    name = None
    read_only = True
    rats = []

    def __init__(self, file, read_only=True):
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

    def get(self, name, version):
        for rat in self.rats:
            if rat.name == name and rat.version == version:
                return rat

        return None

    def get_versions(self, name):
        for rat in self.rats:
            if rat.name == name:
                yield rat
