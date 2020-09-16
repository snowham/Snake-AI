import pygame
from pygame.locals import *
from snake import Snake
from ql_agent import QLAgent
import pickle
import matplotlib.pyplot as plt
import numpy as np
import winsound

pygame.init()
 
fps = 15
fpsClock = pygame.time.Clock()
 
squareSize = 27
gridSize = (15, 15)
width, height = squareSize * gridSize[0], squareSize * gridSize[1]
screen = pygame.display.set_mode((width, height))

agent = QLAgent()
try:
    with open('ql_agent.pickle', 'rb') as q_table:
        agent.q_table = pickle.load(q_table)
except:
    print("Q_Table not found. First run ql_train.py")
    pygame.quit()
    quit()
agent.exploration_rate = 0

snake = Snake(gridSize)

scores = []

for episodeCount in range(agent.testEpisodes):
    snake = Snake(gridSize)
    state = snake.getState()

    while True:
        screen.fill((51, 51, 51))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        action = agent.predict_action(state)
        if action == 1 and snake.dir == 'nope':
            pass
        elif action == 2 and snake.dir != 'l':
            snake.dir = 'r'
        elif action == 1 and snake.dir != 'r':
            snake.dir = 'l'
        elif action == 0 and snake.dir != 'd':
            snake.dir = 'u'
        elif action == 3 and snake.dir != 'u':
            snake.dir = 'd'

        snake.update()
        new_state = snake.getState()
        reward = snake.getReward()

        agent.update_q_table(state, action, new_state, reward)

        state = new_state

        if snake.isDead:
            winsound.PlaySound('snake_dead.wav', winsound.SND_ALIAS)
            break

        snake.draw(screen, squareSize)
        pygame.display.flip()
        fpsClock.tick(fps)
    
    scores.append(len(snake.pos)-4)

pygame.quit()
avgScores = np.split(np.array(scores), agent.testEpisodes)
plt.plot(np.sum(avgScores, 1))

plt.show()