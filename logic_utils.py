def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    raise ValueError(f"Invalid difficulty: {difficulty}")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        value = float(raw)
        if not value.is_integer():
            return False, None, "Please enter a whole number."
        return True, int(value), None
    except ValueError:
        return False, None, "That is not a number."


def check_guess(guess, secret):
    """
    Compare guess to secret and return outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    try:
        guess_int = int(guess)
        secret_int = int(secret)
    except Exception:
        return "Error"

    if guess_int == secret_int:
        return "Win"
    elif guess_int > secret_int:
        return "Too High"
    else:
        return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
