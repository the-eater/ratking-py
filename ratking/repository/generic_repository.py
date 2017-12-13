class GenericRepository:
    loaded = False

    def load(self):
        self.loaded = True

    def save(self):
        pass

    def get(self, name, version):
        for rat in self.get_versions(name):
            if rat.version == version:
                return rat

        return None

    def get_versions(self, name):
        return []

    def get_latest(self, name):
        rats = self.get_versions(name)
        if len(rats) == 0:
            return None

        latest_rat = None

        for rat in rats:
            if latest_rat is None:
                latest_rat = rat
                continue

            if latest_rat.version < rat.version:
                latest_rat = rat

        return latest_rat

    def get_by_selector(self, selector):
        return [rat for rat in self.get_versions(selector.name) if selector.matches(rat)]

    def put(self, rat):
        pass
