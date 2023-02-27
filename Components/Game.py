# @Author: shounak
# @Date:   2023-02-01T20:03:05-08:00
# @Email:  shounak@stanford.edu
# @Filename: Game.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:03:28-08:00

# EOF

from AIAgent import AIAgent
from RLAgent import RLAgent
from Table import Table

"""
What it does: 
* Checks for collisions
* 
"""
class Game:
    def __init__(self, Agent1, Agent2): 
        self.agent1 = Agent1
        self.agent2 = Agent2
    