class Collection:
    def __init__(self, values):
        self._values = values

    def __eq__(self, other):
        if not isinstance(other, Collection):
            return NotImplemented
        for a, b in zip(self._values, other._values):
            if a != b:
                return False
        try:
            next(iter(self._values))
            next(iter(other._values))
        except StopIteration:
            return True
        return all(False for _ in self._values) and all(False for _ in other._values)  # double-check exhaustion

    def __lt__(self, other):
        if not isinstance(other, Collection):
            return NotImplemented
        return tuple(self._values) < tuple(other._values)

    def __le__(self, other):
        if not isinstance(other, Collection):
            return NotImplemented
        return tuple(self._values) <= tuple(other._values)

    def __gt__(self, other):
        if not isinstance(other, Collection):
            return NotImplemented
        return tuple(self._values) > tuple(other._values)

    def __ge__(self, other):
        if not isinstance(other, Collection):
            return NotImplemented
        return tuple(self._values) >= tuple(other._values)

    def __ne__(self, other):
        eq = self.__eq__(other)
        if eq is NotImplemented:
            return NotImplemented
        return not eq
