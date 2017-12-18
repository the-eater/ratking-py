from .git_dist_object import GitDistObject
from .zip_dist_object import ZipDistObject


def dist_object_from_dict(dist_dict):
    dist_type = dist_dict['type']
    if dist_type == 'zip':
        return ZipDistObject(dist_dict['path'])

    if dist_type == 'git':
        return GitDistObject(dist_dict['uri'])
