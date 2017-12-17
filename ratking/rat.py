from .rat_version import RatVersion
from .rat_selector import RatSelector


class Rat:
    name = None
    version = None
    alias = None
    needs = None
    conflicts = None
    provides = None
    dist_objects = None

    def __repr__(self):
        return 'Rat(name=%s, version=%s)' % (self.name, self.version)

    def __init__(self, name, version, alias=None, needs=None, conflicts=None, provides=None, dist_objects=None):
        self.name = name
        self.version = version
        self.alias = [] if alias is None else alias
        self.needs = [] if needs is None else needs
        self.conflicts = [] if conflicts is None else conflicts
        self.provides = [] if provides is None else provides
        self.dist_objects = [] if dist_objects is None else dist_objects

    @staticmethod
    def from_dict(rat_dict):
        return Rat(
            rat_dict['name'],
            rat_dict['version'] if isinstance(rat_dict['version'], RatVersion) else RatVersion.from_str(
                rat_dict['version']),
            alias=rat_dict.get('alias', None),
            needs=RatSelector.get_collection(rat_dict.get('needs', [])),
            conflicts=rat_dict.get('conflicts', None),
            provides=rat_dict.get('provides', None),
            dist_objects=rat_dict.get('dist_objects', None)
        )
