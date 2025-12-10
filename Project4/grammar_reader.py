from grammar_class import *


def read_file(file_path):
    grammar = Grammar()
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f]

    i = 0
    while i < len(lines):

        if lines[i].strip() == '':
            i += 1
            continue

        if lines[i] == '{':
            i += 1
            var_name = lines[i]
            rule = Rule(var_name)
            i += 1

            while i < len(lines) and lines[i].strip() != '}':

                if lines[i].strip() == '':
                    i += 1
                    continue

                parts = lines[i].split()
                weight = int(parts[0])
                symbols = []

                for part in parts[1:]:
                    if part.startswith('[') and part.endswith(']'):
                        symbols.append(Variable(part[1:-1]))
                    else:
                        symbols.append(Terminal(part))

                rule.add_option(Option(weight, symbols))
                i += 1

            grammar.add_rule(rule)

        i += 1

    return grammar
