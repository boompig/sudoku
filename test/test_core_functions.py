from sudoku import solver, utils
import logging


logging.basicConfig(level=logging.DEBUG)


def test_is_solved():
    # here is a solved puzzle:
    puzzle = """123456789
456789123
789123456
234567891
567891234
891234567
345678912
678912345
912345678
"""
    board = utils.read_puzzle_string(puzzle, prune=False)
    assert solver.check_format(board)
    assert solver.all_variables_assigned(board)
    assert solver.is_solved(board)


def test_not_solved_unfinished():
    # here is an unsolved solved puzzle:
    puzzle = """123456789
456789123
789123456
234567891
567091234
891234567
345678912
678912345
912345678
"""
    board = utils.read_puzzle_string(puzzle, prune=False)
    assert solver.check_format(board)
    assert not solver.is_solved(board)


def test_not_is_subsquare_constraint_satisfied():
    # here is a puzzle that should fail validation on subsquare
    # but should be fine for rows and columns
    puzzle = """123456789
234567891
345678912
456789123
567891234
789123456
678912345
891234567
912345678
"""
    board = utils.read_puzzle_string(puzzle, prune=False)
    assert solver.check_format(board)
    assert not solver.is_solved(board)
