from ratking import RatVersion

import unittest


class TestVersion(unittest.TestCase):
    def test_order(self):
        """
        2_3+failed-edition
        1.0.0.1
        1_1
        1.0.0.0.0
        1.0.0-beta
        2_1@devel
        @devel
        """
        versions = [str(version).strip() for version in str(self.test_order.__doc__).strip().split("\n") if str(version).strip()[0] != '#']

        result = versions[:]

        result.sort(key=RatVersion.from_str, reverse=True)

        self.assertSequenceEqual(versions, result)


if __name__ == '__main__':
    unittest.main()
