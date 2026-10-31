import matrix_operations as mo


def rref(matrix):
    """
    Convert an augmented matrix into Reduced Row-Echelon Form (RREF)
    using Gauss-Jordan elimination.

    The original matrix is not modified.

    Args:
        matrix: m x (n + 1) augmented matrix represented by nested lists.

    Returns:
        A dictionary containing:
            matrix, type, pivot_cols, free_vars, solution, general
    """
    # Validate input and determine matrix dimensions.
    num_rows, num_vars = mo.validate_matrix(matrix)

    # Work on a copy so the caller's original matrix stays unchanged.
    reduced = mo.copy_matrix(matrix)

    pivot_cols = []
    pivot_row = 0

    # Process variable columns only; the last column is the RHS.
    for col in range(num_vars):
        if pivot_row >= num_rows:
            break

        # Partial pivoting: choose the largest absolute pivot candidate.
        best_row = pivot_row

        for row in range(pivot_row + 1, num_rows):
            if abs(reduced[row][col]) > abs(reduced[best_row][col]):
                best_row = row

        # No usable pivot in this column, so move to the next column.
        if mo.is_zero(reduced[best_row][col]):
            continue

        if best_row != pivot_row:
            mo.swap_rows(reduced, pivot_row, best_row)

        # Normalize the pivot row so the pivot becomes 1.
        pivot_value = reduced[pivot_row][col]

        for j in range(num_vars + 1):
            reduced[pivot_row][j] /= pivot_value

        # Eliminate the pivot column from every other row.
        for row in range(num_rows):
            if row == pivot_row:
                continue

            factor = reduced[row][col]

            if mo.is_zero(factor):
                reduced[row][col] = 0.0
                continue

            for j in range(num_vars + 1):
                reduced[row][j] -= factor * reduced[pivot_row][j]

        pivot_cols.append(col)
        pivot_row += 1

    # Remove tiny floating-point residues.
    mo.clean_matrix(reduced)

    # Classify the system and extract its solution.
    analysis = mo.analyze_solution(reduced, num_vars, pivot_cols)

    return {
        "matrix": reduced,
        "type": analysis["type"],
        "pivot_cols": analysis["pivot_cols"],
        "free_vars": analysis["free_vars"],
        "solution": analysis["solution"],
        "general": analysis["general"],
    }
