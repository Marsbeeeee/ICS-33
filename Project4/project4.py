# project4.py
#
# ICS 33 Fall 2025
# Project 4: Still Looking for Something

from grammar_reader import read_file


def main() -> None:
    path = input().strip()
    count = int(input().strip())
    start_var = input().strip()

    grammar = read_file(path)

    for _ in range(count):
        words = grammar.rules[start_var].generate(grammar)
        print(" ".join(words))


if __name__ == '__main__':
    main()
