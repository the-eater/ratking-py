from .flat_file_repository import FlatFileRepository


def build_repository(url):
    parts = url.split(':', 2)

    if len(parts) != 2:
        return None

    (repo_type, path) = parts

    if repo_type == 'flat':
        return FlatFileRepository(path)

    return None
