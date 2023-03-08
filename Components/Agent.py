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

from Components.Ball import Ball
import numpy as np
"""
Description: Agent Class with general variables
"""
class Agent: 
    def __init__(self, position, isRL,
                temporal_latency=TEMPORAL_LATENCY, 
                agent_velocity=AGENT_VELOCITY, 
                max_hit_speed=AGENT_HIT_SPEED):
        self.position = position
        self.maximum_velocity = MAX_VELOCITY
        self.minimum_velocity = MIN_VELOCITY
        self.temporal_latency = temporal_latency
        self.velocity = agent_velocity
        self.max_hit_speed = max_hit_speed
        self.lateral_tolerance = .5
        self.depth_tolerance = .5
        self.direction = 1 if self.position["depth"] == 0 else (-1)
    
    # can only move laterally for now
    def _move(self, new_lateral):
        if new_lateral < 0: 
            self.position["lateral"] = 0
        elif new_lateral > 5: 
            self.position["lateral"] = 5
        else: 
            self.position["lateral"] = new_lateral


    def _defaultHit(self, leftBound, rightBound, game_ball:Ball, epsilon=0): 
        assert epsilon >= 0
        # relative to player
        left_lateral = leftBound - self.position["lateral"]  # distance from x = 0
        right_lateral = rightBound - self.position["lateral"]  # distance from x = 5

        ball_to_other_end = 9 - game_ball._position["depth"] if self.direction == 1 else game_ball._position["depth"]  # distance between ball and the other 

        depth_velocity = self.direction * np.random.uniform(.25, self.max_hit_speed)  # randomly sample depth velocity

        time_to_other_end = ball_to_other_end/abs(depth_velocity)  # how much time until ball gets to the other end

        # now calculate possible lateral_velocity params
        left_velocity = left_lateral/time_to_other_end  # max left_lateral velocity that can be applied
        right_velocity = right_lateral/time_to_other_end        # max right_lateral velcity that can be applied

        # sample from left and right
        lateral_velocity = np.random.uniform(left_velocity - epsilon, right_velocity + epsilon)

        newVelocity = {
            "lateral": lateral_velocity,  
            "vertical": 0, 
            "depth": depth_velocity, 
            "speed": 0
        }

        return newVelocity

        