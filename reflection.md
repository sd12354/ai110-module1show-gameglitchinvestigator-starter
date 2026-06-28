# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

	- There was an issue with the score not falling between the range of 1-100 it ended up being -35 the first time I ran it.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

	- When I click new game, its stuck on Game over start new game to try again.
	- The game said I was out of attempts even though it still said I have 1 attempt left.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                                                                 | Expected Behavior                                       | Actual Behavior                               | Console Output / Error |
| --------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------- | ---------------------- |
| 50                                                                    | Go lower                                                | Go higher                                     | none                   |
| Guessing the same number for ex: 100 twice in a row                   | Should say go lower both times                          | Switched between hints, Go higher/go lower    | none                   |
| With 1 attempt left, it says out of attempts and to start a new game. | Nothing, the user should be able to guess one more time | says out of attempts and to start a new game. | none                   |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
	- Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
	- The hints flipping back and forth was confusing me. Claude pointed out that `app.py` was turning the secret number into a string (`str(...)`) on every even attempt, so the comparison was comparing a number to text. I verified it by checking the "Developer Debug Info" and re-reading that block of code, then removed the string conversion and the hints stopped flipping.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
	- For the score, the first idea kept the original "lose points on a wrong guess" logic but just floored it at 0. When I tested it I realized the score still felt random and could sit at 0 the whole game, which wasn't what I wanted. I changed it so wrong guesses don't change the score at all and only a win adds points, and I confirmed that with a pytest test that runs several wrong guesses and checks the score never goes negative.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
	- By testing it myself and utilizing pytest.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
	- I wrote a pytest test `test_guess_too_high` that calls `check_guess(60, 50)` and checks the outcome is "Too High" and that the hint message contains "LOWER". It passed, which confirmed the hint direction was finally correct instead of backwards. I also ran `test_score_never_goes_negative_across_a_game`, which loops through several wrong guesses and proved the score can't drift negative anymore.
- Did AI help you design or understand any tests? How?
	- Yes. The starter only had 3 tests and they were failing because `check_guess` actually returns a tuple `(outcome, message)`, not just a string. Claude helped me move the logic into `logic_utils.py` and write tests that unpack the tuple, plus extra tests for `parse_guess`, `update_score`, and the difficulty ranges so all four functions are covered (15 tests total).

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

	- Every time you click a button or type something, Streamlit re-runs the whole script from top to bottom like it's the first time. So any normal variable gets reset on every click. `st.session_state` is like a little backpack that survives those re-runs, so things you want to keep (the secret number, the score, how many attempts you've used) have to live in there. The "New Game" bug made this click for me: it only reset some of the session_state, so the leftover "lost" status stuck around through the re-run and kept me on the Game Over screen.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - Writing pytest tests for the pure logic instead of only clicking around in the app. Once the logic was in `logic_utils.py`, I could prove a fix worked in a second instead of replaying the whole game by hand, and the tests catch it if I break something later.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I'd reproduce and write down each bug *before* asking the AI to fix it, instead of asking it to "fix the game" all at once. When I gave it one specific bug at a time (with the exact wrong behavior), the fixes were much more accurate and easier to verify.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI code can look clean and confident and still be quietly broken in several places at once. I trust it more as a teammate to bounce ideas off of now, but I won't ship its code without reading it and testing it myself.
