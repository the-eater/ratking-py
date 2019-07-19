from .flat_file_repository import FlatFileRepository
from .composer_repository import ComposerRepository


def build_repository(url):
    parts = url.split(':', maxsplit=1)

    if len(parts) != 2:
        return None

    (repo_type, path) = parts

    if repo_type == 'flat':
        parts = path.split(':', maxsplit=1)
        file = path
        ro = False
        if len(parts) == 2:
            file = parts[1]
            ro = parts[0] == 'ro'

        return FlatFileRepository(file=file, read_only=ro)

    if repo_type == 'composer':
        from .composer_repository import ComposerRepository
        return ComposerRepository(path)

    if repo_type == 'rk':
        from .ratking_repository import RatkingRepository
        return RatkingRepository(path)

    return None
