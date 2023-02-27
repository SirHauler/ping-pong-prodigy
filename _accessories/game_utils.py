# TODO: Need file-string

def inBounds(ball, table):
    # `ball` and `table` are each classes.
    assert (len(ball._position) == 3
            and type(ball._position) == dict
            and sorted(list(ball._position.keys())) == sorted(["lateral", "vertical", "depth"]))
    
    for dim, value in ball._position.items():
        # TODO: Temporary override when dim="vertical". We don't care about ever restricting height of ball, yet.
        if dim == "vertical":
            continue
        # If the ball is not in-bounds in this dimension, then the ball is immediately out of bounds.
        if not (table._true_boundaries[dim][0] <= value <= table._true_boundaries[dim][1]):
            return False
    return True