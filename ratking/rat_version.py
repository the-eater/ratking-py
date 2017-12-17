from pprint import pprint


class RatVersion:
    cache = {}
    separators = ['-', '.', '_', '@', '+']

    revision_separator = '_'
    channel_separator = '@'
    metadata_separator = '+'

    parts = None
    channel = 'stable'
    metadata = None
    is_pre_release = False

    def __init__(self):
        self.parts = []

    @staticmethod
    def from_str(version_str):
        if version_str in RatVersion.cache:
            return RatVersion.cache[version_str]

        version_obj = RatVersion()

        current_part = RatVersionPart(parts=[], separator=".", is_start=True)
        part = ""

        is_number = None

        if version_str[0] == 'v':
            version_str = version_str[1:]

        for c in version_str:
            if (current_part.separator in [RatVersion.metadata_separator, RatVersion.channel_separator] \
                or not current_part.is_numeric) \
                    and c not in [RatVersion.channel_separator, RatVersion.metadata_separator]:
                part += c
                continue

            if c in RatVersion.separators:
                if part != "":
                    current_part.parts.append(int(part) if is_number else part)

                if (current_part.separator is None or current_part.separator == c) \
                        and c not in [RatVersion.revision_separator, RatVersion.channel_separator,
                                      RatVersion.metadata_separator]:
                    current_part.separator = c
                else:
                    version_obj.parts.append(current_part)
                    current_part = RatVersionPart(parts=[], separator=c, is_start=False)
                    is_number = None

                part = ""
                continue

            c_is_digit = str(c).isdigit()

            if c == '*' or is_number is None or is_number == c_is_digit:
                if c != '*':
                    current_part.is_numeric = c_is_digit

                part += c
            else:
                current_part.parts.append(int(part) if is_number and part != '*' and part != '' else part)
                version_obj.parts.append(current_part)
                current_part = RatVersionPart(parts=[], separator=".", is_start=True, is_numeric=c_is_digit)
                part = c

            is_number = c_is_digit

        if part != "":
            current_part.parts.append(int(part) if is_number else part)

        if current_part.separator == RatVersion.channel_separator:
            version_obj.channel = current_part.parts[0]

        elif current_part.separator == RatVersion.metadata_separator:
            version_obj.metadata = current_part.parts[0]
        else:
            version_obj.parts.append(current_part)

        if not version_obj.parts[0].is_numeric:
            version_obj.channel = 'devel'

        if version_obj.channel != 'stable':
            version_obj.is_pre_release = True

        RatVersion.cache[version_str] = version_obj

        return version_obj

    def __repr__(self):
        return 'RatVersion(parts=%s,channel="%s")' % (self.parts, self.channel)

    def __str__(self):
        return ''.join([str(part) for part in self.parts])

    def __cmp__(self, other):
        if self.is_pre_release != other.is_pre_release:
            return 1 if other.is_pre_release else -1

        for (left, right) in zip(self.parts, other.parts):
            res = left.__cmp__(right)

            if res != 0:
                return res

        if len(other.parts) == len(self.parts):
            return 0

        min_len = min(
            len(self.parts),
            len(other.parts)
        )

        left = [part for part in self.parts[min_len:] if not part.is_numeric]
        right = [part for part in other.parts[min_len:] if not part.is_numeric]

        if len(left) > 0:
            return -1

        if len(right) > 0:
            return 1

        if len(self.parts) > len(other.parts):
            return 1

        return -1

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0


class RatVersionPart:
    is_start = False
    is_numeric = None
    separator = "."
    parts = None

    def __init__(self, parts, separator=".", is_start=False, is_numeric=True):
        self.parts = parts
        self.separator = "." if separator is None else separator
        self.is_start = is_start
        self.is_numeric = is_numeric

    def __repr__(self):
        return 'RatVersionPart(parts=%s, separator="%s", is_start=%s, is_numeric=%s)' % (
            self.parts, self.separator, self.is_start, self.is_numeric)

    def __str__(self):
        return (self.separator if not self.is_start else '') + self.separator.join([str(part) for part in self.parts])

    def __cmp__(self, other):
        if self.is_numeric != other.is_numeric:
            return 1 if self.is_numeric else -1

        if self.parts == other.parts:
            return 0

        for (left, right) in zip(self.parts, other.parts):
            if left == '*' or right == '*':
                return 0

            if left != right:
                return 1 if left > right else -1

        min_len = min(len(self.parts), len(other.parts))

        left = [v for v in self.parts[min_len:] if v != 0]
        right = [v for v in other.parts[min_len:] if v != 0]

        left = left[:left.index('*') if '*' in left else len(left)]
        right = right[:right.index('*') if '*' in right else len(right)]

        if left != right:
            return 1 if left > right else -1

        return 0
