from __future__ import print_function
import logging
import pprint
import sys
from collections import deque


"""
Each cell has a domain.
There are also contstraints.
"""

class Cell:
    def __init__(self):
        self.domain = range(1, 10)

class UniqueConstraint:
    def __init__(self, cells):
        self.cells = cells


def gac():
    """??? """
    variables = create_cells()
    constraints = create_constraints()
    for var in variables:
        d_x = var.domain
    C = constraints
    #TODO scope not defined
    tda = set( (X, C) for c, X in zip(C, scope(c)) )
    while len(tda) != 0:
        X, c = tda.pop()
        NDx = [x for x in ???? ]
        if NDx != Dx:
            TDA = ????
            Dx = NDx
    return 


BOARD_SIZE = 9

class Board:
    def __init__(self, board):
        """Board represented as a list of strings."""
        # cells are indexed by (row, column) based on 0
        self.board = {}
        for row_i in range(BOARD_SIZE):
            for col_j in range(BOARD_SIZE):
                t = (row_i, col_j)
                self.board[t] = [i for i in range(1, 10)]
        for row, line in enumerate(board):
            for col, char in enumerate(line):
                t = (row, col)
                if char == "x":
                    # ignore
                    pass
                else:
                    self.board[t] = [int(char)]

    def prune_col(self, row_i, col_j):
        t = (row_i, col_j)
        assert len(self.board[t]) == 1
        val = self.board[t][0]
        for i in range(BOARD_SIZE):
            if i != row_i:
                t = (i, col_j)
                logging.debug("Removed {} from ({}, {})".format(
                    val, i, col_j))
                self.board[t].remove(val)

    def prune_row(self, row_i, col_j):
        t = (row_i, col_j)
        assert len(self.board[t]) == 1
        val = self.board[t][0]
        for j in range(BOARD_SIZE):
            if j != col_j:
                t = (row_i, j)
                logging.debug("Removed {} from ({}, {})".format(
                    val, row_i, j))
                self.board[t].remove(val)

    def prune_small_square(self, row_i, col_j):
        small_square_row_start = nearest_lower_multiple_of_3(row_i)
        small_square_col_start = nearest_lower_multiple_of_3(col_j)
        t = (row_i, col_j)
        assert len(self.board[t]) == 1
        val = self.board[t][0]
        for i in range(0, 3):
            for j in range(0, 3):
                row_i = small_square_row_start + i
                col_j = small_square_col_start + j
                t = (row_i, col_j)
                if t[0] != (row_i, col_j):
                    logging.debug("Removed {} from ({}, {})".format(
                        val, row_i, col_j))
                    self.board[t].remove(val)

    def is_solved(self, i, j):
        t = (i, j)
        return len(self.board[t]) == 1

    def update_cell(self, i, j, val):
        t = (i, j)
        logging.info("Updating cell {} with value {}".format(
            t, val))
        if val in self.board[t]:
            self.board[t].remove(val)
            if self.board[t] == []:
                raise ValueError("No more good values for cell {}".format(
                    t))

    def get_value(self, i, j):
        t = (i, j)
        if len(self.board[t]) == 1:
            return self.board[t][0]
        else:
            return None

    def show(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                v = self.get_value(i, j)
                print(("?" if v is None else str(v)) + " ", end="",
                    file=sys.stderr)
            print("", file=sys.stderr)


def nearest_lower_multiple_of_3(n):
    return (n / 3) * 3


board = Board(
    [
        "x1359xxxx",
        "x9xx7xx32",
        "xxxxx1xx9",
        "xx9xxxxx4",
        "12xxxxx86",
        "7xxxxx5xx",
        "6xx9xxxxx",
        "97xx2xx6x",
        "xxxx8497x"
    ]
)

def find_unsolved_cell(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not board.is_solved(i, j):
                return (i, j)
    return None


def find_solved_cell(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board.is_solved(i, j):
                return (i, j)
    return None


def create_row_rules():
    for i in range(BOARD_SIZE):
        rule = [(i, j) for j in range(BOARD_SIZE)]
        yield rule


def create_col_rules():
    for j in range(BOARD_SIZE):
        rule = [(i, j) for i in range(BOARD_SIZE)]
        yield rule


def create_small_square_rule(row, col):
    rule = []
    for i in range(3):
        for j in range(3):
            t = (row + i, col + j)
            rule.append(t)
    return rule


def create_small_square_rules():
    for i in range(0, BOARD_SIZE, 3):
        for j in range(0, BOARD_SIZE, 3):
            rule = create_small_square_rule(i, j)
            yield rule


def create_rules():
    rules = []
    row_rules = list(create_row_rules())
    rules.extend(row_rules)
    col_rules = list(create_col_rules())
    rules.extend(col_rules)
    small_square_rules = list(create_small_square_rules())
    rules.extend(small_square_rules)
    return rules


def get_rules_related_to_cell(cell, all_rules):
    for rule in all_rules:
        if cell in rule:
            yield rule


def get_cells_related_to_cell(target_cell, all_rules):
    rules = list(get_rules_related_to_cell(target_cell, all_rules))
    s = set([])
    for rule in rules:
        for cell in rule:
            if cell != target_cell:
                s.add(cell)
    return list(s)


def print_board(board):
    print("", file=sys.stderr)
    board.show()


def find_solved_cells(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board.is_solved(i, j):
                yield (i, j)


def solve(board):
    all_rules = create_rules()
    print("all rules:")
    pprint.pprint(all_rules)
    solved_cells = list(find_solved_cells(board))
    q = deque(solved_cells)
    while len(q) > 0:
        solved_cell = q.popleft()
        logging.debug("Looking at solved cell {}".format(
            solved_cell))
        logging.info("Found solved cell {}".format(solved_cell))
        # find all rules related to this cell
        related_cells = get_cells_related_to_cell(solved_cell, all_rules)
        # apply the rules to those cells
        val = board.get_value(*solved_cell)
        for cell in related_cells:
            if not board.is_solved(*cell):
                board.update_cell(cell[0], cell[1], val)
                if board.is_solved(*cell):
                    v = board.get_value(*cell)
                    logging.debug("Cell {} is now solved with value {}, added to queue".format(
                        cell, v))
                    q.append(cell)
        print_board(board)
        # pprint.pprint(related_cells)
        # each cell has a list of possibilities


def setup_logging(verbose=False):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    setup_logging(verbose=True)
    solve(board)
