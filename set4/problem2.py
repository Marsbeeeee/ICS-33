def generate_range(*args):
    if len(args) == 1:
        start, stop, step = 0, args[0], 1
    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1
    elif len(args) == 3:
        start, stop, step = args
    else:
        raise TypeError("generate_range expected 1 to 3 positional arguments")

    if step == 0:
        raise ValueError("step cannot be zero")

    current = start
    if step > 0:
        while current < stop:
            yield current
            current += step
    else:
        while current > stop:
            yield current
            current += step

def no_fizz_without_buzz(start):
    n = start
    while True:
        if (n % 3 == 0 and n % 5 == 0) or (n % 3 != 0 and n % 5 != 0):
            yield n

        n += 1

def cartesian_product(*iterables):
    if len(iterables) == 0:
        return

    lists = [list(it) for it in iterables]

    for lst in lists:
        if len(lst) == 0:
            return

    indices = [0] * len(lists)

    while True:
        yield tuple(lists[i][indices[i]] for i in range(len(lists)))

        pos = len(indices) - 1
        while pos >= 0:
            indices[pos] += 1
            if indices[pos] < len(lists[pos]):
                break
            indices[pos] = 0
            pos -= 1

        if pos < 0:
            return
