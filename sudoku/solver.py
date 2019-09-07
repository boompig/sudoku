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
    # find the numbers that are set
    numbers = []
    for col_index, possible_values in enumerate(board[row_index]):
        if len(possible_values) == 1 and col_index != position[1]:
            numbers.append(possible_values[0])
    return value not in numbers


def is_col_constraint_satisfied(board, col_index, position, value):
    """
    :param board: array of arrays, assume board is properly formatted
    :returns: true iff the column constraint for this column has been violated
    """
    numbers = []
    for row_index in range(9):
        possible_values = board[row_index][col_index]
        if len(possible_values) == 1 and row_index != position[0]:
            numbers.append(possible_values[0])
    return value not in numbers


def is_subsquare_constraint_satisfied(board, subsquare_index, position, value):
    """
    :param board: array of arrays, assume board is properly formatted
    :param subsquare_index: left to right, top to bottom
    """
    numbers = []
    row_start = (subsquare_index // 3) * 3
    col_start = (subsquare_index % 3) * 3
    for row_index in range(row_start, row_start + 3):
        for col_index in range(col_start, col_start + 3):
            possible_values = board[row_index][col_index]
            if (len(possible_values) == 1 and
                    (row_index, col_index) != position):
                numbers.append(possible_values[0])
    return value not in numbers


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
            if len(possible_values) == 0:
                raise Exception("no possible values at position (%d, %d)" %
                                (row_index, col_index))
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


def pick_unassigned_variable(board):
    """
    :returns: (row_index, col_index)
    """
    for rowi, row in enumerate(board):
        for coli, possible_values in enumerate(row):
            if len(possible_values) > 1:
                return (rowi, coli)
            elif len(possible_values) == 0:
                raise Exception("no possible values for position (%d, %d)" %
                                (rowi, coli))
    raise Exception("No more unassigned variables on this board")


def bt(level, board):
    """Backtracking search implementation straight from the slides"""
    if all_variables_assigned(board):
        return True
    position = pick_unassigned_variable(board)
    possible_values = board[position[0]][position[1]]
    for v in possible_values:
        if all_constraints_satisfied(board, position, v):
            board[position[0]][position[1]] = [v]
            if bt(level + 1, board):
                return True
    # none of the assignments work
    # undo the assignment
    board[position[0]][position[1]] = possible_values
    return False


def solve_search_naive(board):
    """
    param board: array of arrays, assume board is properly formatted
    """
    # we start with a board
    return bt(1, board)
