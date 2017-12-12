from docopt import docopt


class Runtime:
    cache_repo = None

    def run(self):
        """
rk - ratking's all purpose package manager

Usage:
    rk install [--repo <repo>] <installable>
    rk remove <name>
    rk list-repo <repo>
    rk resolve [--repo <repo>] <installable>
    rk (-v | -h)

Options:
    -h --help     Show this page
    -v --version  Show version of rk
    --repo -r     Select repo to use for this action
        """
        arguments = docopt(str(self.run.__doc__), version="ratking v0.1")
