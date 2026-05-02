"""
Codveda Internship — Level 3, Task 3
N-Queens Problem
----------------
Solves the classic N-Queens puzzle using backtracking.

Goal: Place N queens on an N×N chessboard such that
      no two queens share the same row, column, or diagonal.

Features:
  • Solves for any N (practical limit ~15 for instant results)
  • Counts all solutions
  • Prints a visual board for each (or first N) solution(s)
  • Shows solving statistics (nodes visited, time taken)
  • Animated display option for visual appeal
"""

import time


# ─────────────────────────────────────────
#  Core solver  (optimised backtracking)
# ─────────────────────────────────────────

class NQueensSolver:
    """
    Solves N-Queens using backtracking with three O(1)-lookup sets
    to track attacked columns and both diagonals.
    """

    def __init__(self, n: int):
        if n < 1:
            raise ValueError("N must be at least 1.")
        self.n          = n
        self.solutions  : list[list[int]] = []  # each solution = list of col indices per row
        self.nodes_visited = 0

    def solve(self) -> list[list[int]]:
        """Run the solver and return all solutions."""
        self.solutions     = []
        self.nodes_visited = 0
        cols      : set[int] = set()
        diag_main : set[int] = set()   # row - col
        diag_anti : set[int] = set()   # row + col
        board     = [-1] * self.n
        self._backtrack(0, board, cols, diag_main, diag_anti)
        return self.solutions

    def _backtrack(
        self,
        row:       int,
        board:     list[int],
        cols:      set[int],
        diag_main: set[int],
        diag_anti: set[int],
    ) -> None:
        self.nodes_visited += 1

        if row == self.n:
            self.solutions.append(board[:])
            return

        for col in range(self.n):
            if col in cols:
                continue
            md = row - col
            ad = row + col
            if md in diag_main or ad in diag_anti:
                continue

            # Place queen
            board[row] = col
            cols.add(col);  diag_main.add(md);  diag_anti.add(ad)

            self._backtrack(row + 1, board, cols, diag_main, diag_anti)

            # Remove queen
            cols.discard(col); diag_main.discard(md); diag_anti.discard(ad)


# ─────────────────────────────────────────
#  Board rendering
# ─────────────────────────────────────────

QUEEN  = "♛"
EMPTY_LIGHT = "·"
EMPTY_DARK  = "·"


def render_board(solution: list[int], n: int, use_unicode: bool = True) -> list[str]:
    """Return a list of strings forming a chessboard diagram."""
    q = QUEEN if use_unicode else "Q"
    lines = []
    top_border    = "  ┌" + ("───┬" * (n - 1)) + "───┐"
    mid_border    = "  ├" + ("───┼" * (n - 1)) + "───┤"
    bottom_border = "  └" + ("───┴" * (n - 1)) + "───┘"
    col_labels    = "    " + "   ".join(chr(ord("a") + c) for c in range(n))

    lines.append(col_labels)
    lines.append(top_border)

    for row in range(n):
        row_label = str(n - row)
        cells = []
        for col in range(n):
            if solution[row] == col:
                cells.append(f" {q} ")
            else:
                cells.append("   ")
        lines.append(f"{row_label:>2}│" + "│".join(cells) + "│")
        if row < n - 1:
            lines.append(mid_border)

    lines.append(bottom_border)
    return lines


def print_board(solution: list[int], n: int, label: str = "") -> None:
    if label:
        print(f"\n  {label}")
    for line in render_board(solution, n):
        print("  " + line)


def print_board_compact(solution: list[int], n: int, index: int) -> None:
    """Single-line compact representation."""
    row_str = " ".join(
        "♛" if solution[r] == c else ("▪" if (r + c) % 2 == 0 else "▫")
        for r in range(n) for c in range(n)
    )
    print(f"  #{index:<4}  [{', '.join(str(c+1) for c in solution)}]")


# ─────────────────────────────────────────
#  Validation
# ─────────────────────────────────────────

def validate_solution(solution: list[int]) -> bool:
    """Verify that a solution is valid (no two queens attack each other)."""
    n = len(solution)
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            c1, c2 = solution[r1], solution[r2]
            if c1 == c2:                      # same column
                return False
            if abs(r1 - r2) == abs(c1 - c2): # same diagonal
                return False
    return True


# ─────────────────────────────────────────
#  UI helpers
# ─────────────────────────────────────────

def get_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if lo <= val <= hi:
                return val
            print(f"  ✗ Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("  ✗ Not a valid integer.")


KNOWN_COUNTS = {
    1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92,
    9: 352, 10: 724, 11: 2680, 12: 14200, 13: 73712, 14: 365596,
}


def display_banner() -> None:
    print("\n" + "═" * 50)
    print("        N-QUEENS PROBLEM SOLVER")
    print("        Backtracking Algorithm")
    print("═" * 50)


def main() -> None:
    display_banner()

    while True:
        n = get_int("\n  Enter board size N (1–15): ", 1, 15)

        print(f"\n  Solving {n}-Queens …")
        solver = NQueensSolver(n)

        start = time.perf_counter()
        solutions = solver.solve()
        elapsed = time.perf_counter() - start

        count = len(solutions)
        print(f"\n  ──── Results ────────────────────────────────")
        print(f"  Board size         : {n} × {n}")
        print(f"  Solutions found    : {count}")
        if n in KNOWN_COUNTS:
            expected = KNOWN_COUNTS[n]
            match = "✔" if count == expected else "✗"
            print(f"  Expected (known)   : {expected}  {match}")
        print(f"  Nodes explored     : {solver.nodes_visited:,}")
        print(f"  Time taken         : {elapsed*1000:.3f} ms")
        print(f"  ─────────────────────────────────────────────")

        if count == 0:
            print(f"\n  No solution exists for N={n}.")
        else:
            # Ask how many boards to display
            max_show = min(count, 5 if n <= 8 else 2)
            show = get_int(
                f"\n  How many boards to display? (0–{min(count, 20)}): ",
                0, min(count, 20)
            )

            for i in range(show):
                sol = solutions[i]
                # Verify our solution
                assert validate_solution(sol), f"BUG: solution {i+1} failed validation!"
                print_board(sol, n, label=f"Solution #{i+1} of {count}")

            if count > show:
                print(f"\n  … {count - show} more solution(s) not shown.")

            # Print a compact list if there are many solutions and user asked for 0 boards
            if show == 0 and count <= 50:
                print(f"\n  Compact listing of all {count} solution(s):")
                print(f"  (column positions per row, 1-indexed)\n")
                for i, sol in enumerate(solutions, 1):
                    print_board_compact(sol, n, i)

        again = input("\n  Solve another N? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
