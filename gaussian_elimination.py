import matrix_operations as mo

def gaussian_elimination(matrix):
    """
    Convert an augmented matrix into Row Echelon Form (REF)
    using Gaussian elimination and analyze the solution.

    The original matrix is not modified.
    """
    num_rows, num_vars = mo.validate_matrix(matrix)
    reduced = mo.copy_matrix(matrix)

    pivot_cols = []
    pivot_row = 0

    for col in range(num_vars):
        if pivot_row >= num_rows:
            break

        best_row = pivot_row
        for row in range(pivot_row + 1, num_rows):
            if abs(reduced[row][col]) > abs(reduced[best_row][col]):
                best_row = row

        if mo.is_zero(reduced[best_row][col]):
            continue

        if best_row != pivot_row:
            mo.swap_rows(reduced, pivot_row, best_row)

        pivot_value = reduced[pivot_row][col]
        for j in range(num_vars + 1):
            reduced[pivot_row][j] /= pivot_value

        # Eliminate entries below the pivot
        for row in range(pivot_row + 1, num_rows):
            factor = reduced[row][col]
            if mo.is_zero(factor):
                reduced[row][col] = 0.0
                continue

            for j in range(num_vars + 1):
                reduced[row][j] -= factor * reduced[pivot_row][j]

        pivot_cols.append(col)
        pivot_row += 1

    mo.clean_matrix(reduced)

    # Analyze the REF matrix to solve variables by back-substitution / consistency
    analysis = mo.analyze_solution(reduced, num_vars, pivot_cols)

    return {
        "matrix": reduced,
        "type": analysis["type"],
        "pivot_cols": analysis["pivot_cols"],
        "free_vars": analysis["free_vars"],
        "solution": analysis["solution"],
        "general": analysis["general"],
    }