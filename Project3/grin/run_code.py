from grin.parser_builder import parse_program

def run_program(lines: list[str]):
    try:
        program = parse_program(lines)
        program.execute()
    except Exception as e:
        print(e)