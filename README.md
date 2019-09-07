Sudoku Solver
======

This is a modified implementation of my Sudoku Solver for my CSC384 class in Spring 2012.

I made some small changes so it would run over the command line and with Python3.
The engine is largely unchanged since 2012. Please don't judge me too harshly for code quality. I was only an undergrad.

## Implementation

This sudoku solver works via DFS. There are much smarter ways to implement a Sudoku solver.

## Run

```
python -m sudoku [-f fname] [-d dirname] [--help]
```

## Testing

```
PYTHONPATH=. pytest test
```

## Linting

```
flake8 test sudoku
```