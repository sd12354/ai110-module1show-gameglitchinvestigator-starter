# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**The game's purpose:** A simple Streamlit number-guessing game. The app picks a
secret number in a range based on the chosen difficulty, and the player has a
limited number of attempts to guess it. After each guess the game gives a
"higher / lower" hint and updates a score; winning fewer attempts scores more.

**Bugs I found:**

1. **The hints lied.** Guessing a number too high told me to "Go HIGHER," and on
   every other attempt the hint flipped direction entirely. (Two causes: the
   hint text was reversed, and `app.py` secretly converted the secret number to
   a *string* on even-numbered attempts, which broke the comparison.)
2. **New Game didn't work.** After losing, clicking "New Game 🔁" left me stuck on
   the "Game over" screen because the game status (and score/history) was never
   reset. It also re-rolled the secret using a hardcoded `1–100` range instead of
   the selected difficulty's range.
3. **The score went negative.** Wrong guesses subtracted points (and flipped
   between +5/-5 depending on whether the attempt number was even), so my score
   dropped to things like `-35`.
4. **Off-by-one attempts.** Attempts started at `1`, so the "attempts left"
   counter was wrong and the game could say "out of attempts" while still
   showing one remaining.
5. **"Hard" was easier than "Normal."** Hard used a smaller range (`1–50`) than
   Normal (`1–100`).

**Fixes I applied:**

- Refactored all four pure-logic functions (`get_range_for_difficulty`,
  `parse_guess`, `check_guess`, `update_score`) out of `app.py` and into
  `logic_utils.py` so they could be unit-tested. `app.py` now imports them.
- Corrected the hint directions and removed the secret→string conversion so the
  comparison is always plain integer math.
- Made "New Game" reset *everything* (attempts, secret, score, status, history)
  and re-roll the secret using the selected difficulty's range.
- Rewrote scoring so a win awards `100 - 10×(attempts-1)` points (floored at 10)
  and wrong guesses never change the score, so it can't go negative.
- Started attempts at `0` and fixed the "attempts left" display.
- Made "Hard" a wider range (`1–500`) than "Normal."

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and open the app in the browser.
2. Pick a difficulty in the sidebar (Easy `1–20`, Normal `1–100`, Hard `1–500`).
   The sidebar shows the range and how many attempts you get.
3. Type a guess and click **Submit Guess 🚀**. The hint now points the correct
   way — a too-high guess says "📉 Go LOWER!" and a too-low guess says
   "📈 Go HIGHER!" — and it stays consistent on every attempt.
4. Keep guessing. The "Attempts left" counter decrements correctly, and the
   score only ever goes up (winning sooner = more points; it never goes
   negative).
5. Guess the secret to win — balloons 🎈 fire and the final score is shown. Or run
   out of attempts to see the "Game over" message.
6. Click **New Game 🔁**. The game fully resets — new secret, score back to 0,
   status back to "playing" — and you can immediately play again (no more being
   stuck on the "Game over" screen).

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.2, pytest-9.0.3, pluggy-1.6.0
collected 15 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_ranges_per_difficulty PASSED              [ 26%]
tests/test_game_logic.py::test_hard_is_not_easier_than_normal PASSED     [ 33%]
tests/test_game_logic.py::test_unknown_difficulty_defaults_to_normal PASSED [ 40%]
tests/test_game_logic.py::test_parse_valid_integer PASSED                [ 46%]
tests/test_game_logic.py::test_parse_empty_is_rejected PASSED            [ 53%]
tests/test_game_logic.py::test_parse_none_is_rejected PASSED             [ 60%]
tests/test_game_logic.py::test_parse_non_number_is_rejected PASSED       [ 66%]
tests/test_game_logic.py::test_parse_decimal_is_truncated PASSED         [ 73%]
tests/test_game_logic.py::test_win_on_first_attempt_scores_100 PASSED    [ 80%]
tests/test_game_logic.py::test_win_later_scores_less_but_never_below_10 PASSED [ 86%]
tests/test_game_logic.py::test_wrong_guess_does_not_change_score PASSED  [ 93%]
tests/test_game_logic.py::test_score_never_goes_negative_across_a_game PASSED [100%]

============================== 15 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
