# @Author: shounak
# @Date:   2023-02-01T20:01:45-08:00
# @Email:  shounak@stanford.edu
# @Filename: Table.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T20:31:25-08:00

# NOTE: 1.0 for naïve implementation, and lower for higher-level implementations
ELASTICITY_FACTOR = 1.0
# 5 ft wide, 9 ft long, 3 ft above table is acceptable
TABLE_DIMENSIONS = {'x': (0, 5),
                    'y': (0, 9),
                    'z': (0, 3)}
# ACCEPTABLE_DEVIATIONS = (0.5, 0.5)


class Table:
    def __init__(self, elasticity_factor=ELASTICITY_FACTOR, table_dims=TABLE_DIMENSIONS):
        self._elasticity_factor = elasticity_factor
        self._true_boundaries = table_dims
        # self._allowed_deviations = {'x': ACCEPTABLE_DEVIATIONS[0],
        #                             'y': ACCEPTABLE_DEVIATIONS[1]}

# EOF
