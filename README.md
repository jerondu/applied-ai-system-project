# The Impossible Guesser 2.0

## 🎮 Original Project - Game Glitch Investigator: The Impossible Guesser 

The original projects goals and capabilities were to create a guessing game system for the user. It provided the user with 3 levels of difficulty that varied in number of guesses and range of guesses, and gave hints for the user to have a chance at winning.

## 🚨 New and Improved Project - Title and Summary

This upgrade of the original project is called "The Impossible Guesser 2.0". It transforms the simple number guessing game into an AI-powered educational platform displaying advanced AI concepts. This project specifically showcases agentic workflow - where AI systems can plan, act, and learn from their actions autonomously. Users can play against intelligent AI opponents that use different strategies, compare performance metrics, and observe how AI makes decisions in real-time. This matters because it makes complex AI concepts accessible and interactive, helping users understand how modern AI systems work through hands-on experience rather than abstract theory.

## 🏗️ Architecture Overview

![AI System Diagram](assets/AI%20System%20Diagram.png)

The system diagram above illustrates the complete architecture of The Impossible Guesser 2.0. At its core is the AI Player module implementing a four-phase agentic workflow: PLAN (choosing strategies), ACT (making guesses), CHECK (evaluating feedback), and REFLECT (updating internal state). The Streamlit UI orchestrates three game modes while the Game Logic engine handles core mechanics. A comprehensive testing suite validates all components, ensuring the AI's decision-making process works reliably. Data flows from user inputs through the game logic to AI processing, with performance metrics enabling comparison between human and AI performance.

## 🛠️ Setup Instructions and How to Play

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`

### Game Modes
- **👤 Human Player**: Classic number guessing game
- **🤖 AI Opponent**: Watch AI play using different strategies
- **🎯 Human vs AI**: Compete against an AI opponent

### AI Strategies
- **Binary Search**: Optimal strategy (finds number in ~7 guesses)
- **Random**: Unpredictable guessing
- **Linear**: Systematic brute-force approach


## 💬 Sample Interactions

### Example 1: Binary Search AI Strategy
```
AI Strategy: Binary Search (Optimal)
Secret Number: 47 (range 1-100)

AI Guess #1: 50 → "Too High!"
AI Reasoning: "Splitting range 1-100 in half. This eliminates ~50% of possibilities."

AI Guess #2: 25 → "Too Low!"
AI Reasoning: "Guess 50 was too high. Adjusting search range from 1-49."

AI Guess #3: 37 → "Too Low!"
AI Guess #4: 43 → "Too Low!"
AI Guess #5: 46 → "Too Low!"
AI Guess #6: 48 → "Too High!"
AI Guess #7: 47 → "Correct!"
Result: AI wins in 7 attempts (optimal performance)
```

### Example 2: Human vs AI Competition
```
Game Mode: Human vs AI
Secret Number: 73 (AI thinking)

Human Guess #1: 50 → AI: "Too Low! Go HIGHER!"
Human Guess #2: 80 → AI: "Too High! Go LOWER!"
Human Guess #3: 65 → AI: "Too Low! Go HIGHER!"
Human Guess #4: 70 → AI: "Too Low! Go HIGHER!"
Human Guess #5: 75 → AI: "Too High! Go LOWER!"
Human Guess #6: 73 → Human: "Correct!"
Result: Human wins in 6 attempts vs AI's optimal 7
```

### Example 3: Performance Comparison
```
After 10 games:

Binary Search AI: Average 6.8 attempts, 100% win rate
Random AI: Average 45.2 attempts, 30% win rate
Human Players: Average 8.3 attempts, 85% win rate

AI demonstrates superior consistency while humans show adaptability
```

## 🏗️ Design Decisions

**Agentic Workflow Implementation**: Chose the PLAN→ACT→CHECK→REFLECT cycle to demonstrate real AI decision-making rather than simple algorithms. This makes the AI "think" like humans do, making it more educational and engaging.

**Multiple AI Strategies**: Implemented three distinct approaches (binary search, random, linear) to show how different algorithms perform. Binary search proves optimal efficiency, while random demonstrates unpredictability, and linear shows systematic but inefficient thinking.

**Streamlit UI**: Selected for rapid prototyping and educational focus over polished design. Trade-off: Less visually impressive but more accessible for learning about AI concepts.

**Comprehensive Testing**: Built 29 automated tests to ensure reliability. Trade-off: Development time investment vs. long-term stability and confidence in the system.

**Modular Architecture**: Separated AI logic, game mechanics, and UI into distinct modules. Trade-off: More complex codebase vs. easier maintenance, testing, and feature extension.


## 🧪 Testing Summary

**29 out of 29 tests passed!!**; AI agentic workflow validated across all strategies. **Confidence scores**: Binary search strategy achieves 100% optimal performance (log₂(n) attempts); random strategy shows 30% success rate with high unpredictability. **Error handling**: Fixed initial AI feedback processing bugs through iterative testing and logging; random strategy edge cases identified and documented. **Human evaluation**: Manual testing confirmed AI strategies perform as expected; binary search demonstrates superior consistency vs human adaptability in performance comparisons.

**What Worked**: Agentic workflow implementation successfully demonstrates AI decision-making. All of the 29 tests pass, the UI is functional across game modes, and the AI strategies perform as expected.

**What Didn't Work**: Initial bugs in AI feedback processing required fixes. Random strategy occasionally gets stuck in edge cases.

**What I Learned**: Modular architecture allows for easier testing and additional features. Also, agentic workflow makes AI behavior more predictable and educational for users. Specifically for testing, I learned that comprehensive testing builds confidence in the reliability of the system itself.

## 🤔 Reflection

Building this AI-enhanced guessing game taught me that AI isn't just about complex algorithms—it's about creating systems that can think step by step, just like humans do. The agentic workflow approach that I took on this project, showed me how AI can plan ahead, take action, check results, and learn from mistakes, making technology feel more intelligent and relatable. I discovered that different AI strategies work better for different situations, and that giving AI the ability to adapt makes it more powerful than rigid programming. On the problem-solving side, I learned that breaking big projects into smaller, testable pieces makes development much easier and more reliable. Testing everything thoroughly from the start prevents many struggles later, and modular design means I can improve one part without breaking everything else. Most importantly, I realized that the best AI solutions balance technical sophistication with clear, understandable behavior that helps people learn and engage.

## 📸 Demo

- [ ] ![alt text](image.png)

