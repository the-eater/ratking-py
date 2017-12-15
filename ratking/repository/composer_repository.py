from .generic_repository import GenericRepository
from ..rat import Rat
from ..rat_version import RatVersion
import requests


class ComposerRepository(GenericRepository):
    url = None

    cache = None

    def __init__(self, url='https://packagist.org/'):
        self.url = url
        self.cache = {}

    def get_versions(self, name):
        if name in self.cache:
            return self.cache[name]

        resp = requests.get(self.url + '/p/' + name + '.json')

        if resp.status_code != 200:
            return []

        versions = resp.json().get('packages', {name: {}}).get(name, {}).values()

        rats = [
            Rat.from_dict({
                'name': version.get('name', name),
                'version': version.get('version'),
                'needs': dict(
                    [(need_name, need_selector) for (need_name, need_selector) in version.get('require', {}).items() if
                     '/' in need_name])
            }) for version in versions if '-dev' not in version.get('version')]

        rats.sort(key=lambda item: item.version, reverse=True)

        self.cache[name] = rats

        return rats
