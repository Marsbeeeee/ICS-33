class MultipleSequence:
    def __init__(self, length, multiplier=1):
        if not isinstance(length, int) or length < 0:
            raise ValueError("Length must be a non-negative integer.")
        self._length = length
        self._multiplier = multiplier

    def __len__(self):
        return self._length

    def __bool__(self):
        return self._length > 0

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if index < 0:
            index += self._length
        if index < 0 or index >= self._length:
            raise IndexError("Index out of range.")
        return index * self._multiplier

    def __contains__(self, value):
        if self._length == 0:
            return False
        if self._multiplier == 0:
            return value == 0
        if (value % self._multiplier) != 0:
            return False
        index = value // self._multiplier
        return 0 <= index < self._length

    def __iter__(self):
        for i in range(self._length):
            yield i * self._multiplier

    def __repr__(self):
        if self._multiplier == 1:
            return f"MultipleSequence({self._length})"
        else:
            return f"MultipleSequence({self._length}, {self._multiplier})"
