# @Author: shounak
# @Date:   2023-02-01T20:02:18-08:00
# @Email:  shounak@stanford.edu
# @Filename: RLAgent.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:03:33-08:00

# EOF

from Components.Agent import Agent

class RLAgent(Agent):
    def __init__(self, position, perception_latency=..., max_movement_speed=..., max_hit_speed=..., t=1):
        super().__init__(position, False, perception_latency, max_movement_speed, max_hit_speed)
        self._id = "RL"
        self.t = t  # specifies time interval: seconds. By Defualt
