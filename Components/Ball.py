# @Author: shounak
# @Date:   2023-02-01T20:01:59-08:00
# @Email:  shounak@stanford.edu
# @Filename: Ball.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:33:57-08:00

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
        # NOTE: For naïve implementation, z=0. `start_pos` should have x, y, z coordinates.
        # NOTE: Lateral is x, Vertical is y, and Depth is z.
        assert (len(start_pos) == 3
                and type(start_pos) == dict
                and sorted(list(start_pos.keys())) == sorted(["lateral", "vertical", "depth"]))

        self._elasticity_factor = elasticity_factor
        self._weight = ball_weight
        self._position = start_pos                                  # This is where the ball starts, based on player pos
        self._speed = {'speed': 0.}                                 # In m/s
        self._direction = {"lateral": 0, "vertical": 0, "depth": 0}
        self._velocity = {**self._direction, **self._speed}

    def setVelocity(self, newVelocity: tuple(float)):
        """Sets the guts to a provided newVelocity."""
        assert len(newVelocity) == 4 and sorted(list(newVelocity.keys())) == sorted(["lateral", "vertical", "depth", "speed"])
        self._velocity = newVelocity
    
    def _update_dimwise_position(self, dims=2, step_forward = 1):
        """Helper to `move`. Updates where the ball is in space in 2- or 3-D."""
        if dims == 2:
            # TODO: Vectorize this if we have a performance bottleneck
            for nature in ['lateral', 'vertical']:
                self._position[nature] + self._velocity[nature] * step_forward
        else:
            raise ValueError("Higher dimensions not supported yet.")

    def move(self, step_forward = 1):
        """SEE `_update_dimwise_position` docstring."""
        self._update_dimwise_position(dims=2, step_forward = step_forward)
        # self._update_dimwise_position(dims=3)

    def bounce(self, on_obj):
        """Change the velocity vector when the ball comes in contact with on_obj.
        NOTE: This function is NOT IMPLEMENTED for dims ≥ 3. The `_elasticity_factor` is not applied in 2D.
        ---
        The elasticity factor of `on_obj` must be taken into account.
        The incoming velocity vector (AKA, the private variables @ the time of collision) should be transformed as follows:
        NEW                 OLD
        self._position.x'   -1. * self._position.x
        TODO: Complete mapping for 3D case
        """

    # EOF
