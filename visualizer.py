# @Author: shounak
# @Date:   2023-02-01T19:51:52-08:00
# @Email:  shounak@stanford.edu
# @Filename: visualizer.py
# @Last modified by:   shounak
# @Last modified time: 2023-02-01T19:51:58-08:00

"""
>> Requirements to visualize a game:

Fixed artifacts include:
> Table
> Half-way line
> Dotted latency markers

At every given time step, we need the changing position^ of:
> AI + RL Agents
> Ball
> GREEN for player who will have to hit the ball, RED for player who just finished hitting the ball

Process:
> Visualization log file is in format:
{time_step: {"AI": {"position": {"lateral": int, "vertical": int, "depth": int},
                   "state": str(bool) },
             "RL": {"position": {"lateral": int, "vertical": int, "depth": int},
                   "state": str(bool) }},
             "Ball": {"position": {"lateral": int, "vertical": int, "depth": int} }}

> Assumptions:
AI is on the bottom.
RL is on the top.
"""

import numpy as np
import random
from Components.Table import TABLE_DIMENSIONS
import matplotlib.pyplot as plt
from VizComponents.topView import _saveTopView
from VizComponents._accessories import _make_video, _prepare_directory
import json

def _dummy_log_generator(dims=2):
    LOG = {}
    AI_pos = {"lateral": None, "vertical": None, "depth": None}
    RL_pos = {"lateral": None, "vertical": None, "depth": None}
    Ball_pos = {"lateral": None, "vertical": None, "depth": None}
    
    if dims == 2:
        # For AI Agent
        AI_pos['lateral'] = np.concatenate([np.arange(*TABLE_DIMENSIONS['lateral'], 0.1), 
                                            np.arange(*TABLE_DIMENSIONS['lateral'], 0.1)[::-1]])
        AI_pos['depth'] = np.ones(len(AI_pos['lateral'])) * min(TABLE_DIMENSIONS['depth'])
        # For RL Agent
        RL_pos['lateral'] = np.concatenate([np.arange(*TABLE_DIMENSIONS['lateral'], 0.1), 
                                            np.arange(*TABLE_DIMENSIONS['lateral'], 0.1)[::-1]])
        RL_pos['depth'] = np.ones(len(RL_pos['lateral'])) * max(TABLE_DIMENSIONS['depth'])
        # For Ball
        Ball_pos['lateral'] = np.array([random.uniform(*TABLE_DIMENSIONS['lateral']) for i in range(len(RL_pos['depth']))])
        Ball_pos['depth'] = np.array([random.uniform(*TABLE_DIMENSIONS['depth']) for i in range(len(RL_pos['depth']))])

        def _retrieve_position(time_step, obj_type):
            if obj_type == "AI":
                return {"position": {"lateral": AI_pos['lateral'][time_step], "vertical": 0, "depth": AI_pos['depth'][time_step]},
                        "state": "true"}
            elif obj_type == "RL":
                return {"position": {"lateral": RL_pos['lateral'][time_step], "vertical": 0, "depth": RL_pos['depth'][time_step]},
                        "state": "false"}
            elif obj_type == "Ball":
                return {"position": {"lateral": Ball_pos['lateral'][time_step], "vertical": 0, "depth": Ball_pos['depth'][time_step]}}
            return ValueError("Bad Value.")

        # Make the dummy log
        for time_step in range(0, 100):
            LOG[time_step] = {}
            LOG[time_step]["AI"] = _retrieve_position(time_step, "AI")
            LOG[time_step]["RL"] = _retrieve_position(time_step, "RL")
            LOG[time_step]["Ball"] = _retrieve_position(time_step, "Ball")
    elif dims == 3:
        raise NotImplementedError("We haven't implemented dummy dataset generation for 3D yet!")
    else:
        raise ValueError("4d ping pong - what're you on bro???")
    
    return LOG


def _2d_visualization(LOG, **kwargs):
    fps, picture_folder = kwargs["fps"], kwargs.get("picture_folder", "pictures")
    # Make pictures directory
    _prepare_directory(picture_folder=picture_folder)
    
    # Actually make the pictures based on log
    for time_step, LOG_SUBDATA in LOG.items():
        # > Top View
        _saveTopView(LOG_SUBDATA, save_prefix=str(time_step), picture_folder=picture_folder)
        # > Side View
        # TODO: Will do later (not really useful for 2D).
        # > Player View
        # TODO: Will do later (not really useful for 2D).
        # print(LOG_SUBDATA["Ball"]["position"])
    print("Saved all pictures.\n")

    # Make video
    _make_video(picture_folder=picture_folder, video_folder="videos", fps=fps, prefix='topView')

# TODO: Add perception latency dashed line

def log_to_visualization(LOG, fps=60, dims=2):
    if dims == 2:
        _2d_visualization(LOG, fps=fps, picture_folder="last_pictures")
        pass
    elif dims == 3:
        # _3d_visualization(LOG, fps=60, dims=2)
        raise NotImplementedError("We haven't implemented viz generation for 3D yet!")
    else:
        raise ValueError("4d viz - what're you on bro???")

if __name__ == "__main__":
    # LOG = _dummy_log_generator()
    with open("Logs/VISUAL_LOG.json", "r") as fp:
        LOG = json.load(fp)

    log_to_visualization(LOG, fps=60, dims=2)

# EOF
