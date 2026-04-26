"""
AI Player Module - Implements agentic workflow for game-playing strategies.

The AI follows a PLAN -> ACT -> CHECK -> REFLECT cycle:
1. PLAN: Choose strategy and initial approach
2. ACT: Make a guess
3. CHECK: Evaluate feedback (hint)
4. REFLECT: Update internal state and decide next action
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class AIGameState:
    """Tracks AI's internal state during gameplay."""
    low: int
    high: int
    attempts: int
    last_guess: int | None
    feedback_history: list[tuple[int, str]]  # (guess, feedback)
    strategy: str
    
    def update_from_feedback(self, guess: int, feedback: str):
        """REFLECT phase: Update state based on feedback."""
        self.feedback_history.append((guess, feedback))
        self.attempts += 1
        self.last_guess = guess
        
        if feedback == "Too Low":
            # Guess was too low, narrow range upward
            self.low = guess + 1
        elif feedback == "Too High":
            # Guess was too high, narrow range downward
            self.high = guess - 1
    
    def get_status(self) -> str:
        """Return human-readable status of AI's knowledge."""
        remaining_range = self.high - self.low + 1
        return f"Searching between {self.low}-{self.high} ({remaining_range} possibilities left)"


class AIPlayer:
    """Represents an AI player with different guessing strategies."""
    
    def __init__(self, low: int, high: int, strategy: str = "binary_search"):
        """
        Initialize AI player.
        
        Args:
            low: Lower bound of number range
            high: Upper bound of number range
            strategy: "binary_search" (optimal), "random", or "linear"
        """
        self.state = AIGameState(
            low=low,
            high=high,
            attempts=0,
            last_guess=None,
            feedback_history=[],
            strategy=strategy
        )
    
    def plan_next_guess(self) -> tuple[int, str]:
        """
        PLAN & ACT phase: Decide on next guess based on strategy and current state.
        
        Returns:
            (guess: int, reasoning: str)
        """
        if self.state.strategy == "binary_search":
            return self._binary_search_guess()
        elif self.state.strategy == "random":
            return self._random_guess()
        elif self.state.strategy == "linear":
            return self._linear_guess()
        else:
            raise ValueError(f"Unknown strategy: {self.state.strategy}")
    
    def _binary_search_guess(self) -> tuple[int, str]:
        """Binary search: optimal strategy. Narrows range by ~50% each time."""
        guess = (self.state.low + self.state.high) // 2
        reasoning = (
            f"[Binary Search Strategy] "
            f"Splitting range {self.state.low}-{self.state.high} in half. "
            f"This eliminates ~50% of possibilities with each guess."
        )
        return guess, reasoning
    
    def _random_guess(self) -> tuple[int, str]:
        """Random strategy: unpredictable, inefficient."""
        import random
        guess = random.randint(self.state.low, self.state.high)
        reasoning = (
            f"[Random Strategy] "
            f"Picked random number {guess} from range {self.state.low}-{self.state.high}. "
            f"No optimization, just guessing!"
        )
        return guess, reasoning
    
    def _linear_guess(self) -> tuple[int, str]:
        """Linear strategy: guesses from low to high sequentially."""
        guess = self.state.low
        reasoning = (
            f"[Linear Strategy] "
            f"Starting from the bottom: guessing {guess}. "
            f"Will increment upward each turn."
        )
        return guess, reasoning
    
    def process_feedback(self, feedback: str) -> str:
        """
        CHECK phase: Process feedback and update internal state.
        
        Args:
            feedback: "Win", "Too Low", or "Too High"
        
        Returns:
            reflection_text: AI's reasoning about what it learned
        """
        last_guess = self.state.last_guess
        
        if feedback == "Win":
            reflection = f"✅ Found it! The secret number was {last_guess}."
        elif feedback == "Too Low":
            old_low = self.state.low
            self.state.update_from_feedback(last_guess, feedback)
            reflection = (
                f"📈 Guess {last_guess} was too low. "
                f"Adjusting search range from {old_low}-{self.state.high} "
                f"to {self.state.low}-{self.state.high}."
            )
        elif feedback == "Too High":
            old_high = self.state.high
            self.state.update_from_feedback(last_guess, feedback)
            reflection = (
                f"📉 Guess {last_guess} was too high. "
                f"Adjusting search range from {self.state.low}-{old_high} "
                f"to {self.state.low}-{self.state.high}."
            )
        else:
            reflection = f"❓ Unexpected feedback: {feedback}"
        
        return reflection
    
    def get_performance_summary(self) -> dict:
        """Return AI's performance metrics."""
        return {
            "strategy": self.state.strategy,
            "attempts": self.state.attempts,
            "guesses": [g for g, _ in self.state.feedback_history],
            "feedback_history": self.state.feedback_history,
        }
