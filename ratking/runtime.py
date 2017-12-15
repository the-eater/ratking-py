import os
import sys
from pprint import pprint
from docopt import docopt
from . import Ratking, RatVersion
from .repository import FlatFileRepository, build_repository
from .version_selector import SelectorParser, VersionSelectorSemantics
from .rat_selector import RatSelector


class Runtime:
    ratking = None
    home = None

    def __init__(self):
        self.home = os.path.expanduser('~/.config/rk')

    def main(self):
        """
{0} - ratking's all purpose package manager

Usage:
    {0} install [--repo=<repo>] <installable>...
    {0} remove <name>
    {0} list-rats <repo>
    {0} resolve [--repo=<repo>] <installable>...
    {0} version-selector [--test=<version>] <version-selector>
    {0} (-v | -h)

Options:
    -h --help     Show this page
    -v --version  Show version of rk
    --repo=<repo> -r=<repo>    Select repo to use for this action
        """
        arg0 = 'rk'

        # if sys.argv[0] != arg0:
        #    arg0 = 'python3 -m ratking'

        arguments = docopt(str.format(str(self.main.__doc__), arg0), version="ratking v0.1")

        if arguments['resolve']:
            self.cmd_resolve(arguments)

        if arguments['version-selector']:
            self.cmd_version_selector(arguments)

    def load_ratking(self, arguments):
        self.ratking = Ratking()

        os.makedirs(self.home, exist_ok=True)
        local_repo = FlatFileRepository(self.home + "/local_repo.toml", read_only=False)

        self.ratking.add_repository(local_repo)

        if arguments['--repo']:
            repo = build_repository(arguments['--repo'])
            if repo is not None:
                self.ratking.add_repository(repo)

    def cmd_resolve(self, arguments):
        self.load_ratking(arguments)

        rats = self.ratking.resolve([RatSelector.from_str(selector) for selector in arguments['<installable>']])

        pprint(rats)

    def cmd_version_selector(self, arguments):
        parser = SelectorParser()
        result_selector = parser.parse(arguments['<version-selector>'], semantics=VersionSelectorSemantics())

        print(result_selector)

        if arguments['--test']:
            version = RatVersion(arguments['--test'])
            print('tested with %s: %s' % (version, result_selector.test(version)))
