from argparse import ArgumentParser
import os
import sys
from . import solver, utils


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--filename", nargs="*", default=[],
                        help="puzzle filenames. See data/puzzles for examples")
    parser.add_argument("-d", "--dirname",
                        help="Solve all .txt puzzle files in directory")
    args = parser.parse_args()

    filenames = list(args.filename)
    if args.dirname:
        try:
            for fname in sorted(os.listdir(args.dirname)):
                if fname.endswith(".txt"):
                    filenames.append(os.path.join(args.dirname, fname))
        except FileNotFoundError:
            print(f"error: no such directory: {args.dirname}", file=sys.stderr)
            sys.exit(1)

    for filename in filenames:
        if not os.path.exists(filename):
            print(f"file {filename} does not exist", file=sys.stderr)
            sys.exit(1)

    for filename in filenames:
        print(filename)
        board = utils.read_board_from_file(filename)
        print("unsolved board:")
        utils.print_unsolved_board(board)
        print("solving...")
        solver.solve_search_naive(board)
        print("solved board:")
        utils.print_solved_board(board)
