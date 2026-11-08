import matrix_operations as mo

def gaussian_elimination(matrix):
    """
    Convert an augmented matrix into Row Echelon Form (REF)
    using Gaussian elimination and solve using back-substitution.

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

    pivot_cols = sorted(set(pivot_cols))
    free_vars = [col for col in range(num_vars) if col not in pivot_cols]

    # Check for inconsistency (No solution: 0 = non-zero)
    for row in reduced:
        all_coefficients_zero = all(mo.is_zero(row[col]) for col in range(num_vars))
        if all_coefficients_zero and not mo.is_zero(row[num_vars]):
            return {
                "matrix": reduced,
                "type": "none",
                "pivot_cols": pivot_cols,
                "free_vars": free_vars,
                "solution": None,
                "general": None,
            }

    # Unique solution using Back-Substitution for REF matrix
    if len(pivot_cols) == num_vars:
        solution = [0.0] * num_vars
        # Back-substitution from bottom to top
        for row_idx in range(len(pivot_cols) - 1, -1, -1):
            p_col = pivot_cols[row_idx]
            rhs = reduced[row_idx][num_vars]
            for j in range(p_col + 1, num_vars):
                rhs -= reduced[row_idx][j] * solution[j]
            solution[p_col] = rhs

        solution = [
            0.0 if mo.is_zero(value) else value
            for value in solution
        ]

        return {
            "matrix": reduced,
            "type": "unique",
            "pivot_cols": pivot_cols,
            "free_vars": [],
            "solution": solution,
            "general": None,
        }

    # For infinite solutions, fallback or analyze
    analysis = mo.analyze_solution(reduced, num_vars, pivot_cols)

    return {
        "matrix": reduced,
        "type": analysis["type"],
        "pivot_cols": analysis["pivot_cols"],
        "free_vars": analysis["free_vars"],
        "solution": analysis["solution"],
        "general": analysis["general"],
    }