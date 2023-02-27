# @Author: shounak
# @Date:   2023-02-01T19:52:38-08:00
# @Email:  shounak@stanford.edu
# @Filename: run_match.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:04:54-08:00

from Components import AIAgent, RLAgent, Ball, Table, Game
from _accessories.game_utils import inBounds

# Initialize the table
Game_Table = Table()

# TODO: make parameter constructions global variables

# Initialize the two agents
Game_AIAgent = AIAgent(position = {"lateral": Game_Table.default_lateral(for_player="AI"),
                                   "vertical": Game_Table.default_vertical(for_player="AI"),
                                   "depth": Game_Table.default_depth(for_player="AI")},
                    perception_latency = 0.5, # seconds
                    max_movement_speed = 0.5, # m/s
                    max_hit_speed = 50)       # m/s

Game_RLAgent = RLAgent(position = {"lateral": Game_Table.default_lateral(for_player="RL"),
                                   "vertical": Game_Table.default_vertical(for_player="RL"),
                                   "depth": Game_Table.default_depth(for_player="RL")},
                    perception_latency = 0.5, # seconds
                    max_velocity = 0.5,       # m/s
                    max_hit_speed = 50)       # m/s

# Initialze who the primary and secondary players are
FirstMover = Game_AIAgent
NextMover = Game_RLAgent

# The position of the ball depends on who's starting (default is Game_AIAgent starts)
Game_Ball = Ball(start_pos=FirstMover.position)

# Start the game
time_step = 0
ACTION_LOG = []                   # Format: List[(time_step, NextMover._id, action of NextMover)]
score = {"AI": 0 , "RL": 0}

# SUMMARY: The AI Agent starts with the ball, so they make the first move.
FirstMover.performAction(Game_Ball, force="hit")
hit_time = time_step
ACTION_LOG.append((time_step, FirstMover._id, "hit"))

while(continue_playing := True):
    Game_Ball.move(step_forward = 1)

    # SUMMARY: Check whether we should terminate game.
    # LOGIC:
    # Immediately after the ball is hit, we check if it's in bounds.
    #   If it isn't in bounds, then the person who just hit the ball (FirstMover) is at fault.
    #   In other words, !FirstMover = NextMover gets a point, and this game ends.
    if not inBounds(Game_Ball, Game_Table):
        assert NextMover._id in ("AI", "RL")
        score[NextMover._id] += 1
        time_step += 1
        break

    # SUMMARY: NextMover performs an action, if it can.
    nextMover_action = "no-perception"
    # LOGIC:
    # If NextMover can perceive the ball some arbitrary time after FirstMover hit the ball,
    #   NextMover can either adjust their own ready-position or – if objectively REQUIRED – hit the ball.
    # If NextMover can NOT perceive the ball some arbitrary time after FirstMover hit the ball,
    #   NextMover just stands still.
    # MISC:
    # `performAction` updates the guts of `Game_Ball` and assigns it a new velocity if player hits.
    # Assumption: an agent can only perform a single action at a time step. AKA, agent CANNOT re-adjust and hit ball at the same time.

    DEBUG_preActionVel, DEBUG_preActionPos = Game_Ball._velocity, NextMover._position
    nextMover_action = NextMover.performAction(Game_Ball)
    assert nextMover_action in ("no-perception", "re-adjusted", "hit")
    assert DEBUG_preActionVel != Game_Ball._velocity if nextMover_action == "hit" else DEBUG_preActionVel == Game_Ball._velocity
    assert DEBUG_preActionPos != NextMover._position if nextMover_action == "re-adjusted" else DEBUG_preActionPos == NextMover._position

    # NOTE: We make an assumption that FirstMover (after hitting a ball) does not perform any action while they
    #       wait for NextMover to hit the ball back. AKA an Agent only moves if a ball is approaching them.

    # SUMMARY: Before potentially swapping player assignments, log our action.
    ACTION_LOG.append((time_step, NextMover._id, nextMover_action))

    # SUMMARY: Swap player assignments if required.
    # LOGIC:
    # We only swap who the `firstMover`` and `nextMover`s "truly" are if the the `nextMover` saw the ball,
    #   and was compelled to respond/hit it.
    if nextMover_action == "hit":
        # TODO: Ensure that this swapping process deoesn't result in a bug
        FirstMover, NextMover = NextMover, FirstMover    
    
    # Proceed in time
    time_step += 1


# EOF
