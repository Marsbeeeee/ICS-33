from grin.parsing import parse
from grin.interpreter import *
from grin.token import GrinTokenKind

def get_value(token):
    kind = token.kind()
    text = token.text()
    if kind == GrinTokenKind.LITERAL_INTEGER:
        text = int(text)
    elif kind == GrinTokenKind.LITERAL_FLOAT:
        text = float(text)
    elif kind == GrinTokenKind.LITERAL_STRING:
        try:
            return token.value()
        except AttributeError:
            return text[1:-1]
    return text

def parse_program(lines: list[str]) -> Interpreter:
    labels_by_name = {}
    statements_by_line = {}
    line_no = 1

    for tokens in parse(lines):
        if tokens[0].kind() == GrinTokenKind.DOT:
            break

        if (len(tokens) >= 2
            and tokens[0].kind() == GrinTokenKind.IDENTIFIER
            and tokens[1].kind() == GrinTokenKind.COLON):
            label = tokens[0].text()
            labels_by_name[label] = line_no
            tokens = tokens[2:]
            if not tokens:
                line_no += 1
                continue

        kind = tokens[0].kind()
        # LET var value
        if kind == GrinTokenKind.LET:
            var = tokens[1].text()
            val = get_value(tokens[2])
            statement = LetStatement(var, val)
        # PRINT var
        elif kind == GrinTokenKind.PRINT:
            val = get_value(tokens[1])
            statement = PrintStatement(val)
        # INNUM var
        elif kind == GrinTokenKind.INNUM:
            var = tokens[1].text()
            statement = InnumStatement(var)
        # INSTR var
        elif kind == GrinTokenKind.INSTR:
            var = tokens[1].text()
            statement = InstrStatement(var)
        # ADD var val
        elif kind == GrinTokenKind.ADD:
            var = tokens[1].text()
            val = get_value(tokens[2])
            statement = AddStatement(var, val)
        # SUB var val
        elif kind == GrinTokenKind.SUB:
            var = tokens[1].text()
            val = get_value(tokens[2])
            statement = SubtractStatement(var, val)
        # MULT var val
        elif kind == GrinTokenKind.MULT:
            var = tokens[1].text()
            val = get_value(tokens[2])
            statement = MultiplyStatement(var, val)
        # DIV var val
        elif kind == GrinTokenKind.DIV:
            var = tokens[1].text()
            val = get_value(tokens[2])
            statement = DivideStatement(var, val)
        # GOTO target (IF val1 op val2)
        elif kind == GrinTokenKind.GOTO:
            target = get_value(tokens[1])
            value1 = op = value2 = None
            if len(tokens) > 2 and tokens[2].kind() == GrinTokenKind.IF:
                value1 = get_value(tokens[3])
                op = tokens[4].text()
                value2 = get_value(tokens[5])
            statement = GOTOStatement(target, value1, op, value2)
        # GOSUB
        elif kind == GrinTokenKind.GOSUB:
            target = get_value(tokens[1])
            value1 = op = value2 = None
            if len(tokens) > 2 and tokens[2].kind() == GrinTokenKind.IF:
                value1 = get_value(tokens[3])
                op = tokens[4].text()
                value2 = get_value(tokens[5])
            statement = GOSUBStatement(target, value1, op, value2)
        # RETURN
        elif kind == GrinTokenKind.RETURN:
            statement = RETURNStatement()
        # END
        elif kind == GrinTokenKind.END:
            statement = ENDStatement()
        else:
            raise Exception('Unknown token kind {}'.format(kind))

        statements_by_line[line_no] = statement
        line_no += 1

    return Interpreter(statements_by_line, labels_by_name)