"""
Use sudoku puzzles downloaded from here to test the code
http://lipas.uwasa.fi/~timan/sudoku/
"""


from sudoku import solver, utils
import time


EASY_PUZZLES = [
    "s01a", "s01b", "s01c",
    "s02a", "s02b", "s02c",
    "s03a", "s03b", "s03c",
    "s04a", "s04b", "s04c",
    "s05a", "s05b", "s05c",
]

MED_PUZZLES = [
    "s06a", "s06b", "s06c",
    "s07a", "s07b", "s07c",
    "s08a", "s08b", "s08c",
    "s09a", "s09b", "s09c",
    "s10a", "s10b", "s10c",
    "s11a", "s11b", "s11c",
]


ADVANCED_PUZZLES = [
    "s12a", "s12b", "s12c",
    "s13a", "s13b", "s13c",
    "s14a", "s14b", "s14c",
    "s15a", "s15b", "s15c",
    "s16",
]


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


def assert_solve_puzzle(puzzle, strategy):
    puzzle_fname = "data/puzzles/" + puzzle + ".txt"
    board = utils.read_board_from_file(puzzle_fname)
    assert solver.check_format(board)
    stats = {}
    start = time.time()
    solution_found = solver.bt(1, board, stats=stats, strategy=strategy)
    end = time.time()
    print("{} - {:.2f}s, expanded {} states, {} backtracks, max depth={}".format(
        puzzle,
        end - start,
        stats["num_states_expanded"],
        stats["num_backtracks"],
        stats["max_depth"]))
    assert solution_found, "Failed to find solution to puzzle %s" % puzzle
    # print_solved_board(board)
    assert board is not None
    verify_solution(board, puzzle)


# NOTE: classifications are based on the results on the above webpage

def test_easy_first_found():
    for puzzle in EASY_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.FIRST_FOUND)


def test_easy_min_row():
    for puzzle in EASY_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.MIN_ROW)


def test_easy_min_heap():
    """easy should each take under a second to run per puzzle
    on the website these are the numerically-numbered difficulty"""
    for puzzle in EASY_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.MIN_HEAP)


def test_easy_min_heap_2():
    for puzzle in EASY_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.MIN_HEAP_2)


def test_medium_min_row():
    for puzzle in MED_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.MIN_ROW)


def test_advanced_min_row():
    for puzzle in ADVANCED_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.MIN_ROW)


def test_medium_min_heap():
    """medium should also take under a second to run per puzzle with few exceptions.
    On the website these are the lettered difficulty,
    as well as those labeled Easy and Medium
    Currently the longest running are 7b and 9c"""
    for puzzle in MED_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.MIN_HEAP)


def test_advanced_min_heap():
    """
    advanced tests are all the puzzles above medium
    most of these are in fact quite fast to solve (under 1s)
    except 15c which may take a bit longer"""
    for puzzle in ADVANCED_PUZZLES:
        assert_solve_puzzle(puzzle, strategy=solver.Strategies.MIN_HEAP)
