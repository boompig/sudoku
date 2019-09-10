"""
Solving sudo exactly as specified here:
http://www.cs.toronto.edu/~fbacchus/csc384/Lectures/csc384-Lecture03-BacktrackingSearch.pdf

We have a set of constraints
Run backtracking search

Board representation looks like this:

board := [row, ...]
row := [valid_values, ...]
valid_values := [number, ...]
"""

# import logging

from enum import Enum


class Strategies(Enum):
    """
    Possible strategies for choosing unassigned variable
    """

    # use the first unassigned variable found in the board in order
    FIRST_FOUND = 1

    # go through all the rows and find the one with the fewest unassigned variables
    MIN_ROW = 2

    # keep track of the number of unassigned variables in each column, row, subsquare
    # choose the row/col/subsquare with the fewest unassigned variables
    MIN_HEAP = 3

    # keep track of the number of unassigned variables in each column, row, subsquare
    # choose the cell which has the most constraints on it
    MIN_HEAP_2 = 4


def check_format(board):
    """
    make sure that the board is well-formatted
    """
    try:
        assert len(board) == 9, "board must have 9 rows, found %d" % len(board)
        for row in board:
            assert len(row) == 9, "each row must have 9 numbers"
            for possible_values in row:
                # 0 represents unfilled square
                assert isinstance(possible_values, list)
                for v in possible_values:
                    assert (isinstance(v, int) and
                            v >= 0 and v <= 9),\
                                "each value must be an integer between 0 and 9"
    except AssertionError as e:
        # logging.debug(str(e))
        print(e)
        return False
    return True


def is_row_constraint_satisfied(board, row_index, position, value):
    """
    :param board: array of arrays, assume board is properly formatted
        board may be unsolved
    :param position: (row, col) indexes
    :param value: value for that position (1, 9)
    :returns: true iff the row constraint for this row has been violated
    """
    for col_index, possible_values in enumerate(board[row_index]):
        if len(possible_values) == 1 and col_index != position[1]:
            if value == possible_values[0]:
                return False
    return True


def is_col_constraint_satisfied(board, col_index, position, value):
    """
    :param board: array of arrays, assume board is properly formatted
    :returns: true iff the column constraint for this column has been violated
    """
    for row_index in range(9):
        possible_values = board[row_index][col_index]
        if len(possible_values) == 1 and row_index != position[0]:
            if value == possible_values[0]:
                return False
    return True


def is_subsquare_constraint_satisfied(board, subsquare_index, position, value):
    """
    :param board: array of arrays, assume board is properly formatted
    :param subsquare_index: left to right, top to bottom
    """
    for (rowi, coli) in iterate_subsquare(subsquare_index):
        possible_values = board[rowi][coli]
        if (len(possible_values) == 1 and (rowi, coli) != position):
            if value == possible_values[0]:
                return False
    return True


def get_subsquare_index(position):
    rowi, coli = position
    return (rowi // 3) * 3 + (coli // 3)


def all_constraints_satisfied(board, position, value):
    rowi, coli = position
    subsquare_index = get_subsquare_index(position)
    return (is_row_constraint_satisfied(board, rowi, position, value) and
            is_col_constraint_satisfied(board, coli, position, value) and
            is_subsquare_constraint_satisfied(board, subsquare_index,
                                              position, value))


def all_variables_assigned(board):
    for row_index in range(9):
        for col_index in range(9):
            possible_values = board[row_index][col_index]
            if len(possible_values) > 1:
                return False
            assert possible_values != [], \
                "no possible values at position (%d, %d)" % \
                (row_index, col_index)
    return True


def is_solved(board):
    if not all_variables_assigned(board):
        return False
    # NOTE: this will be slow
    for row_index in range(9):
        for col_index in range(9):
            v = board[row_index][col_index][0]
            position = (row_index, col_index)
            if not all_constraints_satisfied(board, position, v):
                return False
    return True


def __pick_unassigned_variable_first_found(board):
    for rowi, row in enumerate(board):
        for coli, possible_values in enumerate(row):
            if len(possible_values) > 1:
                return (rowi, coli)
            assert possible_values != [], \
                "no possible values for position (%d, %d)" % \
                (rowi, coli)
    raise Exception("No more unassigned variables on this board")


def __pick_unassigned_variable_min_row(board):
    """
    For Sudoku, I attempt to pick a variable that has the most possible values remaining
    81 + 9 lookups
    81 = count the number of unassigned variables for this row
    9 = find the unassigned variable for this row
    """
    # try to find a row that has the fewest unassigned cells
    # note that there will be at least one row with
    min_row = 0
    min_row_unassigned = 10
    for rowi, row in enumerate(board):
        num_unassigned = sum([
            len(possible_values) > 1 for possible_values in row
        ])
        if num_unassigned < min_row_unassigned and num_unassigned > 0:
            min_row_unassigned = num_unassigned
            min_row = rowi
    assert min_row is not None, "The board is empty"
    return __pick_unassigned_cell_row(board, min_row)


def __pick_unasigned_cell_subsquare(board, subsquare_index):
    for (rowi, coli) in iterate_subsquare(subsquare_index):
        if len(board[rowi][coli]) > 1:
            return (rowi, coli)
    raise Exception("unable to find unassigned cell in subsquare")


def __pick_unassigned_cell_col(board, coli):
    for rowi in range(9):
        if len(board[rowi][coli]) > 1:
            return (rowi, coli)
    raise Exception("unable to find unassigned cell in column")


def __pick_unassigned_cell_row(board, rowi):
    for coli in range(9):
        if len(board[rowi][coli]) > 1:
            return (rowi, coli)
    raise Exception("unable to find unassigned cell in row")


def __pick_unassigned_variable_heap_2(board, unassigned_heap):
    assert unassigned_heap is not None
    min_num_unassigned = 10
    min_unassigned_pos = None
    for rowi in range(9):
        for coli in range(9):
            if len(board[rowi][coli]) > 1:
                ssi = get_subsquare_index((rowi, coli))
                num_unassigned = min(
                    unassigned_heap["subsquare"][ssi],
                    unassigned_heap["row"][rowi],
                    unassigned_heap["col"][coli]
                )
                assert num_unassigned > 0
                if num_unassigned > 0 and num_unassigned < min_num_unassigned:
                    min_num_unassigned = num_unassigned
                    min_unassigned_pos = (rowi, coli)
    assert min_unassigned_pos is not None
    return min_unassigned_pos


def __pick_unassigned_variable_heap(board, unassigned_heap):
    """
    This method requires traversing 27 + 9 items on each call
    27 = 3 * 9 = one for each constraint
    9 = find the unassigned variable for that constraint
    """
    min_num_unassigned = 10
    min_unassigned_index = None
    min_unassigned_type = None
    for i in range(9):
        for t in ["row", "col", "subsquare"]:
            num_unassigned = unassigned_heap[t][i]
            if num_unassigned > 0 and num_unassigned < min_num_unassigned:
                min_num_unassigned = num_unassigned
                min_unassigned_index = i
                min_unassigned_type = t
    assert min_unassigned_index is not None
    assert min_unassigned_type is not None
    # find the cell in the target place
    if min_unassigned_type == "row":
        return __pick_unassigned_cell_row(board, min_unassigned_index)
    elif min_unassigned_type == "col":
        return __pick_unassigned_cell_col(board, min_unassigned_index)
    else:
        return __pick_unasigned_cell_subsquare(board, min_unassigned_index)


def pick_unassigned_variable(board, strategy, unassigned_heap):
    """
    :returns: (row_index, col_index)
    """
    if strategy == Strategies.FIRST_FOUND:
        return __pick_unassigned_variable_first_found(board)
    elif strategy == Strategies.MIN_ROW:
        return __pick_unassigned_variable_min_row(board)
    else:
        (rowi, coli) = (-1, -1)
        if strategy == Strategies.MIN_HEAP:
            (rowi, coli) = __pick_unassigned_variable_heap(board, unassigned_heap)
        else:
            (rowi, coli) = __pick_unassigned_variable_heap_2(board, unassigned_heap)
        # update the heap
        unassigned_heap["row"][rowi] -= 1
        unassigned_heap["col"][coli] -= 1
        ssi = get_subsquare_index((rowi, coli))
        unassigned_heap["subsquare"][ssi] -= 1
        return (rowi, coli)


def iterate_subsquare(subsquare_index):
    row_start = (subsquare_index // 3) * 3
    col_start = (subsquare_index % 3) * 3
    for row_index in range(row_start, row_start + 3):
        for col_index in range(col_start, col_start + 3):
            yield (row_index, col_index)


def create_unassigned_heap(board):
    """
    This is not very fast but is only executed once
    """
    num_unassigned_subsquare = []
    for ssi in range(9):
        num_unassigned = 0
        for (rowi, coli) in iterate_subsquare(ssi):
            if len(board[rowi][coli]) > 1:
                num_unassigned += 1
        num_unassigned_subsquare.append(num_unassigned)

    num_unassigned_col = []
    for coli in range(9):
        num_unassigned = 0
        for rowi in range(9):
            if len(board[rowi][coli]) > 1:
                num_unassigned += 1
        num_unassigned_col.append(num_unassigned)

    num_unassigned_row = []
    for rowi in range(9):
        num_unassigned = 0
        for coli in range(9):
            if len(board[rowi][coli]) > 1:
                num_unassigned += 1
        num_unassigned_row.append(num_unassigned)

    return {
        "row": num_unassigned_row,
        "col": num_unassigned_col,
        "subsquare": num_unassigned_subsquare
    }


def reset_unassigned_variable(board, position, prev_value, unassigned_heap):
    board[position[0]][position[1]] = prev_value
    if unassigned_heap:
        ssi = get_subsquare_index(position)
        unassigned_heap["subsquare"][ssi] += 1
        rowi, coli = position
        unassigned_heap["row"][rowi] += 1
        unassigned_heap["col"][coli] += 1


def bt(level, board, strategy=Strategies.MIN_HEAP, stats=None, unassigned_heap=None):
    """Backtracking search implementation straight from the slides"""
    # keep track of the number of states expanded
    if stats is None:
        stats = {}
    stats.setdefault("num_states_expanded", 0)
    stats.setdefault("num_backtracks", 0)
    stats.setdefault("max_depth", 0)
    stats["num_states_expanded"] += 1

    if strategy in [Strategies.MIN_HEAP, Strategies.MIN_HEAP_2] and unassigned_heap is None:
        unassigned_heap = create_unassigned_heap(board)

    if all_variables_assigned(board):
        return True
    position = pick_unassigned_variable(board, strategy, unassigned_heap)
    possible_values = board[position[0]][position[1]]
    for v in possible_values:
        if all_constraints_satisfied(board, position, v):
            board[position[0]][position[1]] = [v]
            if bt(level + 1, board, strategy, stats=stats, unassigned_heap=unassigned_heap):
                return True

    # none of the assignments work
    # undo the assignment
    reset_unassigned_variable(board, position, possible_values, unassigned_heap)
    stats["num_backtracks"] += 1
    stats["max_depth"] = max(stats["max_depth"], level)
    return False


def solve_search_naive(board, strategy, stats):
    """
    param board: array of arrays, assume board is properly formatted
    """
    # we start with a board
    return bt(0, board, strategy=strategy, stats=stats)
