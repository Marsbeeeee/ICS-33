def make_repeater(repeatable, count):
    def repeater(value):
        result = value
        for _ in range(count):
            result = repeatable(result)
        return result

    return repeater