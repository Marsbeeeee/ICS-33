def all_substring(s):
    return All_Substring(s)

class All_Substring:
    def __init__(self, s):
        self.s = s
        self.n = len(s)
        self.start = 0
        self.end = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.n == 0 or self.start >= self.n:
            raise StopIteration

        result = self.s[self.start:self.end]

        self.end += 1
        if self.end > self.n:
            self.start += 1
            if self.start < self.n:
                self._end = self.start + 1

        return result
