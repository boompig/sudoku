from argparse import ArgumentParser
import os
import sys
from . import solver, utils
from pprint import pprint


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--filename", nargs="*", default=[],
                        help="puzzle filenames. See data/puzzles for examples")
    parser.add_argument("-d", "--dirname",
                        help="Solve all .txt puzzle files in directory")
    parser.add_argument("-s", "--strategy",
                        choices=[strat.name for strat in solver.Strategies],
                        default=solver.Strategies.MIN_HEAP.name,
                        help="Strategy for state expansion")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="If set will also print stats about search")
    args = parser.parse_args()

    print(f"Using strategy {args.strategy}")

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
        stats = {}
        solver.solve_search_naive(
            board,
            strategy=solver.Strategies[args.strategy],
            stats=stats
        )
        print("solved board:")
        utils.print_solved_board(board)
        if args.verbose:
            pprint(stats)
