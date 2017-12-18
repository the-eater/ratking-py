from .generic_dist_object import GenericDistObject


class ZipDistObject(GenericDistObject):
    is_tree = True
    path = None

    def __init__(self, path):
        self.path = path

    def to_json(self):
        return {
            'type': 'zip',
            'path': self.path
        }