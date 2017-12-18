from .generic_dist_object import GenericDistObject


class GitDistObject(GenericDistObject):
    is_tree = True
    uri = None

    def __init__(self, uri):
        self.uri = uri

    def to_json(self):
        return {
            'type': 'git',
            'uri': self.uri
        }