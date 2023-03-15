# TODO: Need file-string

def inBounds(ball, table, dim):
    assert dim in ("lateral", "depth")
    # `ball` and `table` are each classes.
    assert (len(ball._position) == 3
            and type(ball._position) == dict
            and sorted(list(ball._position.keys())) == sorted(["lateral", "vertical", "depth"]))
    
    # TODO: Note: this following code is NOT generalizable to 3D
    
    def __inside(ball, table, dim=dim):
        return table._true_boundaries[dim][0] <= ball._position[dim] <= table._true_boundaries[dim][1]

    return __inside(ball, table, dim=dim)


    # for dim, value in ball._position.items():
    #     # TODO: Temporary override when dim="vertical". We don't care about ever restricting height of ball, yet.
    #     if dim == "vertical":
    #         continue
    #     # print(dim, ' ', value)
    #     # If the ball is not in-bounds in this dimension, then the ball is immediately out of bounds.
    #     if not (table._true_boundaries[dim][0] <= value <= table._true_boundaries[dim][1]):
    #         # print('here')
    #         return False

def getAgentData(agentObject):
    return {"position": agentObject.position, "state": str(bool) }

def storeLog(FirstMover, Game_AIAgent, Game_RLAgent, Game_Ball):
    ACTION_LOG_T = {"NextMover": FirstMover._id, "Action": "hit"}
    VISUAL_LOG_T = {}
    # TODO: The "state" is hardcoded since we don't care about this too much for the visualization
    VISUAL_LOG_T['AI'] = {"position": Game_AIAgent.position.copy(), "state": "true"}
    VISUAL_LOG_T['RL'] = {"position": Game_RLAgent.position.copy(), "state": "false"}
    VISUAL_LOG_T['Ball'] = {"position": Game_Ball._position.copy()}

    return ACTION_LOG_T, VISUAL_LOG_T