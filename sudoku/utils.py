from . import sudoku_fahiem


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
        l = []
        for coli, possible_values in enumerate(row):
            if coli > 0 and coli % 3 == 0:
                l.append("|")
            if len(possible_values) == 1:
                l.append(str(possible_values[0]))
            else:
                l.append("?")
        s = " ".join(l)
        print(s)


def print_solved_board(board):
    print_unsolved_board(board)


def read_puzzle_string(s):
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
    return board
