from Components.Table import TABLE_DIMENSIONS
import matplotlib.pyplot as plt

"""
Recall Convention:
> AI is on the bottom.
> RL is on the top.

Note that frame of reference is IDENTICAL for both AI and RL. Depth-values are NOT relative.

"""


# Same 2d image outputs for 2D or 3D game setting.
def _saveTopView(LOG_SUBDATA, save_prefix=None, picture_folder="pictures"):
    # NOTE: `LOG_SUBDATA` is a *single* dictionary for a single time-step, not `LOG`,
    assert save_prefix is not None and save_prefix.isdigit()

    # figsize = (_horizontal, _vertical) = (lateral, depth)
    LATERAL_MIN, LATERAL_MAX = TABLE_DIMENSIONS["lateral"]
    DEPTH_MIN, DEPTH_MAX = TABLE_DIMENSIONS["depth"]

    fig, ax = plt.subplots(figsize=(LATERAL_MAX * 1.5, DEPTH_MAX * 1.5))

    # Mark table
    plt.axis('off')
    _ = plt.xlim([LATERAL_MIN - 0.2, LATERAL_MAX + 0.2])
    _ = plt.ylim([DEPTH_MIN - 0.2, DEPTH_MAX + 0.2])

    # Horizontal line to mark center
    _halfway_depth = max(TABLE_DIMENSIONS["depth"]) / 2
    _ = plt.axhline(y=_halfway_depth, color='b', linestyle='-')

    # Table boundaries
    _ = plt.axvline(x=LATERAL_MIN, color='black', linestyle='-')
    _ = plt.axvline(x=LATERAL_MAX, color='black', linestyle='-')
    _ = plt.axhline(y=DEPTH_MIN, color='black', linestyle='-')
    _ = plt.axhline(y=DEPTH_MAX, color='black', linestyle='-')

    # Draw AI
    c_ai = 'green' if LOG_SUBDATA["AI"]["state"] == "true" else 'red'
    _ = plt.scatter(LOG_SUBDATA["AI"]["position"]["lateral"],
                    LOG_SUBDATA["AI"]["position"]["depth"],
                    c=c_ai,
                    s=180)
    ax.annotate('AI Agent', xy=(LATERAL_MAX / 2, _halfway_depth), xytext=(LATERAL_MAX / 2 - 0.30, DEPTH_MIN - 0.25), size=15)

    # Draw RL
    c_rl = 'green' if LOG_SUBDATA["RL"]["state"] == "true" else 'red'
    _ = plt.scatter(LOG_SUBDATA["RL"]["position"]["lateral"],
                    LOG_SUBDATA["RL"]["position"]["depth"],
                    c=c_rl,
                    s=180)
    ax.annotate('RL Agent', xy=(LATERAL_MAX / 2, _halfway_depth), xytext=(LATERAL_MAX / 2 - 0.30, DEPTH_MAX + 0.25), size=15)

    # Draw Ball
    c_ball = 'yellow'
    _ = plt.scatter(LOG_SUBDATA["Ball"]["position"]["lateral"],
                    LOG_SUBDATA["Ball"]["position"]["depth"],
                    c=c_ball,
                    s=100)

    # Save image
    _ = plt.tight_layout()
    _ = plt.savefig(f"{picture_folder}/{save_prefix}_gameState.jpeg", bbox_inches="tight")
    plt.close()

# def _saveTopView():
#     return 4

# # EOF