# @Author: shounak
# @Date:   2023-02-01T20:02:18-08:00
# @Email:  shounak@stanford.edu
# @Filename: RLAgent.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:03:33-08:00

# EOF

from Agent import Agent

class RLAgent(Agent):
    def __init__(self, lateral, vertical, depth, temporal_latency=..., agent_velocity=..., t=1):
        super().__init__(lateral, vertical, depth, True, temporal_latency, agent_velocity)
        self._id = "RL"
        self.t = t  # specifies time interval: seconds. By Defualt
