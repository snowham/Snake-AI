# Snake-AI

I created a Snake game in Python using PyGame, and had a Q-Learning AI learn to play the game.

If you want to test out this code:
- Clone the repository
- To play the game yourself, run game.py
- To train an AI agent to play the game and watch it learn, run ql_train.py. It will play 20000 games, gradually getting better at the game, and at the end, it will show a graph of how well it learned. If you don't want to wait for the AI to train, I have added an already-trained agent into this repository so that you don't have to run this.
- Once trained, to watch the AI play 10 games and then show a graph of each game's score, run ql_game.py

I plan on training a Deep Q Network that will input the whole Snake grid each frame, and hopefully it will get a much better score than the Q-Learning agent.
