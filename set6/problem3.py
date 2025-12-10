def sequential_search(collection, search_key):
    try:
        iterator = iter(collection)
        current_element = next(iterator)
        if current_element == search_key:
            return True
        remaining = tuple(iterator)  # Convert remaining elements to tuple for recursion
        return sequential_search(remaining, search_key)
    except StopIteration:
        return False


# What is the closest-fit O-notation that describes how much time is required to search a collection containing n elements?
# O(n)

# What is the closest-fit O-notation that describes how much additional memory is required to search a collection containing n elements?
# O(n)

# How, if at all, would your closest-fit O-notations change if Python performed tail call elimination?
# Time: O(n), Memory: O(1)


def binary_search(collection, search_key, low = 0, high = None):
    if high is None:
        high = len(collection) - 1

    if low > high:
        return False

    mid = (low + high) // 2
    current_element = collection[mid]

    if current_element == search_key:
        return True
    elif current_element < search_key:
        return binary_search(collection, search_key, mid + 1, high)
    else:
        return binary_search(collection, search_key, low, mid - 1)

# What is the closest-fit O-notation that describes how much time is required to search a collection containing n elements?
# O(log n)

# What is the closest-fit O-notation that describes how much additional memory is required to search a collection containing n elements?
# O(log n)

# How, if at all, would your closest-fit O-notations change if Python performed tail call elimination?
# Time: O(log n), Memory: O(1)