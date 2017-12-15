class RatVersion:
    known_seperators = ['-', '_', '.', '@']

    pre_release = ['beta', 'alpha', 'rc', 'pre-release', 'pre', 'prelease', 'dev']

    parts = None
    separators = None

    def __init__(self, version_str):
        self.parts = []
        self.separators = []
        version_str = str(version_str)

        if version_str[0] == 'v':
            version_str = version_str[1:]

        part = ""
        for c in version_str:
            if c in self.known_seperators:
                self.parts.append(part)
                self.separators.append(c)
                part = ""
                continue

            if part != "" and c.isdigit() != part[-1].isdigit():
                self.parts.append(part)
                self.separators.append("")
                part = c
                continue

            part += c

        if part != '':
            self.parts.append(part)

        if len(self.parts) > len(self.separators):
            self.separators.append('')

    def __cmp__(self, other):
        for i in range(0, max(len(self.parts), len(other.parts))):
            left = self.parts[i] if i < len(self.parts) else 0
            right = other.parts[i] if i < len(other.parts) else 0

            if (left in self.pre_release) != (right in self.pre_release):
                return 1 if right in self.pre_release else -1

            if left == '*':
                for j in range(i, len(other.parts)):
                    if other.parts[j] in self.pre_release:
                        return 1

                return 0

            if right == '*':
                for j in range(i, len(self.parts)):
                    if self.parts[j] in self.pre_release:
                        return -1

                return 0

            if (isinstance(left, int) or (isinstance(left, str) and left.isdigit())) and \
                    (isinstance(right, int) or (isinstance(right, str) and right.isdigit())):
                left = int(left)
                right = int(right)

            if isinstance(left, int) != isinstance(right, int):
                left = str(left)
                right = str(right)

            if left != right:
                return 1 if left > right else -1

        return 0

    def strip(self, length=1):
        return 'v' + ''.join([x + z for x, z in zip(self.parts[:length], self.separators[:length])])

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __repr__(self):
        return 'v' + ''.join([x + z for x, z in zip(self.parts, self.separators)])

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0
