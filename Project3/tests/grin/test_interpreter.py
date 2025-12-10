import unittest
from grin.parser_builder import parse_program
from grin import interpreter as grin_interpreter

class InterpreterTest(unittest.TestCase):
    def run_program(self, lines, inputs=None):
        inputs = inputs or []
        it = iter(inputs)
        output = []
        old_input = __builtins__['input']
        old_print = __builtins__['print']
        __builtins__['input'] = lambda prompt=None: next(it)
        __builtins__['print'] = lambda *args, **kwargs: output.append(" ".join(str(a) for a in args))
        try:
            interp = parse_program(lines)
            interp.execute()
        finally:
            __builtins__['input'] = old_input
            __builtins__['print'] = old_print
        return output

    def test_let_print(self):
        self.assertEqual(
            self.run_program(["LET X 5", "PRINT X", "END", "."]),
            ["5"]
        )

    def test_arithmetic(self):
        prog = ["LET A 10", "ADD A 5", "SUB A 3", "MULT A 2", "DIV A 4", "PRINT A", "END", "."]
        self.assertEqual(self.run_program(prog), ["6"])

    def test_goto_absolute(self):
        prog = ["LET X 9", "GOTO 2", "LET X 0", "PRINT X", "END", "."]
        self.assertEqual(self.run_program(prog), ["9"])

    def test_goto_label(self):
        prog = ["LET N 3", "GOTO LOOP", "PRINT 0", "LOOP: PRINT N", "END", "."]
        self.assertEqual(self.run_program(prog), ["3"])

    def test_gosub_return(self):
        prog = [
            "LET A 2",
            "GOSUB HH",
            "PRINT A",
            "END",
            "HH: LET A 5",
            "RETURN",
            "."
        ]
        self.assertEqual(self.run_program(prog), ["5"])

    def test_conditional_gosub(self):
        prog = [
            "LET A 2",
            "GOSUB HH IF A = 3",
            "PRINT A",
            "END",
            "HH: LET A 99",
            "RETURN",
            "."
        ]
        self.assertEqual(self.run_program(prog), ["2"])

    def test_innum_instr(self):
        prog = ["INNUM X", "INSTR S", "PRINT X", "PRINT S", "END", "."]
        out = self.run_program(prog, inputs = ["123", "\"hi\""])
        self.assertEqual(out, ["123", "hi"])

    def test_end(self):
        prog = ["PRINT 8", "END", "PRINT 9", "."]
        self.assertEqual(self.run_program(prog), ["8"])

    def test_simple_let_print(self):
        prog = [
            "LET X 7",
            "PRINT X",
            "."
        ]
        self.assertEqual(self.run_program(prog), ["7"])

    def test_conditional_gosub_false(self):
        prog = [
            "LET A 2",
            "GOSUB HH IF A = 3",
            "PRINT A",
            "END",
            "HH: LET A 99",
            "RETURN",
            "."
        ]
        self.assertEqual(self.run_program(prog), ["2"])

    def test_add_sub_print(self):
        prog = [
            "LET X 5",
            "LET Y 2",
            "ADD X Y",
            "PRINT X",
            "SUB X 3",
            "PRINT X",
            "."
        ]
        self.assertEqual(self.run_program(prog), ["7", "4"])

    def test_mult_div_print(self):
        prog = [
            "LET X 8",
            "MULT X 4",
            "PRINT X",
            "DIV X 2",
            "PRINT X",
            "."
        ]
        self.assertEqual(self.run_program(prog), ["32", "16"])

    def test_goto_conditional(self):
        prog = [
            "LET Z 1",
            "GOTO \"SKIP\" IF Z = 2",
            "PRINT Z",
            ".",
            "SKIP: PRINT 999",
            "END"
        ]
        self.assertEqual(self.run_program(prog), ["1"])

    def test_goto_nonexistent_label(self):
        prog = [
            "GOTO NO_SUCH_LABEL",
            "PRINT 100",
            "."
        ]
        with self.assertRaises(Exception):
            self.run_program(prog)

    def test_instr_invalid_input_exception(self):
        class Weird:
            def strip(self):
                return 123
        prog = [
            "INSTR S",
            ".",
        ]
        with self.assertRaises(Exception):
            self.run_program(prog, inputs = [Weird()])

    def test_sub_invalid_calculation_exception(self):
        prog = [
            'LET S "hi"',
            "SUB S 1",
            ".",
        ]
        with self.assertRaises(Exception):
            self.run_program(prog)

    def test_gosub_nonexistent_label(self):
        prog = [
            "GOSUB NO_SUCH_LABEL",
            "PRINT 100",
            "."
        ]
        with self.assertRaises(Exception):
            self.run_program(prog)

    def test_sub_with_variable_operand(self):
        prog = [
            "LET X 10",
            "LET Y 3",
            "SUB X Y",
            "PRINT X",
            "."
        ]
        self.assertEqual(self.run_program(prog), ["7"])

    def test_innum_invalid_input_exception(self):
        prog = [
            "INNUM X",
            "PRINT X",
            "."
        ]
        with self.assertRaises(Exception):
            self.run_program(prog, inputs = ["abc"])

    def test_gosub_variable_target_label_value(self):
        stmt = grin_interpreter.GOSUBStatement(target = "T")

        statements = {
            1: stmt,
            2: grin_interpreter.ENDStatement(),
        }
        labels = {"HH": 2}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1
        interp.context.variables["T"] = "HH"

        new_line = stmt.execute(interp)

        self.assertEqual(new_line, 2)
        self.assertEqual(interp.context.stack, [2])

    def test_gosub_variable_target_relative_int(self):
        stmt = grin_interpreter.GOSUBStatement(target = "JUMP")

        statements = {
            1: stmt,
            2: grin_interpreter.ENDStatement(),
            3: grin_interpreter.ENDStatement(),
        }
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1
        interp.context.variables["JUMP"] = 2

        new_line = stmt.execute(interp)

        self.assertEqual(new_line, 3)
        self.assertEqual(interp.context.stack, [2])

    def test_gosub_zero_not_permitted(self):
        stmt = grin_interpreter.GOSUBStatement(target = 0)

        statements = {
            1: stmt,
            2: grin_interpreter.ENDStatement(),
        }
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_gosub_out_of_range(self):
        stmt = grin_interpreter.GOSUBStatement(target = 10)

        statements = {
            1: stmt,
            2: grin_interpreter.ENDStatement(),
            3: grin_interpreter.ENDStatement(),
        }
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_gosub_invalid_operator_exception(self):
        old_ops = grin_interpreter.OPS.copy()
        try:
            grin_interpreter.OPS["??"] = None
            stmt = grin_interpreter.GOSUBStatement(
                target = 1,
                value1 = "A",
                op = "??",
                value2 = "B",
            )

            statements = {
                1: stmt,
                2: grin_interpreter.ENDStatement(),
            }
            labels = {}

            interp = grin_interpreter.Interpreter(statements, labels)
            interp.line = 1
            interp.context.variables["A"] = 1
            interp.context.variables["B"] = 2

            with self.assertRaises(Exception):
                stmt.execute(interp)
        finally:
            grin_interpreter.OPS.clear()
            grin_interpreter.OPS.update(old_ops)

    def test_div_with_variable_operand_int(self):
        prog = [
            "LET X 10",
            "LET Y 2",
            "DIV X Y",
            "PRINT X",
            ".",
        ]
        self.assertEqual(self.run_program(prog), ["5"])

    def test_div_by_zero_with_variable_operand(self):
        prog = [
            "INNUM X",
            "LET Y 0",
            "DIV X Y",
            ".",
        ]
        with self.assertRaises(Exception):
            self.run_program(prog, inputs = ["5.0"])

    def test_div_by_zero_with_literal_operand(self):
        prog = [
            "INNUM X",
            "DIV X 0",
            ".",
        ]
        with self.assertRaises(Exception):
            self.run_program(prog, inputs = ["5.0"])

    def test_goto_invalid_str_label_raises(self):
        stmt = grin_interpreter.GOTOStatement(target = "NO_SUCH_LABEL")

        statements = {1: stmt}
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_goto_invalid_target_type_raises(self):
        stmt = grin_interpreter.GOTOStatement(target = ["not", "valid"])

        statements = {1: stmt}
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_goto_condition_left_literal_right_variable(self):
        stmt = grin_interpreter.GOTOStatement(
            target=1,
            value1=5,
            op=">",
            value2="Y",
        )

        statements = {
            1: stmt,
            2: grin_interpreter.ENDStatement(),
        }
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1
        interp.context.variables["Y"] = 3

        new_line = stmt.execute(interp)

        self.assertEqual(new_line, 2)

    def test_mult_with_variable_operand(self):
        prog = [
            "LET X 5",
            "LET Y 2",
            "MULT X Y",
            "PRINT X",
            ".",
        ]
        self.assertEqual(self.run_program(prog), ["10"])

    def test_mult_variable_operand_raises_and_hits_except(self):
        class Weird:
            pass

        stmt = grin_interpreter.MultiplyStatement(var_name = "X", value = "Y")

        statements = {1: stmt}
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        interp.context.variables["X"] = 5
        interp.context.variables["Y"] = Weird()

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_mult_invalid_calculation_branch(self):

        stmt = grin_interpreter.MultiplyStatement(var_name="X", value=2)

        statements = {1: stmt}
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        interp.context.variables["X"] = [1, 2, 3]

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_gosub_invalid_target_type_raises(self):
        stmt = grin_interpreter.GOSUBStatement(target=["not", "valid"])

        statements = {1: stmt}
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_add_variable_operand_raises_and_hits_except(self):
        class Weird:
            pass

        stmt = grin_interpreter.AddStatement(var_name="X", value="Y")

        statements = {1: stmt}
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        interp.context.variables["X"] = 5
        interp.context.variables["Y"] = Weird()

        with self.assertRaises(Exception):
            stmt.execute(interp)

    def test_add_invalid_calculation_branch(self):
        stmt = grin_interpreter.AddStatement(var_name="X", value=2)

        statements = {1: stmt}
        labels = {}

        interp = grin_interpreter.Interpreter(statements, labels)
        interp.line = 1

        interp.context.variables["X"] = [1, 2, 3]

        with self.assertRaises(Exception):
            stmt.execute(interp)

if __name__ == "__main__":
    unittest.main()