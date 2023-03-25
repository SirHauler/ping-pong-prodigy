# @Author: shounak
# @Date:   2023-02-01T20:02:18-08:00
# @Email:  shounak@stanford.edu
# @Filename: RLAgent.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:03:33-08:00

from Components.Agent import Agent
from Components.Ball import Ball
from Components.DQN import DQN
import numpy as np

class self:
    pass

class RLAgent(Agent):
    def __init__(self, position, perception_latency=..., max_movement_speed=..., max_hit_speed=..., t=1):
        super().__init__(position, False, perception_latency, max_movement_speed, max_hit_speed)
        self._id = "RL"
        self.t = t  # specifies time interval: seconds. By Defualt
        
        self.action_mapping = {"M_L": 0,
                                "M_C": 1,
                                "M_R": 2,
                                "H_L": 3,
                                "H_C": 4,
                                "H_R": 5,
                                "H_V": 6}
        self.reverse_mapping = dict(map(reversed, self.action_mapping.items()))

        states = sorted([1, 2, 3, 4, 5, 6])
        actions = sorted(list(self.action_mapping.values()))

        actions = [0] * 2
        self._agent = DQN(states, actions,
                          lrate=1e-1,
                          discount=0.99,
                          exploration=0.3)
    
    def performAction(self, game_ball: Ball, force=None):
        # Get current state of ball
        # TODO: Can obviously be condensed, but keeping like this for clarity
        if self.position['lateral'] <= game_ball._position['lateral'] - 2:
            current_state = 1
        elif self.position['lateral'] <= game_ball._position['lateral'] - 1:
            current_state = 2
        elif self.position['lateral'] <= game_ball._position['lateral']:
            current_state = 3
        elif self.position['lateral'] <= game_ball._position['lateral'] + 1:
            current_state = 4
        elif self.position['lateral'] <= game_ball._position['lateral'] + 2:
            current_state = 5
        else:
            current_state = 6

        # Agent offers action once provided with integer state
        proposed_action = self._agent.performAction(current_state=current_state)

        print(f"Value of `proposed_action`: {proposed_action}")
        
        int_action = np.where(proposed_action == 1)
        if len(int_action) >= 0:
            # Somehow protect against this
            decoded_action = self.reverse_mapping[int_action[0]]
        else:
            decoded_action = self.reverse_mapping[int_action[0]]
        # Note that `proposed_action` is in one-hot format
        # This actually performs the action
        if decoded_action == "M_L":
            # This means we want to move left with maximum velocity*
            pass
        elif decoded_action == "M_C":
            # This means we want to stay centered with maximum velocity*
            pass
        elif decoded_action == "M_R":
            # This means we want to move right with maximum velocity*
            pass
        elif decoded_action == "H_L":
            # This means we want to hit to left side
            pass
        elif decoded_action == "H_C":
            # This means we want to hit to center
            pass
        elif decoded_action == "H_R":
            # This means we want to hit to right side
            pass
        elif decoded_action == "H_V":
            # This means we want to hit to right side
            pass
        
        # NOTE: Are the agents actually learning? Or is this basically just random performance?

        pass


# EOF