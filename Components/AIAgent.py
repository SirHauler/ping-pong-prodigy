# @Author: shounak
# @Date:   2023-02-01T20:02:28-08:00
# @Email:  shounak@stanford.edu
# @Filename: AIAgent.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:03:37-08:00

# EOF

from Agent import Agent
from Ball import Ball
import numpy as np

"""
AI Agent using a Randomized Policy: 
1. Creates Randomized Vectors
"""
class AIAgent(Agent):
    """
    Initialize AI Agent using randomized policy

    Args:
        Agent (Agent): Agent Class
    """
    def __init__(self, lateral, vertical, depth, temporal_latency=..., agent_velocity=...):
        super().__init__(lateral, vertical, depth, False, temporal_latency, agent_velocity)

    def hit(self, Ball): 
        """
        Follows a randomized policy in order to update ball. 
        Args:
            ball (Ball): Ball Class

        Returns: 
            None
        """
        vector = np.array([0, 0, 0])
        # TODO: Update Ball Velocity Vector, call Ball.update() method
        return None

    def performAction(self, Ball):
        """
        Follows policy in order to perform an action
        Args:
            Ball (Class): Current Ball 

        Returns:
            None
        """
        return None

