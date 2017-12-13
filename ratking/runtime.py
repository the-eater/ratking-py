import os
from docopt import docopt
from . import Ratking
from .repository import FlatFileRepository
from .version_selector import SelectorParser, VersionSelectorSemantics

class Runtime:
    ratking = None
    home = None

    def __init__(self):
        self.home = os.path.expanduser('~/.config/rk')

    def main(self):
        """
rk - ratking's all purpose package manager

Usage:
    rk install [--repo <repo>] <installable>...
    rk remove <name>
    rk list-rats <repo>
    rk resolve [--repo <repo>] <installable>...
    rk version-selector <version-selector>
    rk (-v | -h)

Options:
    -h --help     Show this page
    -v --version  Show version of rk
    --repo -r     Select repo to use for this action
        """
        arguments = docopt(str(self.main.__doc__), version="ratking v0.1")

        if arguments['resolve']:
            self.cmd_resolve(arguments)

        if arguments['version-selector']:
            self.cmd_version_selector(arguments)

    def load_ratking(self):
        self.ratking = Ratking()

        os.makedirs(self.home, exist_ok=True)
        local_repo = FlatFileRepository(self.home + "/local_repo.toml", read_only=False)

        self.ratking.add_repository(local_repo)

    def cmd_resolve(self, arguments):
        self.load_ratking()

        rats = self.ratking.resolve(hints=arguments['<installable>'])

        print(rats)

    def cmd_version_selector(self, arguments):
        x = SelectorParser()
        print(x.parse(arguments['<version-selector>'], semantics=VersionSelectorSemantics()))