import math
import tkinter as tk
from tkinter import messagebox

from gaussian_elimination import gaussian_elimination
from rref import rref


class LinearAlgebraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Algebra Solver")
        self.root.geometry("850x720")
        self.root.minsize(650, 550)
        self.root.configure(bg="#10182D")

        self.entries = []

        self._build_interface()
        self.generate_matrix_grid()

    def _build_interface(self):
        """Create the main application layout."""
        title = tk.Label(
            self.root,
            text="Linear Algebra Solver",
            bg="#10182D",
            font=("Arial", 20, "bold"),
            fg="#EADCC7"
        )
        title.pack(pady=(12, 4))

        subtitle = tk.Label(
            self.root,
            text="Enter an augmented matrix, then choose a solving method.",
            bg="#10182D",
            font=("Arial", 10),
            fg="#EADCC7"
        )
        subtitle.pack(pady=(0, 10))

        dimensions_frame = tk.LabelFrame(
            self.root,
            text="System dimensions",
            bg="#10182D",
            font=("Arial", 11, "bold"),
            fg="#EADCC7",
            padx=10,
            pady=10
        )
        dimensions_frame.pack(fill="x", padx=15, pady=8)

        tk.Label(dimensions_frame, text="Number of equations:", bg="#10182D", fg="#EADCC7").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.rows_entry = tk.Entry(dimensions_frame, width=7, justify="center", bg="#FBF2CF", fg="#1A2647")
        self.rows_entry.insert(0, "2")
        self.rows_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dimensions_frame, text="Number of variables:", bg="#10182D", fg="#EADCC7").grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )
        self.cols_entry = tk.Entry(dimensions_frame, width=7, justify="center", bg="#FBF2CF", fg="#1A2647")
        self.cols_entry.insert(0, "2")
        self.cols_entry.grid(row=0, column=3, padx=5, pady=5)

        create_button = tk.Button(
            dimensions_frame,
            text="Create / Reset Matrix",
            bg="#B7CDDE",
            fg="#1A2647",
            command=self.generate_matrix_grid
        )
        create_button.grid(row=0, column=4, padx=12, pady=5)

        self.matrix_frame = tk.LabelFrame(
            self.root,
            text="Augmented matrix",
            font=("Arial", 11, "bold"),
            bg="#10182D",
            fg="#EADCC7",
            padx=10,
            pady=10
        )
        self.matrix_frame.pack(fill="both", expand=False, padx=15, pady=8)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=15, pady=8)

        gaussian_button = tk.Button(
            buttons_frame,
            text="Solve using Gaussian Elimination",
            command=self.solve_gaussian,
            bg="#F1B24A",
            fg="#FFF4EB",
            activebackground="#F1B24A",
            activeforeground="#ECD8CC",
            font=("Arial", 10, "bold"),
            padx=8,
            pady=8
        )
        gaussian_button.pack(side="left", expand=True, fill="x", padx=5)

        jordan_button = tk.Button(
            buttons_frame,
            text="Solve using Gauss-Jordan (RREF)",
            command=self.solve_jordan,
            bg="#B7CDDE",
            fg="#1A2647",
            activebackground="#B7CDDE",
            activeforeground="#1A2647",
            font=("Arial", 10, "bold"),
            padx=8,
            pady=8
        )
        jordan_button.pack(side="right", expand=True, fill="x", padx=5)

        result_frame = tk.LabelFrame(
            self.root,
            text="Result",
            font=("Arial", 11, "bold"),
            bg="#10182D",
            fg="#EADCC7",
            padx=10,
            pady=10
        )
        result_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.result_text = tk.Text(
            result_frame,
            height=14,
            wrap="word",
            font=("Courier New", 10),
            bg="#10182D",
            fg="#B7CDDE",
            state="disabled"
        )
        self.result_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.configure(yscrollcommand=scrollbar.set)

    def generate_matrix_grid(self):
        """Build an editable m x (n+1) augmented-matrix grid."""
        try:
            num_rows = int(self.rows_entry.get().strip())
            num_vars = int(self.cols_entry.get().strip())

            if num_rows <= 0 or num_vars <= 0:
                raise ValueError

            # Prevent accidentally creating an excessively large GUI grid.
            if num_rows > 20 or num_vars > 20:
                messagebox.showerror(
                    "Invalid dimensions",
                    "Please use no more than 20 equations and 20 variables."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Invalid dimensions",
                "Enter positive whole numbers for equations and variables."
            )
            return

        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.entries = []

        for col in range(num_vars):
            tk.Label(
                self.matrix_frame,
                text=f"x{col + 1}",
                font=("Arial", 10, "bold"),
                bg="#10182D",
                fg="#F6E18F"
            ).grid(row=0, column=col, padx=5, pady=4)

        tk.Label(
            self.matrix_frame,
            text="RHS",
            font=("Arial", 10, "bold"),
            bg="#10182D",
            fg="#F6E18F"
        ).grid(row=0, column=num_vars, padx=5, pady=4)

        for row_index in range(num_rows):
            row_entries = []

            for col_index in range(num_vars + 1):
                entry = tk.Entry(
                    self.matrix_frame,
                    width=10,
                    justify="center",
                    font=("Arial", 10),
                    bg="#B7CDDE" if col_index == num_vars else "#FBF2CF",
                    fg="#10182D"
                )
                entry.grid(
                    row=row_index + 1,
                    column=col_index,
                    padx=4,
                    pady=4
                )
                entry.insert(0, "0")
                row_entries.append(entry)

            self.entries.append(row_entries)

        self.display_result(
            "Matrix created. Enter your coefficients and constants, "
            "then choose a solving method."
        )

    def read_matrix(self):
        """
        Read the values currently shown in the Entry widgets.

        Returns:
            A nested list of floats, or None if validation fails.
        """
        if not self.entries:
            messagebox.showerror("Input error", "Create a matrix first.")
            return None

        matrix = []

        for row_index, entry_row in enumerate(self.entries):
            row = []

            for col_index, entry in enumerate(entry_row):
                value_text = entry.get().strip()

                if not value_text:
                    messagebox.showerror(
                        "Input error",
                        f"Cell at row {row_index + 1}, "
                        f"column {col_index + 1} is empty."
                    )
                    entry.focus_set()
                    return None

                try:
                    value = float(value_text)
                except ValueError:
                    messagebox.showerror(
                        "Invalid number",
                        f"'{value_text}' at row {row_index + 1}, "
                        f"column {col_index + 1} is not a valid number."
                    )
                    entry.focus_set()
                    return None

                if not math.isfinite(value):
                    messagebox.showerror(
                        "Invalid number",
                        "Please enter finite numbers only "
                        "(NaN and Infinity are not allowed)."
                    )
                    entry.focus_set()
                    return None

                row.append(value)

            matrix.append(row)

        return matrix

    @staticmethod
    def format_matrix(matrix):
        """Return a readable string representation of a matrix."""
        if not matrix:
            return "(empty matrix)"

        formatted_rows = []

        for row in matrix:
            formatted_values = []
            for value in row:
                if abs(value) < 1e-9:
                    value = 0.0

                rounded = round(value)
                if abs(value - rounded) < 1e-9:
                    formatted_values.append(str(int(rounded)))
                else:
                    formatted_values.append(f"{value:.6g}")

            formatted_rows.append("[ " + "   ".join(formatted_values) + " ]")

        return "\n".join(formatted_rows)

    def display_result(self, message):
        """Replace the contents of the result area."""
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.configure(state="disabled")

    def show_solver_result(self, result, method_name):
        """Display the transformed matrix and the solution information."""
        required_keys = {
            "matrix", "type", "pivot_cols",
            "free_vars", "solution", "general"
        }

        if not isinstance(result, dict) or not required_keys.issubset(result):
            raise ValueError(
                f"{method_name} returned an invalid result. "
                "It must return the agreed result dictionary."
            )

        output = [
            f"=== {method_name} ===",
            "",
            "Transformed matrix:",
            self.format_matrix(result["matrix"]),
            "",
            f"Solution type: {result['type']}",
            f"Pivot columns (1-based): "
            f"{[col + 1 for col in result['pivot_cols']]}",
            f"Free variables (1-based): "
            f"{[col + 1 for col in result['free_vars']]}",
            ""
        ]

        if result["type"] == "unique":
            output.append("Unique solution:")
            for index, value in enumerate(result["solution"]):
                output.append(f"x{index + 1} = {value:.10g}")

        elif result["type"] == "infinite":
            output.append("General solution:")
            output.extend(result["general"] or [])

        elif result["type"] == "none":
            output.append("The system is inconsistent: no solution exists.")

        else:
            raise ValueError(
                "Unknown solution type. Expected unique, infinite, or none."
            )

        self.display_result("\n".join(output))

    def _solve(self, solver_function, method_name):
        """Read the current matrix, call a solver, and display its result."""
        matrix = self.read_matrix()

        if matrix is None:
            return

        try:
            # Each algorithm is expected to preserve the input matrix
            # and return the shared result dictionary.
            result = solver_function(matrix)
            self.show_solver_result(result, method_name)

        except (ValueError, TypeError, ZeroDivisionError) as error:
            messagebox.showerror("Could not solve system", str(error))

        except Exception as error:
            messagebox.showerror(
                "Unexpected error",
                f"An unexpected error occurred:\n{error}"
            )

    def solve_gaussian(self):
        self._solve(gaussian_elimination, "Gaussian Elimination")

    def solve_jordan(self):
        self._solve(rref, "Gauss-Jordan Elimination (RREF)")


if __name__ == "__main__":
    root = tk.Tk()
    app = LinearAlgebraApp(root)
    root.mainloop()
