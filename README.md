# The Impossible Guesser 2.0

## 🎮 Original Project - Game Glitch Investigator: The Impossible Guesser 

The original projects goals and capabilities were to create a guessing game system for the user. It provided the user with 3 levels of difficulty that varied in number of guesses and range of guesses, and gave hints for the user to have a chance at winning.

## 🚨 New and Improved Project

This upgrade of the original project is called "The Impossible Guesser 2.0", 

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

- [ ] Describe the game's purpose.
   This game is supposed to be a number guessing game with three different difficulties: Easy, Normal, and Hard. The number range and number of attempts is dependent on which difficulty the user chooses. The overall idea of the game is to try and guess the random secret number without running out of attempts. Users also have the option of turning on the "Show Hints" setting, enabling the game to tell the user whether their guess is too high or too low.
- [ ] Detail which bugs you found.
   The main bugs I found was that the range display was hard coded to "Guess a number between 1 and 100", regardless of difficulty, whic was misleading. The hint were also displaying swapped outcomes and messages, so when the user's guess was too low, the hint displayed "Go LOWER!" instead of "Go HIGHER!", and vice versa. Additionally, the TypeError handling included in the original code did string comparisons, which are lexicographic. This meant that on even attempts, the secret number was converted to a string, causing type errors and incorrect comparisons. There were also inconsistent scoring, and the number of attempts logic was off by one, making users start with one attempt already used.
- [ ] Explain what fixes you applied.
   The first fix was updating the "Guess a number between ..." message to use the low and high variables. Then I corrected outcome and messages by flipping the hint messages and also removing string conversion allowing consistency when making comparisons. For the inconsistent scoring, the fix applied was always substracting the score by 5 for wrong guesses. To fix the number of attempts logic, I changed the st.session_state.attempts to be set equal to 0 instead of 1 like it was originally initialized to.

## 📸 Demo

- [ ] ![alt text](image.png)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
