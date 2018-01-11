class RatFulfillment:
    repo = None
    rat = None
    manual = False

    def __init__(self, rat=None, repo=None, manual=False):
        self.repo = repo if repo is not None else rat.repo
        self.rat = rat
        self.manual = manual

    def __repr__(self):
        return 'RatFulfillment(rat=%s, repo=%s, manual=%s)' % (self.rat, self.repo.name if self.repo is not None else None, self.manual)