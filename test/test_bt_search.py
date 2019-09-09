"""
Use sudoku puzzles downloaded from here to test the code
http://lipas.uwasa.fi/~timan/sudoku/
"""


from sudoku import solver, utils
import time


def verify_solution(board, name):
    solution_fname = "data/solutions/" + name + "_s.txt"
    s = ""
    with open(solution_fname) as fp:
        s = fp.read()
    solution_board = utils.read_puzzle_string(s)
    assert solver.is_solved(solution_board)
    for row_i in range(9):
        for col_i in range(9):
            v = board[row_i][col_i]
            expected_v = solution_board[row_i][col_i]
            assert v == expected_v


def assert_solve_puzzle(puzzle):
    puzzle_fname = "data/puzzles/" + puzzle + ".txt"
    board = utils.read_board_from_file(puzzle_fname)
    assert solver.check_format(board)
    stats = {}
    start = time.time()
    solution_found = solver.bt(1, board, stats=stats)
    end = time.time()
    print("%s - %.2f s, expanded %d states" % (puzzle, end - start, stats["num_states_expanded"]))
    assert solution_found, "Failed to find solution to puzzle %s" % puzzle
    # print_solved_board(board)
    assert board is not None
    verify_solution(board, puzzle)


# NOTE: classifications are based on the results on the above webpage

def test_easy():
    """easy should each take under a second to run per puzzle
    on the website these are the numerically-numbered difficulty"""

    easy = [
        "s01a", "s01b", "s01c",
        "s02a", "s02b", "s02c",
        "s03a", "s03b", "s03c",
        "s04a", "s04b", "s04c",
        "s05a", "s05b", "s05c",
    ]
    for puzzle in easy:
        assert_solve_puzzle(puzzle)


def test_medium():
    """medium should also take under a second to run per puzzle with few exceptions.
    On the website these are the lettered difficulty,
    as well as those labeled Easy and Medium
    Currently the longest running are 7b and 9c"""
    puzzles = [
        "s06a", "s06b", "s06c",
        "s07a", "s07b", "s07c",
        "s08a", "s08b", "s08c",
        "s09a", "s09b", "s09c",
        "s10a", "s10b", "s10c",
        "s11a", "s11b", "s11c",
    ]
    for puzzle in puzzles:
        assert_solve_puzzle(puzzle)


def test_advanced():
    """
    advanced tests are all the puzzles above medium
    most of these are in fact quite fast to solve (under 1s)
    except 15c which may take a bit longer"""
    puzzles = [
        "s12a", "s12b", "s12c",
        "s13a", "s13b", "s13c",
        "s14a", "s14b", "s14c",
        "s15a", "s15b", "s15c",
        "s16",
    ]
    for puzzle in puzzles:
        assert_solve_puzzle(puzzle)