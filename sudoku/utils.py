from . import solver
# import logging


def read_board_from_file(fname):
    puzzle = ""
    with open(fname) as fp:
        puzzle = fp.read()
    # print(puzzle)
    return read_puzzle_string(puzzle)


def print_unsolved_board(board):
    """
    I tried to approximate the print format in the solution files
    as closely as possible
    """
    for rowi, row in enumerate(board):
        if rowi > 0 and rowi % 3 == 0:
            print("-" * 21)
        arr = []
        for coli, possible_values in enumerate(row):
            if coli > 0 and coli % 3 == 0:
                arr.append("|")
            if len(possible_values) == 1:
                arr.append(str(possible_values[0]))
            else:
                arr.append("?")
        s = " ".join(arr)
        print(s)


def print_solved_board(board):
    print_unsolved_board(board)


def get_possible_values_for_cell(board, rowi, coli):
    possible_vals = set(range(1, 10))
    # look at other columns in the same row
    for i in range(9):
        if i != coli and len(board[rowi][i]) == 1:
            possible_vals.discard(board[rowi][i][0])
    # look at other rows in the same column
    for i in range(9):
        if i != rowi and len(board[i][coli]) == 1:
            possible_vals.discard(board[i][coli][0])
    # look at other cells in the same subsquare
    ssi = solver.get_subsquare_index((rowi, coli))
    for i, j in solver.iterate_subsquare(ssi):
        if (i, j) != (rowi, coli) and len(board[i][j]) == 1:
            possible_vals.discard(board[i][j][0])
    return list(possible_vals)


def prune_possible_values(board):
    """Once a board has been loaded, prune the impossible values for each cell"""
    num_pruned = 0
    for rowi, row in enumerate(board):
        for coli, possible_values in enumerate(row):
            if len(possible_values) > 1:
                new_possible_vals = get_possible_values_for_cell(board, rowi, coli)
                num_pruned += len(possible_values) - len(new_possible_vals)
                board[rowi][coli] = new_possible_vals
    # prune 0 for solutions
    if num_pruned > 0:
        # logging.debug("# pruned = %d", num_pruned)
        pass


def read_puzzle_string(s, prune=True):
    """
    :param prune: True to remove impossible values from the board representation
    """
    board = []
    for line in s.split("\n"):
        row = []
        line = line.rstrip()
        if line == "":
            continue
        for c in line:
            if c in [" ", "|"]:
                # internet-downloaded files dilineate subsquares using |
                continue
            elif c == "-":
                # internet-downloaded files dilineate subsquares using -
                # skip this line entirely
                break
            elif c == "=":
                # internet-downloaded solution files end the row with this char
                break
            elif c == "0":
                entry = list(range(1, 10))
            else:
                entry = [int(c)]
            row.append(entry)
        if row != []:
            assert len(row) == 9
            board.append(row)
        if len(board) == 9:
            break
    assert len(board) == 9
    if prune:
        prune_possible_values(board)
    return board
