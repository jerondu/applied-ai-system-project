import random
import streamlit as st
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score
from ai_player import AIPlayer


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

# Game Mode Selection
game_mode = st.sidebar.radio(
    "Game Mode",
    ["Human Player", "AI Opponent", "Human vs AI"],
    help="Choose to play yourself, watch AI play, or play against AI"
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

#FIX: Refactored logic into logic_utils.py using Copilot Agent mode
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0 #FIX: changed logic so user has correct amount of attempts

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_mode" not in st.session_state:
    st.session_state.game_mode = "Human Player"

if "ai_player" not in st.session_state:
    st.session_state.ai_player = None

if "ai_thoughts" not in st.session_state:
    st.session_state.ai_thoughts = []

# Handle game mode changes
if game_mode != st.session_state.game_mode:
    st.session_state.game_mode = game_mode
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.ai_player = None
    st.session_state.ai_thoughts = []
    st.rerun()

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# ============ AI OPPONENT MODE ============
if game_mode == "AI Opponent":
    st.divider()
    st.subheader("🤖 AI Opponent Mode")
    
    # AI strategy selector
    ai_strategy = st.sidebar.selectbox(
        "AI Strategy",
        ["binary_search", "random", "linear"],
        format_func=lambda x: {
            "binary_search": "Binary Search (Optimal)",
            "random": "Random (Lucky?)",
            "linear": "Linear (Brute Force)"
        }[x]
    )
    
    # Initialize AI player
    if st.session_state.ai_player is None:
        st.session_state.ai_player = AIPlayer(low, high, strategy=ai_strategy)
    
    # Auto-play one AI turn
    col1, col2 = st.columns(2)
    with col1:
        auto_play = st.button("🤖 AI Makes a Guess", use_container_width=True)
    with col2:
        reset_ai = st.button("🔁 New Game", use_container_width=True)
    
    if reset_ai:
        st.session_state.ai_player = AIPlayer(low, high, strategy=ai_strategy)
        st.session_state.ai_thoughts = []
        st.session_state.attempts = 0
        st.session_state.secret = random.randint(low, high)
        st.session_state.status = "playing"
        st.rerun()
    
    if st.session_state.status == "playing" and auto_play:
        # PLAN & ACT: AI decides on next guess
        guess, reasoning = st.session_state.ai_player.plan_next_guess()
        
        st.session_state.attempts += 1
        st.session_state.history.append(guess)
        
        # Set the last guess in AI state before processing feedback
        st.session_state.ai_player.state.last_guess = guess
        
        # Get feedback
        outcome = check_guess(guess, st.session_state.secret)
        
        # Display AI's guess
        st.write(f"**AI Guess #{st.session_state.attempts}:** {guess}")
        st.caption(reasoning)
        
        # CHECK phase: Evaluate feedback
        if outcome == "Win":
            feedback_text = f"✅ Correct! The secret number was {guess}!"
            st.success(feedback_text)
            st.balloons()
            st.session_state.status = "won"
        elif outcome == "Too High":
            feedback_text = "📉 Too High!"
            st.warning(feedback_text)
            reflection = st.session_state.ai_player.process_feedback(outcome)
            st.info(reflection)
        elif outcome == "Too Low":
            feedback_text = "📈 Too Low!"
            st.warning(feedback_text)
            reflection = st.session_state.ai_player.process_feedback(outcome)
            st.info(reflection)
        
        # Check if AI ran out of attempts
        if st.session_state.attempts >= attempt_limit and st.session_state.status != "won":
            st.error(f"❌ AI ran out of attempts! The secret was {st.session_state.secret}.")
            st.session_state.status = "lost"
    
    # Show game status
    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success(f"🎉 AI won in {st.session_state.attempts} attempts!")
        else:
            st.error(f"💔 AI lost after {st.session_state.attempts} attempts.")
    
    # Display AI reasoning history
    st.divider()
    with st.expander("📊 AI Thinking Process"):
        if st.session_state.ai_player:
            perf = st.session_state.ai_player.get_performance_summary()
            st.write(f"**Strategy:** {perf['strategy']}")
            st.write(f"**Guesses Made:** {perf['guesses']}")
            st.write(f"**Feedback History:**")
            for i, (g, fb) in enumerate(perf['feedback_history'], 1):
                st.write(f"  {i}. Guess {g} → {fb}")

# ============ HUMAN VS AI MODE ============
elif game_mode == "Human vs AI":
    st.subheader("🤖 Human vs AI")
    st.write("**You** guess the number that the **AI** is thinking of!")
    
    # Initialize AI's secret number if not set
    if "ai_secret" not in st.session_state:
        st.session_state.ai_secret = random.randint(low, high)
    
    # Reset logic for mode changes
    if st.session_state.game_mode != game_mode:
        st.session_state.game_mode = game_mode
        st.session_state.attempts = 0
        st.session_state.ai_secret = random.randint(low, high)
        st.session_state.score = 0
        st.session_state.status = "playing"
        st.session_state.history = []
        st.rerun()
    
    st.info(f"Guess a number between {low} and {high}. Attempts left: {attempt_limit - st.session_state.attempts}")
    
    # Show debug info
    with st.expander("Developer Debug Info"):
        st.write("AI's Secret:", st.session_state.ai_secret)
        st.write("Your Attempts:", st.session_state.attempts)
        st.write("Your Score:", st.session_state.score)
        st.write("History:", st.session_state.history)
    
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"human_vs_ai_guess_{difficulty}"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        submit_guess = st.button("Submit Guess 🚀", use_container_width=True)
    with col2:
        new_game_vs_ai = st.button("New Game 🔁", use_container_width=True)
    with col3:
        show_hint_vs_ai = st.checkbox("Show hint", value=True)
    
    if new_game_vs_ai:
        st.session_state.attempts = 0
        st.session_state.ai_secret = random.randint(low, high)
        st.session_state.score = 0
        st.session_state.status = "playing"
        st.session_state.history = []
        st.success("New game started! AI picked a new number.")
        st.rerun()
    
    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success("You won! You guessed the AI's number.")
        else:
            st.error(f"Game over. The AI's number was {st.session_state.ai_secret}.")
        st.stop()
    
    if submit_guess:
        st.session_state.attempts += 1
        
        ok, guess_int, err = parse_guess(raw_guess)
        
        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(err)
        else:
            st.session_state.history.append(guess_int)
            
            # AI provides feedback (AI is "thinking" of the number)
            outcome = check_guess(guess_int, st.session_state.ai_secret)
            
            if outcome == "Win":
                message = "🎉 Correct! You guessed it!"
                st.session_state.score = update_score(
                    current_score=st.session_state.score,
                    outcome=outcome,
                    attempt_number=st.session_state.attempts,
                )
            elif outcome == "Too High":
                message = "📉 Too High! Go LOWER!"
            elif outcome == "Too Low":
                message = "📈 Too Low! Go HIGHER!"
            else:
                message = "Error"
            
            if show_hint_vs_ai:
                if outcome == "Win":
                    st.success(message)
                    st.balloons()
                    st.session_state.status = "won"
                else:
                    st.warning(message)
            
            if outcome == "Win":
                st.success(f"You won in {st.session_state.attempts} attempts! Final score: {st.session_state.score}")
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(f"Out of attempts! The AI's number was {st.session_state.ai_secret}. Score: {st.session_state.score}")

# ============ AI OPPONENT MODE ============
else:
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        submit = st.button("Submit Guess 🚀")
    with col2:
        new_game = st.button("New Game 🔁")
    with col3:
        show_hint = st.checkbox("Show hint", value=True)

    if new_game:
        st.session_state.attempts = 0
        st.session_state.secret = random.randint(low, high)
        st.session_state.score = 0
        st.session_state.status = "playing"
        st.session_state.history = []
        st.success("New game started.")
        st.rerun()

    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success("You already won. Start a new game to play again.")
        else:
            st.error("Game over. Start a new game to try again.")
        st.stop()

    if submit:
        st.session_state.attempts += 1

        #FIX: Refactored logic into logic_utils.py using Copilot Agent mode
        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(err)
        else:
            st.session_state.history.append(guess_int)

            secret = st.session_state.secret

            #FIX: Refactored logic into logic_utils.py using Copilot Agent mode
            outcome = check_guess(guess_int, secret) 

            if outcome == "Win":
                message = "🎉 Correct!"
            elif outcome == "Too High":
                message = "📉 Go LOWER!"
            elif outcome == "Too Low":
                message = "📈 Go HIGHER!"
            else:
                message = "Error"

            if show_hint:
                st.warning(message)

            #FIX: Refactored logic into logic_utils.py using Copilot Agent mode
            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(
                        f"Out of attempts! "
                        f"The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )

st.divider()

# Performance Comparison Dashboard
st.subheader("📊 Performance Comparison")

if game_mode == "Human Player":
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 👤 Human Player")
        st.metric("Score", st.session_state.score)
        st.metric("Attempts", st.session_state.attempts)
        st.metric("Status", st.session_state.status.upper())
    with col2:
        st.write("### 🎯 Target")
        st.metric("Range", f"{low}-{high}")
        st.metric("Max Attempts", attempt_limit)
        st.metric("Difficulty", difficulty)

elif game_mode == "AI Opponent":
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🤖 AI Opponent")
        if st.session_state.ai_player:
            perf = st.session_state.ai_player.get_performance_summary()
            st.metric("Strategy", perf['strategy'].replace('_', ' ').title())
            st.metric("Attempts", perf['attempts'])
            # Calculate AI score the same way as human
            ai_score = 100 - 10 * (perf['attempts'] + 1)
            if ai_score < 10:
                ai_score = 10
            st.metric("Score (if won)", ai_score if st.session_state.status == "won" else "N/A")
    with col2:
        st.write("### 🎯 Target")
        st.metric("Range", f"{low}-{high}")
        st.metric("Max Attempts", attempt_limit)
        st.metric("Difficulty", difficulty)

elif game_mode == "Human vs AI":
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 👤 Human vs AI")
        st.metric("Score", st.session_state.score)
        st.metric("Attempts", st.session_state.attempts)
        st.metric("Status", st.session_state.status.upper())
    with col2:
        st.write("### 🤖 AI Opponent")
        st.metric("Strategy", "Thinking")
        st.metric("Range", f"{low}-{high}")
        st.metric("Secret Set", "✅" if "ai_secret" in st.session_state else "❌")


