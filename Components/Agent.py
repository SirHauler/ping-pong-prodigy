# import Table in order to define where player should be
# from Ball import Ball

TEMPORAL_LATENCY = .5 # TODO
AGENT_VELOCITY = 1    # TODO
AGENT_HIT_SPEED = 1
RLAGENT_START_LATERAL  = .5 # TODO: UPDATE X, Ys
RLAGENT_START_DEPTH = .5
AIAGENT_START_DEPTH = .5
AIAGENT_START_LATERAL = .5
MAX_VELOCITY = 1
MIN_VELOCITY = 0


"""
Description: Agent Class with general variables
"""
class Agent: 
    def __init__(self, position, isRL,
                temporal_latency=TEMPORAL_LATENCY, 
                agent_velocity=AGENT_VELOCITY, 
                max_hit_speed=AGENT_HIT_SPEED):
        
        self.init_position(isRL)
        self.position = position
        self.maximum_velocity = MAX_VELOCITY
        self.minimum_velocity = MIN_VELOCITY
        self.temporal_latency = temporal_latency
        self.velocity = agent_velocity
        self.max_hit_speed = max_hit_speed
        self.lateral_tolerance = .5
        self.depth_tolerance = .5
    
    # can only move laterally for now
    def _move(self, new_lateral):
        if new_lateral < 0: 
            self.position["lateral"] = 0
        elif new_lateral > 5: 
            self.position["lateral"] = 5
        else: 
            self.position["lateral"] = new_lateral

    def init_position(self, isRL):
        if (isRL):
            self.lateral = RLAGENT_START_LATERAL
            self.depth = RLAGENT_START_DEPTH
        else: 
            self.lateral = AIAGENT_START_LATERAL
            self.depth = AIAGENT_START_DEPTH

        