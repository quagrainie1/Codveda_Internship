"""
Codveda Internship — Level 1, Task 2
Number Guessing Game
--------------------
Randomly generates a number between 1 and 100.
The player has a limited number of attempts to guess it.
"""

import random

LOWER_BOUND = 1
UPPER_BOUND = 100
MAX_ATTEMPTS = 10


def get_guess(attempt: int, max_attempts: int) -> int:
    """Prompt until the user enters a valid integer in the valid range."""
    while True:
        try:
            raw = input(f"  Attempt {attempt}/{max_attempts} — Your guess: ").strip()
            guess = int(raw)
            if not (LOWER_BOUND <= guess <= UPPER_BOUND):
                print(f"  ✗ Please enter a number between {LOWER_BOUND} and {UPPER_BOUND}.\n")
            else:
                return guess
        except ValueError:
            print("  ✗ Invalid input. Please enter a whole number.\n")


def give_hint(guess: int, secret: int) -> None:
    """Print a directional hint based on how close the guess is."""
    diff = abs(secret - guess)
    if diff == 0:
        return  # correct — handled by caller
    elif diff <= 5:
        direction = "slightly higher" if secret > guess else "slightly lower"
        print(f"  ↕  Very close! The answer is {direction}.")
    elif secret > guess:
        print("  ↑  Too low! Guess higher.")
    else:
        print("  ↓  Too high! Guess lower.")


def play_round() -> bool:
    """Run one full round. Returns True if the player won."""
    secret = random.randint(LOWER_BOUND, UPPER_BOUND)
    print(f"\n  I've picked a secret number between {LOWER_BOUND} and {UPPER_BOUND}.")
    print(f"  You have {MAX_ATTEMPTS} attempts. Good luck!\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        guess = get_guess(attempt, MAX_ATTEMPTS)

        if guess == secret:
            print(f"\n  🎉 Correct! The number was {secret}.")
            print(f"  You guessed it in {attempt} attempt{'s' if attempt > 1 else ''}!")
            return True

        give_hint(guess, secret)

        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"  ({remaining} attempt{'s' if remaining > 1 else ''} remaining)\n")

    print(f"\n  💀 Out of attempts! The secret number was {secret}.")
    return False


def show_banner() -> None:
    print("\n" + "=" * 45)
    print("         NUMBER GUESSING GAME")
    print("=" * 45)


def main() -> None:
    show_banner()
    wins = losses = 0

    while True:
        won = play_round()
        if won:
            wins += 1
        else:
            losses += 1

        print(f"\n  Score — Wins: {wins}  |  Losses: {losses}")
        again = input("\n  Play again? (y/n): ").strip().lower()
        if again != "y":
            print(f"\n  Thanks for playing! Final score — Wins: {wins}, Losses: {losses}\n")
            break
        show_banner()


if __name__ == "__main__":
    main()
