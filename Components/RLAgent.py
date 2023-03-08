# @Author: shounak
# @Date:   2023-02-01T20:02:18-08:00
# @Email:  shounak@stanford.edu
# @Filename: RLAgent.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:03:33-08:00

# EOF

from Components.Agent import Agent
from Components.Ball import Ball

import numpy as np

class RLAgent(Agent):
    def __init__(self, position, perception_latency=..., max_movement_speed=..., max_hit_speed=..., t=1):
        super().__init__(position, False, perception_latency, max_movement_speed, max_hit_speed)
        self._id = "RL"
        self.t = t  # specifies time interval: seconds. By Defualt
        self._move_actions = [0, 1] # left, right
        self._hit_actions = [2, 3, 4]  # hit1, hit2, hit3 in this order
        self._hit_spaces = {}

    def _hit(self, num_hit_actions, action, game_ball:Ball): 
        assert action in self._hit_actions
        coords = np.linspace(0, 5, num_hit_actions + 1) # to create num_hit_action intervals
        print(coords)
        curAction = self._hit_actions[0]
        for i in range(1, len(coords)): 
            lat1, lat2 = coords[i-1], coords[i]
            self._hit_spaces[curAction] = (lat1, lat2)
            curAction += 1
        print(self._hit_spaces)

        # now for the hit logic
        aimCoords = self._hit_spaces[action]

        newVelocity = self._defaultHit(aimCoords[0], aimCoords[1], game_ball=game_ball)

        game_ball.setVelocity(newVelocity=newVelocity)        

        #TODO: Reset temporal latency somewhere: unless I decide to scrap
    
    def R(self, action, state): 
        # this is our reward function 
        pass



            