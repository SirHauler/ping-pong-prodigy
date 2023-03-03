# @Author: Alex Alvarado-Barahona
# @Date:   2023-02-01T20:02:28-08:00
# @Email:  alexaab@stanford.edu
# @Filename: AIAgent.py
# @Last modified by:   Alex
# @Last modified time: 2023-02-01T20:03:37-08:00

# EOF

from .Agent import Agent
from .Ball import Ball
import numpy as np
from .Table import Table

TEMPORAL_LATENCY = 5  # in seconds

MOVE = "re-adjusted"
CANT_SEE = "no-perception"
HIT = "hit"
"""
AI Agent using a Randomized Policy: 
1. Creates Randomized Vectors
"""
class AIAgent(Agent):
    """
    Initialize AI Agent with following rules: 
    1. Will Move Towards Ball Regardless of if it will make it
    2. Knows exactly where the ball is and where it will move to
    3. If it can hit the ball it will always choose to do so

    Args:
        Agent (Agent): Agent Class
    """
    def __init__(self, position, perception_latency=..., max_movement_speed=..., max_hit_speed=..., t=1):
        super().__init__(position, False, perception_latency, max_movement_speed, max_hit_speed)
        self.can_hit = False
        self.distance_to_ball = None
        self.ball_lateral = None
        self.remaining_latency = self.temporal_latency
        self.time_to_ball = None
        self._id = "AI"
        self.t = t  # measurement of time: seconds. By Defualt. 
        self.save_t = t
        self.can_see = False
        self.will_make_it = False
        self.direction = 1 if self.position["depth"] == 0 else (-1)

    # TODO: SetVelocity Function Updates
    def hit(self, game_ball: Ball, serve=False): 
        """
        Follows a randomized policy in order to update ball. 
        Args:
            game_ball (Ball): Ball Class

        Returns: 
            None
        """
        if (serve):
            # negative or positive velocity? 
            speed = np.random.uniform(.5, self.max_hit_speed)
            speed = speed if self.position["depth"] == 0 else (-1) * speed

            velocity = {
                "lateral": 0, 
                "vertical": 0, 
                "depth": (-1 if speed < 0 else 1) * speed,
                "speed": speed
            }
            game_ball.setVelocity(newVelocity=velocity)

        # hit the ball in a random location in bounds! # TODO: Update to allow the ball to not be perfectly hit!
        else: 
            
            left_lateral = self.position["lateral"]  # distance from x = 0
            right_lateral = 5 - self.position["lateral"]  # distance from x = 5

            ball_to_other_end = 9 - game_ball._position["depth"] if self.direction == 1 else game_ball._position["depth"]  # distance between ball and the other 
            
            depth_velocity = self.direction * np.random.uniform(0, self.max_hit_speed)  # randomly sample depth velocity

            time_to_other_end = ball_to_other_end/depth_velocity  # how much time until ball gets to the other end

            # now calculate possible lateral_velocity params
            left_velocity = (-1) * left_lateral/time_to_other_end  # max left_lateral velocity that can be applied
            right_velocity = right_lateral/time_to_other_end        # max right_lateral velcity that can be applied

            # sample from left and right
            lateral_velocity = np.random.uniform(left_velocity, right_velocity)

            newVelocity = {
                "lateral": lateral_velocity,  
                "vertical": 0, 
                "depth": depth_velocity, 
                "speed": 0
            }


            game_ball.setVelocity(newVelocity=newVelocity)
            self.remaining_latency = self.temporal_latency  # reset the temporal latency
        
        # reset perception
        self.can_see = False


    
    def performAction(self, game_ball: Ball, force=None): 
        """
        Follows policy in order to perform an action
        Args:
            Ball (Class): Current Ball 

        Returns:
            action (str): Str denoting the action taken
        """
        t = self.t  # time interval that has passed

        # serve if prompted
        if (force == "hit"): 
            self.hit(game_ball, serve=True)
            return "hit"

        # cannot see yet
        if self.remaining_latency > self.t: 
            self.remaining_latency -= self.t
            return CANT_SEE
        else: 
            # you can see but time interval 
            t = self.t - self.remaining_latency
            self.remaining_latency = 0
        
        # project forward to see if Agent can move in time
        if not self.can_see:
            _, self.ball_lateral, self.time_to_ball, self.will_make_it = self.projectForward(game_ball)
            self.can_see = True

        
        self.time_to_ball -= t

        
        # got there before the ball did :p
        
        if (self.direction == 1): 
            if (self.position["depth"] - game_ball._position["depth"] >= 0 and self.will_make_it and self.time_to_ball <= 0): 
                self.hit(game_ball=game_ball)
                return HIT
        else: 
            if (self.position["depth"] - game_ball._position["depth"] <= 0 and self.will_make_it and self.time_to_ball <= 0): 
                self.hit(game_ball=game_ball)
                return HIT


        # TODO: tolerance built in for hitting

 
        # regardless of if they will make it, start moving towards ball
        if abs(self.ball_lateral - self.position["lateral"]) > 0: 
            
            # get one time step closer to target position
            sign = 1 if self.ball_lateral - self.position["lateral"] > 0 else -1

            # most ground AI can cover in a single time step
            max_distance = abs(self.velocity * t)  

            # you are close enough to move exactly to the right spot
            if (max_distance > abs(self.ball_lateral - self.position["lateral"])): 
                
                # respect the boundaries of the board
                if (self.ball_lateral < 0):
                    self.position["lateral"] = 0
                elif (self.ball_lateral > 5): 
                    self.position["lateral"] = 5
                else: 
                    self.position["lateral"] = self.ball_lateral
            else: 
                # move max_distance
                self.position["lateral"] += max_distance * sign
            
            # you are in the right position 
        
        if (self.direction == 1): 
            if (self.position["depth"] - game_ball._position["depth"] >= 0 and self.will_make_it and self.time_to_ball <= 0): 
                self.hit(game_ball=game_ball)
                return HIT
        else: 
            if (self.position["depth"] - game_ball._position["depth"] <= 0 and self.will_make_it and self.time_to_ball <= 0): 
                self.hit(game_ball=game_ball)
                return HIT

        return MOVE
        

    # TODO: update so that x component of velocity is reflected in time calculation ---- I think this if fine b/c I use the velocity will give me the other point for the calulation. Just in case I will keep this in here. 
    def projectForward(self, game_ball: Ball): 
        """
        Projects the game ball forward and predicts whether or not 
        the agent will reach the ball
        """                
        ball_pos = game_ball._position
        ball_velocity = game_ball._velocity
        
        # player points -- dependent on which side they are on
        A = (0, 0) if self.position["depth"] == 0 else (0, 9)
        B = (0, 5) if self.position["depth"] == 0 else (5, 9)
        # ball points
        C = (ball_pos["lateral"] + ball_velocity["lateral"], ball_pos["depth"] + ball_velocity["depth"]) # x, y
        D = (ball_pos["lateral"], ball_pos["depth"]) # x, y

        will_interesect, x, y = self.lineIntersection(game_ball)

        # print("My prediction of the ball: ", x, " ", y)

        future_pos_of_ball = (x, y)
        time_to_ball = self.timeToBall(D, future_pos_of_ball, ball_velocity["depth"])

        # will you make it to the ball? 
        distance_to_ball = abs(x - self.position["lateral"])
        players_time_to_ball = distance_to_ball/self.maximum_velocity
        will_make_it = False
        if time_to_ball - players_time_to_ball >= 0: 
            will_make_it = True

        # TODO: UPDATE position representation of player


        # now calculate time to get there, regardless of if we will make it
        

        if (will_interesect): 
            return True, x, time_to_ball, will_make_it
        
        return False, -1, -1, False

    

    def lineIntersection(self, game_ball:Ball): 
        """
        Provide 4 points with the first 2 corresponding
        to one line and the next two to another.

        Args:
            A (tuple): point
            B (tuple): point
            C (tuple): point
            D (tuple): point
        """
        
        # ydiff between player and ball 
        ydiff = game_ball._position["depth"] if self.direction == 1 else self.position["depth"] - game_ball._position["depth"]
        game_y_velocity = game_ball._velocity["depth"]

        time_ball_to_other_end =abs(ydiff/game_y_velocity)

        x = game_ball._position["lateral"] + game_ball._velocity["lateral"] * time_ball_to_other_end
        y = 0 if self.direction == 1 else 9

        return True, x, y


    
    def timeToBall(self, A, B, ball_depth_velocity): 
        """
        Calculates the amount of time needed to
        reach the ball given the current velocity
        of the ball and its position. 

        Args:
            A (tuple): point
            B (tuple): point
        """
        ydiff = abs(A[1] - B[1])
        return abs(ydiff/ball_depth_velocity)  # time


# Game_Table = Table()

# Game_AIAgent = AIAgent(position = {"lateral": 2.5,
#                                 "vertical": 0,
#                                 "depth": 9},
#                 perception_latency = 0.5, # seconds
#                 max_movement_speed = 0.5, # m/s
#                 max_hit_speed = 1 )       # m/s

# Game_Ball = Ball(start_pos={"lateral": 2.5,
#                             "vertical": 0, 
#                             "depth": 9})

# direction = {"lateral": 2.5,
#             "vertical": 0, 
#             "depth": 8}

# speed = {"speed": 1}

# Game_Ball._velocity = {**direction, **speed}

# for i in range(7):
#     print("-------------------------------------------")
#     print("Time Step: ", i + 1)
#     print("Player: Before Action: ", Game_AIAgent.position)
#     print("Where the ball is now: ", Game_Ball._position["lateral"], " ", Game_Ball._position["depth"])
#     Game_Ball._position["depth"] += 1
#     print("Ball has moved to: ", Game_Ball._position["lateral"], " ", Game_Ball._position["depth"])
#     action = Game_AIAgent.performAction(game_ball=Game_Ball)
#     print("Player: After Action: ", Game_AIAgent.position)
#     print("Ball: Velocity ", Game_Ball._velocity)
#     print("ACTION: ", action)
#     print("-------------------------------------------")
