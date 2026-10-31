EPS = 1e-9


def is_zero(value):
    """Check whether a number is approximately zero."""
    return abs(value) < EPS


def copy_matrix(matrix):
    """Return an independent copy of a matrix."""
    return [row[:] for row in matrix]


def swap_rows(matrix, i, j):
    """Swap two rows in-place."""
    matrix[i], matrix[j] = matrix[j], matrix[i]


def clean_matrix(matrix):
    """Replace values very close to zero with 0.0."""
    for row in matrix:
        for col in range(len(row)):
            if is_zero(row[col]):
                row[col] = 0.0
    return matrix


def validate_matrix(matrix):
    """
    Validate an augmented matrix.

    Returns:
        (number_of_rows, number_of_variables)
    """
    import math

    if not isinstance(matrix, list) or not matrix:
        raise ValueError("Matrix must be a non-empty list.")

    if not isinstance(matrix[0], list):
        raise ValueError("Each row must be a list.")

    num_cols = len(matrix[0])

    if num_cols < 2:
        raise ValueError(
            "An augmented matrix must have at least one variable "
            "and one RHS column."
        )

    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != num_cols:
            raise ValueError("All rows must have the same number of columns.")

        for j, value in enumerate(row):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(
                    f"Value at row {i + 1}, column {j + 1} must be numeric."
                )

            if not math.isfinite(value):
                raise ValueError(
                    f"Value at row {i + 1}, column {j + 1} must be finite."
                )

    return len(matrix), num_cols - 1


def _format_number(value):
    """Format numbers for readable solution equations."""
    if is_zero(value):
        value = 0.0

    rounded = round(value)
    if abs(value - rounded) < EPS:
        return str(int(rounded))

    return f"{value:.6g}"


def analyze_solution(rref_matrix, num_vars, pivot_cols):
    """
    Analyze a matrix that is already in RREF form.

    Returns:
        type: 'unique', 'infinite', or 'none'
        pivot_cols: zero-based pivot column indices
        free_vars: zero-based free-variable indices
        solution: numeric values or None
        general: parametric equations or None
    """
    pivot_cols = sorted(set(pivot_cols))
    free_vars = [
        col for col in range(num_vars)
        if col not in pivot_cols
    ]

    # Check for an inconsistent row: 0 = non-zero.
    for row in rref_matrix:
        all_coefficients_zero = all(
            is_zero(row[col]) for col in range(num_vars)
        )

        if all_coefficients_zero and not is_zero(row[num_vars]):
            return {
                "type": "none",
                "pivot_cols": pivot_cols,
                "free_vars": free_vars,
                "solution": None,
                "general": None,
            }

    # A pivot in every variable column means a unique solution.
    if len(pivot_cols) == num_vars:
        solution = [0.0] * num_vars

        for row_index, pivot_col in enumerate(pivot_cols):
            solution[pivot_col] = rref_matrix[row_index][num_vars]

        solution = [
            0.0 if is_zero(value) else value
            for value in solution
        ]

        return {
            "type": "unique",
            "pivot_cols": pivot_cols,
            "free_vars": [],
            "solution": solution,
            "general": None,
        }

    # Otherwise, construct a parametric solution.
    parameters = {
        col: f"t{index + 1}"
        for index, col in enumerate(free_vars)
    }

    equations = {}

    for col in free_vars:
        equations[col] = f"x{col + 1} = {parameters[col]}"

    for row_index, pivot_col in enumerate(pivot_cols):
        rhs = rref_matrix[row_index][num_vars]
        terms = []

        if not is_zero(rhs):
            terms.append(_format_number(rhs))

        for free_col in free_vars:
            coefficient = rref_matrix[row_index][free_col]

            if is_zero(coefficient):
                continue

            magnitude = abs(coefficient)
            coefficient_text = (
                "" if abs(magnitude - 1.0) < EPS
                else _format_number(magnitude)
            )

            term_body = coefficient_text + parameters[free_col]

            if not terms:
                terms.append(
                    "-" + term_body if coefficient > 0 else term_body
                )
            else:
                sign = "-" if coefficient > 0 else "+"
                terms.append(f"{sign} {term_body}")

        expression = " ".join(terms) if terms else "0"
        equations[pivot_col] = f"x{pivot_col + 1} = {expression}"

    general = [equations[col] for col in range(num_vars)]

    return {
        "type": "infinite",
        "pivot_cols": pivot_cols,
        "free_vars": free_vars,
        "solution": None,
        "general": general,
    }