from .rat_version import RatVersion
from .rat_selector import RatSelector
from .dist_object import dist_object_from_dict
import json

class Rat:
    name = None
    version = None
    alias = None
    needs = None
    conflicts = None
    provides = None
    dist_objects = None
    repo = None
    is_virtual = False

    def __repr__(self):
        return 'Rat(name=%s, version=%s)' % (self.name, self.version.__repr__())

    def __init__(self, name, version, alias=None, needs=None, conflicts=None, provides=None, dist_objects=None, repo=None):
        self.name = name
        self.version = version
        self.alias = alias
        self.needs = [] if needs is None else needs
        self.conflicts = [] if conflicts is None else conflicts
        self.provides = [] if provides is None else provides
        self.dist_objects = [] if dist_objects is None else dist_objects
        self.repo = repo

    @staticmethod
    def from_dict(rat_dict, repo=None):
        return Rat(
            rat_dict['name'],
            rat_dict['version'] if isinstance(rat_dict['version'], RatVersion) else RatVersion.from_str(
                rat_dict['version']),
            alias=rat_dict.get('alias', None),
            needs=RatSelector.get_collection(rat_dict.get('needs', [])),
            conflicts=rat_dict.get('conflicts', None),
            provides=rat_dict.get('provides', None),
            dist_objects=[dist_object_from_dict(obj) if isinstance(obj, dict) else obj for obj in rat_dict.get('dist_objects', None)],
            repo=repo
        )

    def to_dict(self):
        needs = {}

        for need in self.needs:
            needs[need.name] = need.version_selector.to_str()

        return {
            'name': self.name,
            'version': str(self.version),
            'alias': self.alias,
            'needs': needs,
            'conflicts': self.conflicts,
            'provides': self.provides,
            'dist_objects': [dist.to_dict() for dist in self.dist_objects]
        }

    def to_json(self):
        return json.dumps(self.to_dict())