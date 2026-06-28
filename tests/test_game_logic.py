"""Automated tests for the game logic in logic_utils.py.

Run with:  pytest tests/
check_guess returns a (outcome, message) tuple, so the tests unpack it and
assert on the outcome string.
"""

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------- check_guess ----------

def test_winning_guess():
    # If the secret is 50 and the guess is 50, it should be a win.
    outcome, _message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # Guess 60 vs secret 50 -> too high, and the hint should say go LOWER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    # Guess 40 vs secret 50 -> too low, and the hint should say go HIGHER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# ---------- get_range_for_difficulty ----------

def test_ranges_per_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 500)


def test_hard_is_not_easier_than_normal():
    # Regression test for the planted glitch: Hard used to be (1, 50),
    # making it a smaller (easier) range than Normal.
    _normal_low, normal_high = get_range_for_difficulty("Normal")
    _hard_low, hard_high = get_range_for_difficulty("Hard")
    assert hard_high >= normal_high


def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)


# ---------- parse_guess ----------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_is_rejected():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_none_is_rejected():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None


def test_parse_non_number_is_rejected():
    ok, value, err = parse_guess("banana")
    assert ok is False
    assert err == "That is not a number."


def test_parse_decimal_is_truncated():
    ok, value, _err = parse_guess("42.9")
    assert ok is True
    assert value == 42


# ---------- update_score ----------

def test_win_on_first_attempt_scores_100():
    assert update_score(0, "Win", 1) == 100


def test_win_later_scores_less_but_never_below_10():
    # Attempt 12 would be 100 - 10*11 = -10, so it floors at 10.
    assert update_score(0, "Win", 12) == 10


def test_wrong_guess_does_not_change_score():
    # Regression test for the negative-score glitch: wrong guesses kept
    # subtracting points and drove the score below zero.
    assert update_score(50, "Too High", 3) == 50
    assert update_score(50, "Too Low", 4) == 50


def test_score_never_goes_negative_across_a_game():
    score = 0
    for attempt in range(1, 6):
        score = update_score(score, "Too High", attempt)
    assert score >= 0
