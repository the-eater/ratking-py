from .rat_version import RatVersion
from .rat_selector import RatSelector


class Rat:
    name = None
    version = None
    alias = None
    needs = None
    conflicts = None
    provides = None

    def __repr__(self):
        return 'Rat(name=%s, version=%s)' % (self.name, self.version)

    def __init__(self, name, version, alias=None, needs=None, conflicts=None, provides=None):
        self.name = name
        self.version = version
        self.alias = [] if alias is None else alias
        self.needs = [] if needs is None else needs
        self.conflicts = [] if conflicts is None else conflicts
        self.provides = [] if provides is None else provides

    @staticmethod
    def from_dict(rat_dict):
        return Rat(
            rat_dict['name'],
            RatVersion(rat_dict['version']),
            alias=rat_dict.get('alias', None),
            needs=RatSelector.get_collection(rat_dict.get('needs', [])),
            conflicts=rat_dict.get('conflicts', None),
            provides=rat_dict.get('provides', None),
        )
