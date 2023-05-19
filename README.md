# ping-pong-prodigy

2D Simulation of a Ping-Pong Match! This repo contains 3 Models each containing weights for a Reinforcement Learning agent trained on a different nubmer of games (5000, 6000, and 7000 games). The 7000 gamem model performs best and outperforms an AI Agent (hard-coded opponent, with a 5% error rate in its moves). 


https://github.com/SirHauler/ping-pong-prodigy/assets/62616045/2ae1504e-a1e0-499f-9572-05db026b68f0



## AI Agent

Hard Coded Agent that can forward simulate the action in order to calculate the best move. Theoretically this agent is perfect but an epsilon is introduced as noise which allows for mistakes. 

## RL Agent

An Agent trained using Actor-Critic methods (through Keras & Tensorflow). This agent is then trained on x amount of games in order to learn how to play the game against a much more capable opponent. 


### File Structure
`\_accessories` is for any utility/helper functions used across all files (e.g. save image, file IO, etc.)

`Components` contains class definitions for everything used in the game (e.g. players, board, etc.)

`Extracontent` are just file(s) that we made but are no longer used, or code snippets that are no longer used (but might be useful)

`Logs` stores positions of moving Components w.r.t. time for debugging purpose (and maybe visualization)

`Visualizer Components` contains class definitions + functions that visualizes a match/interaction

`run_match.py` is the "glue": it actually...runs...the match. Pulls from `Components` + `\_accessories` to do its thing.

`visualizer.py` is the code that generates visualizations and saves them to the file. Pulls from `Visualizer Components` and `Logs` (?)
