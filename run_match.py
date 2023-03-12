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
from _accessories.game_utils import inBounds, storeLog, modinBounds
import json
import copy
import tensorflow as tf
import numpy as np
from tqdm import tqdm
# Initialize the table
Game_Table = Table()

Game_RLAgent = RLAgent(position = Table.default_starting(for_player = "RL"),
                        perception_latency = 2.5, # seconds
                        max_movement_speed = 0.125, # m/s
                        max_hit_speed = 0.5)      # m/s

for i in tqdm(range(5)):
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
                    "state": str(bool) }},s
                "Ball": {"position": {"lateral": int, "vertical": int, "depth": int} }}
    """
    VISUAL_LOG = {}
    score = {"AI": 0 , "RL": 0}
    WINNING_POINTS = 11
    continueRally = max(list(score.values())) <= WINNING_POINTS
    state = []
    # state = tf.constant([0, 0, 0])
    with tf.GradientTape(persistent=True) as tape:
        while (continueRally):
            # TODO: make parameter constructions global variables
            # Initialize the two agents

            Game_RLAgent.position = Table.default_starting(for_player="RL")

            Game_AIAgent = AIAgent(position = Table.default_starting(for_player = "AI"),
                    perception_latency = 2.5, # seconds
                    max_movement_speed = 0.5, # m/s
                    max_hit_speed = 0.5)      # m/s

            
            Game_RLAgent._id = "RL"

            # Initialze who the primary and secondary players are
            FirstMover = Game_AIAgent
            NextMover = Game_RLAgent

            # The position of the ball depends on who's starting (default is Game_AIAgent starts)
            ball_pos = copy.deepcopy(FirstMover.position)
            Game_Ball = Ball(start_pos=ball_pos)

            # SUMMARY: The AI Agent starts with the ball, so they make the first move.
            FirstMover.performAction(Game_Ball, force="hit")

            VISUAL_LOG[time_step] = {}
            ACTION_LOG[time_step], VISUAL_LOG[time_step] = storeLog(FirstMover, Game_AIAgent, Game_RLAgent, Game_Ball)

            while(continue_playing := True):
                Game_Ball.move(step_forward = 1)

                state = tf.constant([Game_Ball._position["lateral"], Game_Ball._position["depth"], Game_RLAgent.position["lateral"], Game_RLAgent.position["depth"]])  # ball_x, ball_y, and RL_x 

                # SUMMARY: Check whether we should terminate game.
                # LOGIC:
                # Immediately after the ball is hit, we check if it's in bounds.
                #   If it isn't in bounds, then the person who just hit the ball (FirstMover) is at fault.
                #   In other words, !FirstMover = NextMover gets a point, and this game ends.
                
                inBound, dim = modinBounds(Game_Ball, Game_Table)
                if not inBound:
                    assert NextMover._id in ("AI", "RL")
                    # print(f"{NextMover._id} gained a point.")

                    VISUAL_LOG[time_step] = {}
                    ACTION_LOG[time_step], VISUAL_LOG[time_step] = storeLog(FirstMover, Game_AIAgent, Game_RLAgent, Game_Ball)

                    winner_id = ""

                    if (dim == "lateral"):
                        # last player to hit it is at fault
                        winner_id = NextMover._id
                    if (dim == "depth"): 
                        if NextMover._id == "RL":
                            winner_id = "AI"
                        else: 
                            winner_id = "RL"

                    Game_RLAgent.endOfRally(winner_id=="RL")

                    # score[NextMover._id] += 1
                    score[winner_id] += 1
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

                # TODO: Add underscore to _position
                DEBUG_preActionVel, DEBUG_preActionPos = Game_Ball._velocity, NextMover.position

                rlAgentAction = ""  # nothing by default

                # AI perform action when they are "defending"
                if (NextMover._id == "AI"): 
                    nextMover_action = NextMover.performAction(Game_Ball)

                else: # RL perform action at each timestep
                    rlAgentAction = Game_RLAgent.performAction(Game_Ball, state)
                

                assert nextMover_action in ("no-perception", "re-adjusted", "hit")
                # assert DEBUG_preActionVel != Game_Ball._velocity if nextMover_action == "hit" else DEBUG_preActionVel == Game_Ball._velocity
                # assert DEBUG_preActionPos != NextMover.position if nextMover_action == "re-adjusted" else DEBUG_preActionPos == NextMover.position
                # NOTE: This is commented out because the player can stay in the same position

                # NOTE: We make an assumption that FirstMover (after hitting a ball) does not perform any action while they
                #       wait for NextMover to hit the ball back. AKA an Agent only moves if a ball is approaching them.

                # SUMMARY: Before potentially swapping player assignments, log our action.
                VISUAL_LOG[time_step] = {}
                ACTION_LOG[time_step], VISUAL_LOG[time_step] = storeLog(FirstMover, Game_AIAgent, Game_RLAgent, Game_Ball)

                # SUMMARY: Swap player assignments if required.
                # LOGIC:
                # We only swap who the `firstMover`` and `nextMover`s "truly" are if the the `nextMover` saw the ball,
                #   and was compelled to respond/hit it.
                if nextMover_action == "hit" or rlAgentAction == "hit":
                    FirstMover, NextMover = NextMover, FirstMover    

                nextMover_action == ""
                
                # Proceed in time
                time_step += 1

            # print(f"Rally Completed.\nScore is now {score}.\n\n")
        
            continueRally = max(list(score.values())) < WINNING_POINTS
            if (continueRally == False):
                Game_RLAgent.endOfEpisode(tape)
    print(f"Game #{i + 1} Complete")
    print("Score: ", score)
    score = {"AI": 0 , "RL": 0}
    
    continueRally = True

# Game_RLAgent.model.save('update-rlagent.h5')
# TODO: Add time_step and Score to the visualization
# TODO: Make visualization a bit faster

with open("Logs/ACTION_LOG.json", "w") as f:
    json.dump(ACTION_LOG, f)

with open("Logs/VISUAL_LOG.json", "w") as f:
    json.dump(VISUAL_LOG, f)

# EOF