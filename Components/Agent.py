# import Table in order to define where player should be

from Ball import Ball



TEMPORAL_LATENCY = .5 # TODO
AGENT_VELOCITY = 1    # TODO
RLAGENT_START_LATERAL  = .5
RLAGENT_START_DEPTH = .5
AIAGENT_START_DEPTH = .5
AIAGENT_START_LATERAL = .5


"""
Description: Agent Class with general variables
"""
class Agent: 
    def __init__(self, lateral, vertical, depth, isRL,
                temporal_latency=TEMPORAL_LATENCY, 
                agent_velocity=AGENT_VELOCITY):
        
        self.init_position(isRL)
        self.lateral = lateral  # TODO
        self.vertical = vertical  # TODO
        self.depth = depth  # TODO
        self.temporal_latency = temporal_latency
        self.agent_velocity = agent_velocity
    
    def update_pos(self, x, y, z):
        self.lateral = x
        self.vertical = y
        self.depth = z 
    

    def init_position(self, isRL):
        if (isRL):
            self.lateral = RLAGENT_START_LATERAL
            self.depth = RLAGENT_START_DEPTH
        else: 
            self.lateral = AIAGENT_START_LATERAL
            self.depth = AIAGENT_START_DEPTH
    def perform_Action(self, ):
        return 0

        