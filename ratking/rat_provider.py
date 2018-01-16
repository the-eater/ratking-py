from .rat import Rat
from .rat_version import RatVersion
from .rat_selector import RatSelector
from .version_selector.clauses import SimpleClause


class RatProvider(Rat):
    is_virtual = True

    def __init__(self, name, parent, version=RatVersion.bottom):
        super().__init__(name, version=version)
        self.is_virtual = True
        self.needs = [
            RatSelector(name=parent.name, version_selector=SimpleClause('=', parent.version))
        ]

    def __repr__(self):
        return 'RatProvider(name=%s, from=%s)' % (self.name, self.needs[0].__repr__())