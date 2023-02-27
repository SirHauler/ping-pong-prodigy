# @Author: shounak
# @Date:   2023-02-01T19:52:38-08:00
# @Email:  shounak@stanford.edu
# @Filename: run_match.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:04:54-08:00

from Components import AIAgent, RLAgent, Ball, Table, Game

# Initialize the table
Game_Table = Table()

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
                    max_velocity = 2,         # m/s
                    max_hit_speed = 50)       # m/s

# The position of the ball depends on who's starting (default is Game_AIAgent starts)
Game_Ball = Ball(start_pos=Game_AIAgent.position_vec)


# EOF
