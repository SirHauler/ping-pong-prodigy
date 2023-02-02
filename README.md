# ping-pong-prodigy

### File Structure
`\_accessories` is for any utility/helper functions used across all files (e.g. save image, file IO, etc.)

`Components` contains class definitions for everything used in the game (e.g. players, board, etc.)

`Extracontent` are just file(s) that we made but are no longer used, or code snippets that are no longer used (but might be useful)

`Logs` stores positions of moving Components w.r.t. time for debugging purpose (and maybe visualization)

`Visualizer Components` contains class definitions + functions that visualizes a match/interaction

`run_match.py` is the "glue": it actually...runs...the match. Pulls from `Components` + `\_accessories` to do its thing.

`visualizer.py` is the code that generates visualizations and saves them to the file. Pulls from `Visualizer Components` and `Logs` (?)
