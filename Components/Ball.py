# @Author: shounak
# @Date:   2023-02-01T20:01:59-08:00
# @Email:  shounak@stanford.edu
# @Filename: Ball.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:33:57-08:00

import ursina
import numpy as np

# NOTE: 1.0 for naïve implementation, and lower for higher-level implementations
from Table import TABLE_DIMENSIONS
ELASTICITY_FACTOR = 1.0
# NOTE: For naïve implementation, this value is not used.
BALL_WEIGHT = 2.7 * 10e-3  # in kilograms


class Ball:
    def __init__(self, elasticity_factor=ELASTICITY_FACTOR,
                 ball_weight=BALL_WEIGHT,
                 start_pos=None
                 ):
        # Note: For naïve implementation, z=0
        assert len(start_pos) == 3 and type(start_pos) == dict  # Should have x, y, z coordinates

        self._elasticity_factor = elasticity_factor
        self._weight = ball_weight
        self._position = start_pos                      # This is where the ball starts, based on player pos
        self._speed = {'speed': 0.}                     # In m/s
        self._velocity = {**self._position, **self._speed}

        self._in_bounds = True

    # def in_bounds(self, ball_position):
    #     assert type(ball_position) == dict and len(ball_position) == 3
    #     for dim, value in ball_position.items():
    #         if TABLE_DIMENSIONS[dim][0] <= value <= TABLE_DIMENSIONS[dim][1]:
    #             return False
    #     return True

    def bounce(self, on_obj):
        """Change the velocity vector when the ball comes in contact with on_obj.
        The elasticity factor of `on_obj` must be taken into account.
        The incoming velocity vector (AKA, the private variables @ the time of collision) should be transformed as follows:
        NEW                 OLD
        self._position.x'   -1. * self._position.x

        """
    

    # TODO: Need to check whether ball came in contact

    # EOF
