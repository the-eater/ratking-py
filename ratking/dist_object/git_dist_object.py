from .generic_dist_object import GenericDistObject


class GitDistObject(GenericDistObject):
    is_tree = True
    uri = None

    def __init__(self, uri):
        self.uri = uri
