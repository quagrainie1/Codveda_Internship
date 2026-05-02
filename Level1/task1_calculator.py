"""
Codveda Internship — Level 1, Task 1
Simple Calculator
-----------------
Performs addition, subtraction, multiplication, and division.
"""


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Division by zero is undefined. Please enter a non-zero divisor.")
    return a / b


OPERATIONS = {
    "1": ("Addition       (+)", add),
    "2": ("Subtraction    (-)", subtract),
    "3": ("Multiplication (×)", multiply),
    "4": ("Division       (÷)", divide),
}


def get_number(prompt: str) -> float:
    """Prompt the user until a valid number is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ✗ Invalid input. Please enter a numeric value.\n")


def display_menu() -> None:
    print("\n" + "=" * 40)
    print("       SIMPLE CALCULATOR")
    print("=" * 40)
    for key, (label, _) in OPERATIONS.items():
        print(f"  [{key}]  {label}")
    print("  [0]  Exit")
    print("=" * 40)


def main() -> None:
    print("\nWelcome to the Simple Calculator!")

    while True:
        display_menu()
        choice = input("Select an operation (0-4): ").strip()

        if choice == "0":
            print("\nGoodbye! Thanks for using the calculator.\n")
            break

        if choice not in OPERATIONS:
            print("  ✗ Invalid choice. Please select a number between 0 and 4.")
            continue

        label, operation = OPERATIONS[choice]
        print(f"\n  — {label.strip()} —")

        num1 = get_number("  Enter first number  : ")
        num2 = get_number("  Enter second number : ")

        try:
            result = operation(num1, num2)
            # Format: remove unnecessary trailing zeros for clean display
            display_result = int(result) if result == int(result) else round(result, 10)
            print(f"\n  Result: {num1} {['+','-','×','÷'][int(choice)-1]} {num2} = {display_result}")
        except ValueError as e:
            print(f"\n  ✗ Error: {e}")

        again = input("\n  Perform another calculation? (y/n): ").strip().lower()
        if again != "y":
            print("\nGoodbye! Thanks for using the calculator.\n")
            break


if __name__ == "__main__":
    main()
