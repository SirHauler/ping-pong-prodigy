# @Author: shounak
# @Date:   2023-02-01T20:02:28-08:00
# @Email:  shounak@stanford.edu
# @Filename: AIAgent.py
# @Last modified by:   shounak
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

    # TODO: SetVelocity Function Updates
    def hit(self, Ball:Ball, serve=False): 
        """
        Follows a randomized policy in order to update ball. 
        Args:
            ball (Ball): Ball Class

        Returns: 
            None
        """
        if (serve):
            # negative or positive velocity? 
            speed = np.random.uniform(0, self.max_hit_speed)
            speed = speed if self.position["depth"] == 0 else (-1) * speed

            # init all but only update depth
            new_depth = 0
            
            if speed < 0: 
                new_depth = self.position["depth"] - 1
            else: 
                new_depth = self.position["depth"] + 1

            velocity = {
                "lateral": self.position["lateral"], 
                "vertical": self.position["vertical"], 
                "depth": new_depth,   # only update depth for direction
                "speed": speed
            }
            Ball.setVelocity(newVelocity=velocity)
        else: 
            dir_mod_x = .2
            dir_mod_y = 1
            ball_x, ball_y = Ball._position["lateral"], Ball._position["depth"]
            
            min_x = ball_x - dir_mod_x
            max_x = ball_x + dir_mod_x

            # sample x direction & update directions
            new_lateral, new_depth = np.random.uniform(min_x, max_x), ball_y + dir_mod_y

            # sample hit speed
            hit_speed = np.random.uniform(0, self.max_hit_speed)
            newVelocity = {
                "lateral": new_lateral, 
                "vertical": 0,  # leave at 0 for 2D Implementation
                "depth": new_depth, 
                "speed": hit_speed
            }

            Ball.setVelocity(newVelocity=newVelocity)
            self.remaining_latency = self.temporal_latency  # reset the temporal latency
            # TODO: Update Ball Velocity Vector, call Ball.update() method


    
    def performAction(self, Ball:Ball, force=None):  #TODO: Make sure to handle case where force = "hit"
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
            self.hit(Ball=Ball, serve=True)


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
            _, self.ball_lateral, self.time_to_ball = self.projectForward(Ball)
            self.can_see = True

        
        self.time_to_ball -= t

        
        # got there before the ball did :p
        if (self.ball_lateral - self.position["lateral"] == 0 and self.time_to_ball <= 0): # TODO: Check the time aswell
            self.hit(Ball=Ball)
            return HIT
 
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
        
        if (self.ball_lateral - self.position["lateral"]== 0 and self.time_to_ball <= 0):
            self.hit(Ball=Ball)
            return HIT

        return MOVE
        

        # TODO: will it arrive in time to hit the ball?
    
    def projectForward(self, Ball:Ball): 
        """
        Projects the game ball forward and predicts whether or not 
        the agent will reach the ball
        """                
        ball_pos = Ball._position
        ball_velocity = Ball._velocity
        
        # player points
        A = (0, 9)
        B = (5, 9)
        # ball points
        C = (ball_velocity["lateral"], ball_velocity["depth"]) # x, y
        D = (ball_pos["lateral"], ball_pos["depth"]) # x, y


        will_interesect, x, y = self.lineIntersection(A, B, C, D)

        # print("My prediction of the ball: ", x, " ", y)

        future_pos_of_ball = (x, y)
        time_to_ball = self.timeToBall(D, future_pos_of_ball, Ball._velocity["speed"])

        # print("Time to get there: ", time_to_ball)

        # TODO: UPDATE position representation of player


        # now calculate time to get there, regardless of if we will make it
        

        if (will_interesect): 
            return True, x, time_to_ball
        
        return False, -1, -1

    

    def lineIntersection(self, A, B, C, D): 
        """
        Provide 4 points with the first 2 corresponding
        to one line and the next two to another.

        Args:
            A (tuple): point
            B (tuple): point
            C (tuple): point
            D (tuple): point
        """
        xdiff = (A[0] - B[0], C[0] - D[0])
        ydiff = (A[1] - B[1], C[1] - D[1])

        def det (a, b): 
            return a[0] * b[1] - a[1] * b[0]
        
        div = det(xdiff, ydiff)
        
        if div == 0: 
            return False, -1, -1  # lines are parallel and will not intersect
        
        d = (det(A, B), det(C, D))

        x = det(d, xdiff) / div

        y = det(d, ydiff) / div

        return True, x, y
    
    def timeToBall(self, A, B, ball_velocity): 
        """
        Calculates the amount of time needed to
        reach the ball given the current velocity
        of the ball and its position. 

        Args:
            A (tuple): point
            B (tuple): point
        """
        a = abs(A[0] - B[0])
        b = abs(A[1] - B[1])

        d = np.sqrt(a**2 + b**2)
        time = d/ball_velocity

        return time



        
Game_Table = Table()

Game_AIAgent = AIAgent(position = {"lateral": 2.5,
                                "vertical": 0,
                                "depth": 9},
                perception_latency = 0.5, # seconds
                max_movement_speed = 0.5, # m/s
                max_hit_speed = 1 )       # m/s

Game_Ball = Ball(start_pos={"lateral": 2.5,
                            "vertical": 0, 
                            "depth": 9})

direction = {"lateral": 2.5,
            "vertical": 0, 
            "depth": 8}

speed = {"speed": 1}

Game_Ball._velocity = {**direction, **speed}

# for i in range(9):
#     print("-------------------------------------------")
#     print("Time Step: ", i + 1)
#     print("Player: Before Action: ", Game_AIAgent.position)
#     print("Where the ball is now: ", Game_Ball._position["lateral"], " ", Game_Ball._position["depth"])
#     Game_Ball._position["depth"] += 1
#     print("Ball has moved to: ", Game_Ball._position["lateral"], " ", Game_Ball._position["depth"])
#     action = Game_AIAgent.performAction(Ball=Game_Ball)
#     print("Player: After Action: ", Game_AIAgent.position)
#     print("Ball: Velocity ", Game_Ball._velocity)
#     print("ACTION: ", action)
#     print("-------------------------------------------")
