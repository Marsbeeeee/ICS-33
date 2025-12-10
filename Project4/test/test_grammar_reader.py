import unittest
from grammar_reader import read_file
from grammar_class import Grammar, Rule, Terminal, Variable, Option


def write_test_file(content: str, filename: str = "test_grammar_input.txt") -> str:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

class TestGrammarReader(unittest.TestCase):
    def test_read_file_empty_file_returns_empty_grammar(self):
        path = write_test_file("", "test_grammar_empty.txt")
        grammar = read_file(path)
        self.assertIsInstance(grammar, Grammar)
        self.assertEqual(grammar.rules, {})

    def test_read_file_parses_multiple_rules_with_blanks_and_mixed_symbols(self):
        content = """
{
S
1 hello [NAME]
2 bye world
}

{
NAME
1 Alice
1 Bob
}
"""
        path = write_test_file(content, "test_grammar_normal.txt")
        grammar = read_file(path)

        self.assertIn("S", grammar.rules)
        self.assertIn("NAME", grammar.rules)

        rule_s = grammar.rules["S"]
        rule_name = grammar.rules["NAME"]

        self.assertEqual(len(rule_s.options), 2)
        opt1, opt2 = rule_s.options

        self.assertEqual(opt1.weight, 1)
        self.assertEqual(opt1.symbols[0].text, "hello")
        self.assertIsInstance(opt1.symbols[1], Variable)
        self.assertEqual(opt1.symbols[1].name, "NAME")

        self.assertEqual(opt2.weight, 2)
        self.assertEqual(opt2.symbols[0].text, "bye")
        self.assertEqual(opt2.symbols[1].text, "world")

        self.assertEqual(len(rule_name.options), 2)
        for opt in rule_name.options:
            self.assertEqual(opt.weight, 1)
            self.assertIn(opt.symbols[0].text, {"Alice", "Bob"})

    def test_read_file_invalid_weight_raises_value_error(self):
        content = """{
S
abc hello
}
"""
        path = write_test_file(content, "test_grammar_invalid_weight.txt")
        with self.assertRaises(ValueError):
            read_file(path)

    def test_read_file_missing_var_name_after_brace_raises_index_error(self):
        content = "{\n"
        path = write_test_file(content, "test_grammar_missing_name.txt")
        with self.assertRaises(IndexError):
            read_file(path)


if __name__ == "__main__":
    unittest.main()