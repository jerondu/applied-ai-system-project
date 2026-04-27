# 💭 Reflection: The Impossible Guesser 2.0

AI isn't just about what works -- it's about what's responsible. Include a short reflection answering the following questions:

**What are the limitations or biases in your system?**

My AI system works well for guessing numbers in a set range, but it has some limits. It depends on getting correct hints about whether guesses are too high or too low. If the hints are wrong or unclear, the AI might struggle. The binary search method is smart and usually wins quickly, but it can be slow with very large ranges. The random strategy is simple but often takes many guesses, which isn't efficient.

**Could your AI be misused, and how would you prevent that?**

Someone might try to use this AI to cheat in games or tests where guessing numbers is involved. To prevent misuse, I built it only as a fun learning tool for a simple number guessing game. It's not connected to real-world systems and doesn't have access to outside information. The code is open for anyone to see, so people can understand it's just for education.

**What surprised you while testing your AI's reliability?**

I was surprised by how reliable the binary search AI turned out to be. In testing, it almost always guessed the right number in the fewest possible tries. I expected it to sometimes take longer, but it was very consistent. The random strategy surprised me too, because it could sometimes guess quickly by luck, but other times it took much longer than expected.

**Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.**

I used AI tools like GitHub Copilot to help write and improve the code for this project. One helpful time was when the AI suggested using a dataclass to store the game state, which made the code much cleaner and easier to manage. But there was also a time when the AI suggested a way to process feedback from guesses that had a bug in it. The code looked right at first, but when I tested it, it didn't work properly, so I had to fix it myself. 

