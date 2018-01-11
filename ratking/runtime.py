import os
import sys
from pprint import pprint
from docopt import docopt
from . import Ratking, RatVersion
from .repository import FlatFileRepository, build_repository
from .version_selector import SelectorParser, VersionSelectorSemantics
from .rat_selector import RatSelector


class Runtime:
    exec = 'rk'
    description = 'ratking\'s all purpose package manager'
    ratking = None
    home = None

    def __init__(self):
        self.home = os.path.expanduser('~/.config/rk')
        self.ratking = Ratking()

    def main(self):
        """
{0} - {1}

Usage:
    {0} install <options> <installable>...
    {0} remove <name>
    {0} list <repo>
    {0} resolve [--missing] [--repo=<repo>]... [--cache-repo=<repo>]...  <installable>...
    {0} version-selector [--test=<version>] <version-selector>
    {0} (-v | -h)

Options:
    -h --help     Show this page
    -v --version  Show version of rk
    --repo=<repo>...  Select repo to use for this action
    --cache-repo=<repo>  Select repo to use to cache all successful queries
        """

        arguments = docopt(str.format(str(self.main.__doc__), self.exec, self.description), version="ratking v0.1")

        if arguments['resolve']:
            self.cmd_resolve(arguments)

        if arguments['version-selector']:
            self.cmd_version_selector(arguments)

    def load_ratking(self, arguments):
        # os.makedirs(self.home, exist_ok=True)
        # local_repo = FlatFileRepository(self.home + "/local_repo.toml", read_only=False)

        # self.ratking.add_repository(local_repo)

        for repo in arguments['--repo']:
            build_repo = build_repository(repo)
            if build_repo is not None:
                self.ratking.add_repository(build_repo)

        for repo in arguments['--cache-repo']:
            build_repo = build_repository(repo)
            if build_repo is not None:
                self.ratking.add_cache_repository(build_repo)

    def cmd_resolve(self, arguments):
        self.load_ratking(arguments)

        selectors = [RatSelector.from_str(selector, manual=True) for selector in arguments['<installable>']]

        rats = {}

        if arguments['--missing']:
            rats = self.ratking.resolve_missing(selectors)
        else:
            rats = self.ratking.resolve(selectors)

        pprint(rats)

    def cmd_version_selector(self, arguments):
        parser = SelectorParser()
        result_selector = parser.parse(arguments['<version-selector>'], semantics=VersionSelectorSemantics())

        print(result_selector)

        if arguments['--test']:
            version = RatVersion.from_str(arguments['--test'])
            print('tested with %s: %s' % (version, result_selector.test(version)))
