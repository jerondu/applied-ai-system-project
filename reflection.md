# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game looked like a normal number guessing game with a way to change the difficulty on the left side while the main part of the screen was the actual game. At the top says "Guess a number between 1 and 100. Attempts: (number of attempts left)". However, the problem with this was that anytime you changed the difficulty, the range remaing from 1 to 100 instead of changing to the specified range on the side bar. Below this has a section called "Developer Debug Info", and "Enter your guess: " with a textbox to enter your guess. Below this are two buttons: Submit Guess and New Game, and there is an option to show hint.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
One specific bug, as previously mentioned, is the fact that the range stays the same for every difficulty. For example, I would expect the range to be from numbers in between 1 and 20 for the Easy mode, as it says on the lefthand side, yet when switching to the Easy mode the main game still says to pick a number between 1 and 100. Another bug when playing the game is the inaccuracy with the"Go LOWER!" and "Go HIGHER!" messages (the hints were definitely backwards). There is no consistency with what exactly determines which is shown. For example, when typing 10, I would expect the game to tell me to go higher because the secret number was 39, but instead it prompts me to go lower. Other bugs include the New Game button not working and the score being counted very oddly.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I mainly used Copilot, especially when helping with inline chat and fixing any bugs where I commented "# FIXME: Logic breaks here" on.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
One of the AI suggestions that was correct was when fixing the problem of the hints. When I asked Copilot to explain what was wrong with the underlying logic, it broke down the problem and explained how not only where the Go HIGHER! and Go LOWER! messages where backwards, but also on in the TypeError branch, comparisons used string lexicographic order, leading to inconsitent results, which made sense. I verified the result by testing out the problem while having the undo button available, just in case I wanted to revert the changes. The logic also seemed correct just by looking at it.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
One AI suggestion that was both incorrect and misleading was when it told me that on "line 54" was where the main game prompt was hardcoded as f"Guess a number between 1 and 100", but this line of code was on line 107 when I scrolled through the code manually.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
To decide whether a bug was really fixed, I reran the program through streamlit and tried playing the game by myself to test and ensure everything working as it supposed to.
- Describe at least one test you ran (manual or using pytest)  
and what it showed you about your code.
  One of the pytests I ran was to ensure that the correct message is displayed when a guess was too high or too low. I tested this pytest after Copilot refactored the bugs in the code and moved it to logic_utils.py. Because the test passed when I ran the file in terminal, showed me that the bug that was in the code previously is truly fixed.
- Did AI help you design or understand any tests? How?
Copilot helped me design and understand some of the tests by providing a detailed description of each test it designed  in the test_game_logic.py file, showing what it tested for and the results of each test.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Apperently the secret number itself was not changing, but other bugs in the code made it seem like the number was changing. For example, there were backwards hints which wa the main reason why the secret number seemed like it was changing. The type errors from string conversions also made the game unpredictable by causing comparison bugs when comparing the guessed number to the secret number, making the secret number itself seem off. 
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
When building an app using Streamlit, unlike a normal backend server where the script runs continuously, Streamlit reruns your script from top to bottom after every user interaction. Session state is used as st.session_state to store values that should continue to exist across reruns without refreshing. For example, the secret number was stored in a st.session_state variable so that it remains unchanging after each Streamlit rerun.
- What change did you make that finally gave the game a stable secret number?
I didn't change specificallty the way the secret number was stored, because it was originally stored correctly using session state, but I changed the other bugs that were causing it to seem like the secret number was changing, like the backwards hints and the string conversion and comparison of the guessed number and secret number.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
One strategy from this project I want to reuse in future projects is commenting "#FIXME" wherever I believe lines of code are causing a bug. This way, I could open new chats for each individual FIXME area and focus on tackling each problem one at a time.
- What is one thing you would do differently next time you work with AI on a coding task?
One thing I would do differently next time I work with AI on a coding task is read carefully through all the code firt before telling AI what to do so that I can not only learn alongside using AI, but also to craft specific directions for the AI to follow when fixing the code.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project changed the way I think about AI generated code by showing me that AI is not perfect. It is still capable of making mistakes if specific instructions are not given to it. However, AI is also incredibly helpful with breaking down specific problems with the code and what is causing each bug, if questions are asked in detail.
