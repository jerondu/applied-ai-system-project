"""
Tests for AI Player module - Agentic Workflow
Tests the PLAN -> ACT -> CHECK -> REFLECT cycle
"""

import pytest
from ai_player import AIPlayer, AIGameState


class TestAIGameState:
    """Test the AI game state management."""
    
    def test_initial_state(self):
        """Test that initial state is set correctly."""
        state = AIGameState(
            low=1, high=100, attempts=0, 
            last_guess=None, feedback_history=[], strategy="binary_search"
        )
        assert state.low == 1
        assert state.high == 100
        assert state.attempts == 0
        assert state.last_guess is None
        assert state.feedback_history == []
        assert state.strategy == "binary_search"
    
    def test_update_from_feedback_too_low(self):
        """Test state update when feedback is 'Too Low'."""
        state = AIGameState(
            low=1, high=100, attempts=0, 
            last_guess=None, feedback_history=[], strategy="binary_search"
        )
        state.update_from_feedback(50, "Too Low")
        
        assert state.low == 51  # Should update lower bound
        assert state.high == 100
        assert state.attempts == 1
        assert state.last_guess == 50
        assert ("Too Low", ) in [(fb, ) for g, fb in state.feedback_history]
    
    def test_update_from_feedback_too_high(self):
        """Test state update when feedback is 'Too High'."""
        state = AIGameState(
            low=1, high=100, attempts=0, 
            last_guess=None, feedback_history=[], strategy="binary_search"
        )
        state.update_from_feedback(75, "Too High")
        
        assert state.low == 1
        assert state.high == 74  # Should update upper bound
        assert state.attempts == 1
        assert state.last_guess == 75


class TestAIPlayer:
    """Test the AI Player class."""
    
    def test_binary_search_initialization(self):
        """Test binary search strategy initialization."""
        ai = AIPlayer(1, 100, strategy="binary_search")
        assert ai.state.strategy == "binary_search"
        assert ai.state.low == 1
        assert ai.state.high == 100
    
    def test_binary_search_first_guess(self):
        """Test that binary search picks the midpoint for first guess."""
        ai = AIPlayer(1, 100, strategy="binary_search")
        guess, reasoning = ai.plan_next_guess()
        assert guess == 50  # Midpoint of 1-100
        assert "Binary Search" in reasoning
        assert "split" in reasoning.lower()
    
    def test_binary_search_narrows_range(self):
        """Test that binary search correctly narrows the range."""
        ai = AIPlayer(1, 100, strategy="binary_search")
        
        # First guess should be 50
        guess1, _ = ai.plan_next_guess()
        assert guess1 == 50
        
        # Simulate feedback: too low
        ai.state.last_guess = guess1
        ai.process_feedback("Too Low")
        
        # Next guess should be in upper half
        guess2, _ = ai.plan_next_guess()
        assert guess2 == 75  # Midpoint of 51-100
        assert guess2 > guess1
    
    def test_random_strategy_different_guesses(self):
        """Test that random strategy produces different guesses."""
        ai = AIPlayer(1, 100, strategy="random")
        guesses = []
        for _ in range(10):
            guess, reasoning = ai.plan_next_guess()
            guesses.append(guess)
            assert "Random" in reasoning
            assert 1 <= guess <= 100
        
        # Should have some variety (very unlikely to get same number 10 times)
        assert len(set(guesses)) > 1
    
    def test_linear_strategy_starts_low(self):
        """Test that linear strategy starts from low bound."""
        ai = AIPlayer(1, 100, strategy="linear")
        guess, reasoning = ai.plan_next_guess()
        assert guess == 1
        assert "Linear" in reasoning
    
    def test_process_feedback_win(self):
        """Test processing feedback when AI wins."""
        ai = AIPlayer(1, 100, strategy="binary_search")
        ai.state.last_guess = 50
        
        reflection = ai.process_feedback("Win")
        assert "Found it" in reflection or "found it" in reflection.lower()
        assert "50" in reflection
    
    def test_process_feedback_too_high(self):
        """Test processing feedback when guess is too high."""
        ai = AIPlayer(1, 100, strategy="binary_search")
        ai.state.last_guess = 75
        
        reflection = ai.process_feedback("Too High")
        assert "too high" in reflection.lower()
        assert "75" in reflection
        # State should be updated
        assert ai.state.attempts == 1
        assert ai.state.high == 74
    
    def test_performance_summary(self):
        """Test that performance summary is generated correctly."""
        ai = AIPlayer(1, 100, strategy="binary_search")
        guess, _ = ai.plan_next_guess()
        ai.state.last_guess = guess
        ai.process_feedback("Too Low")
        
        perf = ai.get_performance_summary()
        assert perf['strategy'] == 'binary_search'
        assert perf['attempts'] == 1
        assert perf['guesses'] == [50]
        assert len(perf['feedback_history']) == 1
    
    def test_agentic_workflow_complete_game(self):
        """
        Test complete agentic workflow: PLAN -> ACT -> CHECK -> REFLECT
        This simulates a full game where AI wins.
        """
        ai = AIPlayer(1, 100, strategy="binary_search")
        secret = 47
        guesses_made = 0
        max_attempts = 20
        won = False
        
        while guesses_made < max_attempts:
            # PLAN & ACT: AI decides on next guess
            guess, reasoning = ai.plan_next_guess()
            guesses_made += 1
            ai.state.last_guess = guess
            
            # Evaluate outcome
            if guess == secret:
                outcome = "Win"
                won = True
            elif guess < secret:
                outcome = "Too Low"
            else:
                outcome = "Too High"
            
            # CHECK: Process feedback and update state
            reflection = ai.process_feedback(outcome)
            
            if outcome == "Win":
                break
        
        # Verify the AI found the secret number (or very close)
        perf = ai.get_performance_summary()
        # With binary search, should find the number in ~7 attempts for 1-100 range
        assert guesses_made < 10, f"AI took too many attempts: {guesses_made}"
        assert won, f"AI should have found the secret number, got {perf['guesses'][-1]} vs secret {secret}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
