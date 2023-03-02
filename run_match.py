# @Author: shounak
# @Date:   2023-02-01T19:52:38-08:00
# @Email:  shounak@stanford.edu
# @Filename: run_match.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:04:54-08:00

from Components.AIAgent import AIAgent
from Components.RLAgent import RLAgent
from Components.Table import Table
from Components.Ball import Ball
from _accessories.game_utils import inBounds
import json

# Initialize the table
Game_Table = Table()

# TODO: make parameter constructions global variables

# Initialize the two agents
Game_AIAgent = AIAgent(position = Table.default_starting(for_player = "AI"),
                    perception_latency = 0.5, # seconds
                    max_movement_speed = 0.5, # m/s
                    max_hit_speed = 50)       # m/s
# Game_AIAgent.position

Game_RLAgent = RLAgent(position = Table.default_starting(for_player = "RL"),
                    perception_latency = 0.5, # seconds
                    max_movement_speed = 0.5,       # m/s
                    max_hit_speed = 50)       # m/s
# Game_RLAgent.position

# Initialze who the primary and secondary players are
FirstMover = Game_AIAgent
NextMover = Game_RLAgent

# The position of the ball depends on who's starting (default is Game_AIAgent starts)
Game_Ball = Ball(start_pos=FirstMover.position)

# Start the game
time_step = 0
"""
Format: {time_step: {"NextMover": NextMover._id, "Action": action of NextMover}}
"""
ACTION_LOG = {}

"""
{time_step: {"AI": {"position": {"lateral": int, "vertical": int, "depth": int},
                   "state": str(bool) },
             "RL": {"position": {"lateral": int, "vertical": int, "depth": int},
                   "state": str(bool) }},
             "Ball": {"position": {"lateral": int, "vertical": int, "depth": int} }}
"""
VISUAL_LOG = {}
score = {"AI": 0 , "RL": 0}

# SUMMARY: The AI Agent starts with the ball, so they make the first move.
print(Game_Ball._velocity)
# TODO: Bug here?
FirstMover.performAction(Game_Ball, force="hit")
print(Game_Ball._velocity)
hit_time = time_step
ACTION_LOG[time_step] = {"NextMover": FirstMover._id, "Action": "hit"}
VISUAL_LOG[time_step] = {}
# TODO: The "state" is hardcoded since we don't care about this too much for the visualization
VISUAL_LOG[time_step]['AI'] = {"position": Game_AIAgent.position, "state": "true"}
VISUAL_LOG[time_step]['RL'] = {"position": Game_RLAgent.position, "state": "false"}
VISUAL_LOG[time_step]['Ball'] = {"position": Game_Ball._position}

print(Game_Ball._position)

while(continue_playing := True):
    Game_Ball.move(step_forward = 1)

    # print(Game_Ball._position)

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

    raise ValueError("stop")

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
    ACTION_LOG[time_step] = {"NextMover": NextMover._id, "Action": nextMover_action}

    # TODO: Need to actually populate VISUAL_LOG
    VISUAL_LOG[time_step] = {}
    # TODO: The "state" is hardcoded since we don't care about this too much for the visualization
    VISUAL_LOG[time_step]['AI'] = {"position": Game_AIAgent.position, "state": "true"}
    VISUAL_LOG[time_step]['RL'] = {"position": Game_RLAgent.position, "state": "false"}
    VISUAL_LOG[time_step]['Ball'] = {"position": Game_Ball._position}

    # SUMMARY: Swap player assignments if required.
    # LOGIC:
    # We only swap who the `firstMover`` and `nextMover`s "truly" are if the the `nextMover` saw the ball,
    #   and was compelled to respond/hit it.
    if nextMover_action == "hit":
        # TODO: Ensure that this swapping process deoesn't result in a bug
        FirstMover, NextMover = NextMover, FirstMover    
    
    # Proceed in time
    time_step += 1

# TODO: Need to save `ACTION_LOG` and `VISUAL_LOG` to file.
with open("Logs/ACTION_LOG.json", "w") as f:
    json.dump(ACTION_LOG, f)

with open("Logs/VISUAL_LOG.json", "w") as f:
    json.dump(VISUAL_LOG, f)

# EOF
