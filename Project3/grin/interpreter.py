import operator

OPS = {
    '=':  operator.eq,
    '<>': operator.ne,
    '<':  operator.lt,
    '<=': operator.le,
    '>':  operator.gt,
    '>=': operator.ge,
}

class ExecutionContext:
    def __init__(self):
        self.variables = {}
        self.stack = []

class Interpreter:
    def __init__(self, statement_by_line, label_by_name):
        self.statements = statement_by_line
        self.labels = label_by_name
        self.line = min(self.statements)
        self.context = ExecutionContext()

    def execute(self):
        try:
            while self.line in self.statements:
                statement = self.statements[self.line]
                next_line = statement.execute(self)
                if next_line is not None:
                    self.line = next_line
                else:
                    self.line += 1
        except StopIteration:
            return

# Let var value
class LetStatement:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def execute(self, interpreter):
        if isinstance(self.value, str) and self.value in interpreter.context.variables:
            val = interpreter.context.variables[self.value]
        else:
            val = self.value
        interpreter.context.variables[self.var_name] = val
        return None

# Print value
class PrintStatement:
    def __init__(self, value):
        self.value = value

    def execute(self, interpreter):
        to_print = self.value
        if isinstance(to_print, str) and to_print in interpreter.context.variables:
            val = interpreter.context.variables[to_print]
            print(val)
        elif isinstance(to_print, (str, int, float)):
            print(to_print)
        return None

# Innum var
class InnumStatement:
    def __init__(self, var_name):
        self.var_name = var_name

    def execute(self, interpreter):
        raw = input().strip()

        try:
            val = int(raw)
        except ValueError:
            try:
                val = float(raw)
            except ValueError as e:
                print(e)
        interpreter.context.variables[self.var_name] = val
        return interpreter.line + 1


# INSTR var
class InstrStatement:
    def __init__(self, var_name):
        self.var_name = var_name

    def execute(self, interpreter):
        raw = input().strip()

        if isinstance(raw, str):
            interpreter.context.variables[self.var_name] = raw[1:-1]
        else:
            raise Exception('Invalid input {}'.format(raw))
        return interpreter.line + 1

# ADD var value
class AddStatement:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def execute(self, interpreter):
        value = interpreter.context.variables[self.var_name]
        to_add = self.value

        if isinstance(value, (int, float, str)) and isinstance(to_add, (int, float, str)):
            if isinstance(to_add, str) and to_add in interpreter.context.variables:
                to_add = interpreter.context.variables[to_add]
                try:
                    val = value + to_add
                except Exception as e:
                    print(e)
            else:
                try:
                    val = value + to_add
                except Exception as e:
                    print(e)
        else:
            raise Exception('Invalid Calculation')

        interpreter.context.variables[self.var_name] = val
        return interpreter.line + 1

# SUB var val
class SubtractStatement:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def execute(self, interpreter):
        current = interpreter.context.variables[self.var_name]
        to_sub = self.value
        result = 0

        if isinstance(current, (int, float)) and isinstance(to_sub, (int, float, str)):
            if isinstance(to_sub, str) and to_sub in interpreter.context.variables:
                to_sub = interpreter.context.variables[to_sub]
                try:
                    result = current - to_sub
                except Exception as e:
                    print(e)
            else:
                try:
                    result = current - to_sub
                except Exception as e:
                    print(e)
        else:
            raise Exception('Invalid Calculation')

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        interpreter.context.variables[self.var_name] = result
        return interpreter.line + 1

# MULT var val
class MultiplyStatement:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def execute(self, interpreter):
        value = interpreter.context.variables[self.var_name]
        to_mult = self.value

        if isinstance(value, (int, float, str)) and isinstance(to_mult, (int, float, str)):
            if isinstance(to_mult, str) and to_mult in interpreter.context.variables:
                to_mult = interpreter.context.variables[to_mult]
                try:
                    val = value * to_mult
                except Exception as e:
                    print(e)
            else:
                try:
                    val = value * to_mult
                except Exception as e:
                    print(e)
        else:
            raise Exception('Invalid Calculation')

        interpreter.context.variables[self.var_name] = val
        return interpreter.line + 1

# DIV var val
class DivideStatement:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def execute(self, interpreter):
        value = interpreter.context.variables[self.var_name]
        to_div = self.value

        if isinstance(value, (int, float)) and isinstance(to_div, (int, float, str)):
            if isinstance(value, int) and isinstance(to_div, int):
                val = value // to_div
            elif isinstance(to_div, str) and to_div in interpreter.context.variables:
                to_div = interpreter.context.variables[to_div]
                try:
                    if isinstance(value, int) and isinstance(to_div, int):
                        val = value // to_div
                    else:
                        val = value / to_div
                except Exception as e:
                    print(e)
            else:
                try:
                    val = value / to_div
                except Exception as e:
                    print(e)
        else:
            raise Exception('Invalid Calculation')

        interpreter.context.variables[self.var_name] = val
        return interpreter.line + 1

# GOTO target
class GOTOStatement:
    def __init__(self, target, value1=None, op=None, value2=None):
        self.target = target
        self.value1 = value1
        self.op = op
        self.value2 = value2

    def execute(self, interpreter):
        if self.op is not None:
            # left
            if isinstance(self.value1, str) and self.value1 in interpreter.context.variables:
                left = interpreter.context.variables[self.value1]
            else:
                left = self.value1
            # right
            if isinstance(self.value2, str) and self.value2 in interpreter.context.variables:
                right = interpreter.context.variables[self.value2]
            else:
                right = self.value2

            func = OPS[self.op]
            if func is None:
                raise Exception('Invalid operator')

            if not func(left, right):
                return None

        tgt = self.target
        if isinstance(tgt, str) and tgt in interpreter.context.variables:
            tgt = interpreter.context.variables[tgt]

        if isinstance(tgt, str):
            if tgt not in interpreter.labels:
                raise Exception('Invalid GOTO: str')
            new_line = interpreter.labels[tgt]
        elif isinstance(tgt, int):
            if tgt == 0:
                raise Exception("GOTO 0 is not permitted")
            new_line = interpreter.line + tgt
        else:
            raise Exception('Invalid GOTO')

        max_line = max(interpreter.statements)
        if new_line <= 0 or new_line > max_line + 1 or new_line == interpreter.line:
            raise Exception('Out of range')

        return new_line

# GOSUB statement
class GOSUBStatement:
    def __init__(self, target, value1 = None, op = None, value2 = None):
        self.target = target
        self.value1 = value1
        self.op = op
        self.value2 = value2

    def execute(self, interpreter):
        if self.op is not None:
            # left
            if isinstance(self.value1, str) and self.value1 in interpreter.context.variables:
                left = interpreter.context.variables[self.value1]
            else:
                left = self.value1
            # right
            if isinstance(self.value2, str) and self.value2 in interpreter.context.variables:
                right = interpreter.context.variables[self.value2]
            else:
                right = self.value2

            func = OPS[self.op]
            if func is None:
                raise Exception('Invalid operator')

            if not func(left, right):
                return None

        tgt = self.target
        if isinstance(tgt, str) and tgt in interpreter.context.variables:
            tgt = interpreter.context.variables[tgt]

        # str
        if isinstance(tgt, str):
            if tgt not in interpreter.labels:
                raise Exception('Invalid GOSUB')
            new_line = interpreter.labels[tgt]
        # int
        elif isinstance(tgt, int):
            if tgt == 0:
                raise Exception("GOSUB 0 is not permitted")
            new_line = interpreter.line + tgt
        else:
            raise Exception('Invalid GOSUB')

        max_line = max(interpreter.statements)
        if new_line <= 0 or new_line > max_line + 1 or new_line == interpreter.line:
            raise Exception('Out of range')

        interpreter.context.stack.append(interpreter.line + 1)
        return new_line

# RETURN
class RETURNStatement:
    def execute(self, interpreter):
        if not interpreter.context.stack:
            raise Exception("RETURN without matching GOSUB")
        return interpreter.context.stack.pop()

# END
class ENDStatement:
    def execute(self, interpreter):
        raise StopIteration