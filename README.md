Sudoku Solver
======

This is a modified implementation of my Sudoku Solver for my CSC384 class in Spring 2012.

I made some small changes so it would run over the command line and with Python3.
The engine is largely unchanged since 2012. Please don't judge me too harshly for code quality. I was only an undergrad.

The solver implements 4 strategies for which state to expand next:

- `FIRST_FOUND` - choose the first unassigned cell
- `MIN_ROW` - choose a cell in the row which has the fewest but non-zero unassigned cells. This is recomputed on each state expansion.
- `MIN_HEAP` - choose a cell in the row/col/subsquare which has the fewest but non-zero unassigned cells. There is book-keeping which keeps track of these numbers throughout program execution.
- `MIN_HEAP_2` - choose the cell which is under the most constraints. There is book-keeping which keeps track of these numbers throughout program execution.

Take a look at their relative performance in `data/results`.

## Implementation

This sudoku solver works via DFS. There are much smarter ways to implement a Sudoku solver.

## Run

```
python -m sudoku [-f fname] [-d dirname] [-s strategy] [--help]
```

## Testing

```
pytest test
```

or with coverage

```
pytest test --cov=sudoku --cov-report=html
```

## Linting

```
flake8 test sudoku
```