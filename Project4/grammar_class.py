class Grammar:
    def __init__(self):
        self.rules = {}

    def add_rule(self, rule):
        self.rules[rule.variable_name] = rule

class Symbol:
    def generate(self, grammar):
        raise NotImplementedError

class Terminal(Symbol):
    def __init__(self, text: str):
        self.text = text

    def generate(self, grammar):
        yield self.text

class Variable(Symbol):
    def __init__(self, name: str):
        self.name = name

    def generate(self, grammar):
        rule = grammar.rules[self.name]
        yield from rule.generate(grammar)

class Option:
    def __init__(self, weight: int, symbols):
        self.weight = weight
        self.symbols = list(symbols)

    def generate(self, grammar):
        for s in self.symbols:
            yield from s.generate(grammar)

class Rule:
    def __init__(self, variable_name: str):
        self.variable_name = variable_name
        self.options = []

    def add_option(self, option):
        self.options.append(option)

    def generate(self, grammar):
        import random
        weights = [opt.weight for opt in self.options]
        chosen = random.choices(self.options, weights=weights, k=1)[0]
        yield from chosen.generate(grammar)