# Linear Algebra Solver

A simple desktop app that solves systems of linear equations. Enter an augmented matrix, pick a method, and the app shows the reduced matrix and the solution.

Built with Python and Tkinter as a Linear Algebra course project.

## Features

- Enter any system of up to 20 equations and 20 variables
- Two solving methods:
  - **Gaussian Elimination** (Row Echelon Form)
  - **Gauss-Jordan Elimination** (Reduced Row Echelon Form)
- Detects all three possible outcomes:
  - **Unique solution** – prints the value of each variable
  - **Infinite solutions** – prints the general solution using parameters (`t1`, `t2`, ...)
  - **No solution** – reports that the system is inconsistent
- Shows the transformed matrix, pivot columns, and free variables
- Input validation for empty cells, non-numeric values, and bad dimensions

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | The Tkinter GUI (input grid, buttons, result display) |
| `gaussian_elimination.py` | Gaussian elimination algorithm |
| `rref.py` | Gauss-Jordan elimination algorithm |
| `matrix_operations.py` | Shared helpers: validation, row swap, copy, zero-check, solution analysis |


## How to Run

```bash
python main.py
```

## How to Use

1. Enter the **number of equations** and **number of variables**, then click **Create / Reset Matrix**.
2. Fill in the coefficients and the right-hand side (RHS) constants.
3. Click **Solve using Gaussian Elimination** or **Solve using Gauss-Jordan (RREF)**.
4. Read the result in the **Result** panel.

### Example

The system:

```
x1 + x2 = 3
x1 - x2 = 1
```

is entered as the augmented matrix:

```
[ 1   1 | 3 ]
[ 1  -1 | 1 ]
```

Gauss-Jordan gives `x1 = 2`, `x2 = 1`.

## How It Works

Both algorithms follow the same steps:

1. Pick the largest value in the column as the pivot (partial pivoting) and swap it into place.
2. Scale the pivot row so the pivot becomes 1.
3. Eliminate the other entries in the pivot column (below the pivot for Gaussian, above and below for Gauss-Jordan).
4. Repeat for each column, then classify the system as unique, infinite, or none.

Values very close to zero (below `1e-9`) are treated as zero to avoid floating-point errors.
