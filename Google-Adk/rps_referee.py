
# import google.adk is commented out since ADK is not publicly exposed; using simple local stubs instead.
# from google.adk import Agent, tool

import random

# ADK-style lightweight stubs

def tool(func):
    """ADK-style tool decorator (stub for local execution)"""
    return func

class Agent:
    def __init__(self, name, instructions, tools):
        self.name = name
        self.instructions = instructions
        self.tools = tools

# Game State (stored outside prompt)

game_state = {
    "round": 1,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False
}

# Tool 1: Validate user move

@tool
def validate_move(user_move: str) -> dict:
    """
    Checks if the user's move is valid and allowed.
    """
    allowed_moves = ["rock", "paper", "scissors", "bomb"]

    if user_move not in allowed_moves:
        return {"valid": False, "reason": "Invalid move"}

    if user_move == "bomb" and game_state["user_bomb_used"]:
        return {"valid": False, "reason": "Bomb already used"}

    return {"valid": True}

# Tool 2: Resolve round

@tool
def resolve_round(user_move: str, bot_move: str) -> dict:
    """
    Decides the winner of the round.
    """
    # Bomb rules
    if user_move == "bomb" and bot_move == "bomb":
        return {"winner": "draw", "message": "Both used bomb"}

    if user_move == "bomb":
        return {"winner": "user", "message": "Bomb beats everything"}

    if bot_move == "bomb":
        return {"winner": "bot", "message": "Bot used bomb"}

    # Normal Rock Paper Scissors
    if user_move == bot_move:
        return {"winner": "draw", "message": "Same move"}

    if (
        (user_move == "rock" and bot_move == "scissors") or
        (user_move == "paper" and bot_move == "rock") or
        (user_move == "scissors" and bot_move == "paper")
    ):
        return {"winner": "user", "message": f"{user_move} beats {bot_move}"}

    return {"winner": "bot", "message": f"{bot_move} beats {user_move}"}

# Tool 3: Update game state

@tool
def update_game_state(user_move: str, bot_move: str, winner: str) -> dict:
    """
    Updates scores, round count, and bomb usage.
    """
    if user_move == "bomb":
        game_state["user_bomb_used"] = True

    if bot_move == "bomb":
        game_state["bot_bomb_used"] = True

    if winner == "user":
        game_state["user_score"] += 1
    elif winner == "bot":
        game_state["bot_score"] += 1

    game_state["round"] += 1
    return game_state



# Agent Definition

referee_agent = Agent(
    name="rps_referee",
    instructions=(
        "You are a game referee. "
        "Explain rules briefly, validate moves using tools, "
        "resolve rounds, update state, and stop after 3 rounds."
    ),
    tools=[validate_move, resolve_round, update_game_state],
)

# Simple CLI Game Loop

print("Rock–Paper–Scissors–Plus")
print("Rules:")
print("- Best of 3 rounds")
print("- Moves: rock, paper, scissors, bomb")
print("- Bomb can be used once\n")

while game_state["round"] <= 3:
    print(f"\nRound {game_state['round']}")
    user_move = input("Your move: ").strip().lower()

    check = validate_move(user_move)
    if not check["valid"]:
        print(check["reason"])
        game_state["round"] += 1
        continue

    bot_move = random.choice(["rock", "paper", "scissors", "bomb"])
    if bot_move == "bomb" and game_state["bot_bomb_used"]:
        bot_move = random.choice(["rock", "paper", "scissors"])

    result = resolve_round(user_move, bot_move)
    update_game_state(user_move, bot_move, result["winner"])

    print(f"You: {user_move} | Bot: {bot_move}")
    print(result["message"])

print("\nFinal Result")
print("Your score:", game_state["user_score"])
print("Bot score:", game_state["bot_score"])

if game_state["user_score"] > game_state["bot_score"]:
    print("You win!")
elif game_state["user_score"] < game_state["bot_score"]:
    print("Bot wins!")
else:
    print("It's a draw!")
