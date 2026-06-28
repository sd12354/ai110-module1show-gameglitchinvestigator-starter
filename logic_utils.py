"""Pure game-logic helpers for the Number Guessing Game.

These functions hold all of the game's decision-making. They are kept free of
Streamlit so they can be unit-tested directly with pytest (see
tests/test_game_logic.py). app.py imports everything from here.
"""


def get_range_for_difficulty(difficulty: str):
    """Return the (low, high) inclusive range for a given difficulty.

    Harder difficulties use a wider range. The original AI-generated code made
    "Hard" use a *smaller* range (1-50) than "Normal" (1-100), which made Hard
    easier than Normal -- a logic glitch. This version keeps the ranges ordered.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    # Unknown difficulty falls back to the Normal range.
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    text = raw.strip()
    try:
        # Accept whole numbers like "42" and decimals like "42.0" (truncated).
        if "." in text:
            value = int(float(text))
        else:
            value = int(text)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return (outcome, message).

    outcome is one of: "Win", "Too High", "Too Low".

    The original code gave backwards hints ("Too High" told the player to go
    HIGHER) and, in app.py, secretly turned `secret` into a string on every
    other attempt so the comparison silently broke. Both bugs are fixed here:
    the hints point the right way and the comparison is plain integer math.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        # Guess is too high, so the player needs to aim LOWER.
        return "Too High", "📉 Go LOWER!"
    # Guess is too low, so the player needs to aim HIGHER.
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update the score based on the outcome and which attempt this was.

    `attempt_number` is 1-based (the first guess is attempt 1).

    A win awards more points the sooner it happens, with a floor of 10. Wrong
    guesses do not change the score. The original code subtracted points on
    wrong guesses and flipped between +5/-5 based on whether the attempt number
    was even, which let the score drift negative (e.g. -35).
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # Too High / Too Low / anything else: no change.
    return current_score
