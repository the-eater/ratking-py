class GenericRepository:
    def load(self):
        pass

    def save(self):
        pass

    def get(self, name, version):
        for rat in self.get_versions(name):
            if rat.version == version:
                return rat

        return None

    def get_versions(self, name):
        return []

    def put(self, rat):
        pass
