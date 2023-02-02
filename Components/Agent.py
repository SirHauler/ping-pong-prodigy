# import Table in order to define where player should be

TEMPORAL_LATENCY = .5 # TODO
AGENT_VELOCITY = 1    # TODO

class Agent: 
    def __init__(self, lateral, vertical, depth, 
                temporal_latency=TEMPORAL_LATENCY, 
                agent_velocity=AGENT_VELOCITY):
        self.lateral = lateral  # TODO
        self.vertical = vertical  # TODO
        self.depth = depth  # TODO
        self.temporal_latency = temporal_latency
        self.agent_velocity = agent_velocity
    
        

        