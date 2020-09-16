import pygame
import random

class Snake:
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.pos = [(2, gridSize[1]//2), (3, gridSize[1]//2), (4, gridSize[1]//2), (5, gridSize[1]//2)]
        self.dir = 'nope'
        self.food = (gridSize[0]-5, gridSize[1]//2)
        self.oldFood = (gridSize[0]-5, gridSize[1]//2)
        self.isDead = False
        self.growing = []
        self.stepsSinceEaten = 0
        self.maxSteps = 500
        self.distFromFood = self.food[0] - self.pos[-1][0]
        self.prevDistFromFood = self.food[0] - self.pos[-1][0]

    def move(self):
        if self.dir == 'nope':
            return
        head = self.pos[-1]
        self.pos.pop(0)
        if self.dir == 'r':
            self.pos.append((head[0]+1, head[1]))
        elif self.dir == 'l':
            self.pos.append((head[0]-1, head[1]))
        elif self.dir == 'u':
            self.pos.append((head[0], head[1]-1))
        elif self.dir == 'd':
            self.pos.append((head[0], head[1]+1))

    def collision_detect(self):
        head = self.pos[-1]
        if head[0] < 0 or head[1] < 0 or head[0] >= self.gridSize[0] or head[1] >= self.gridSize[1] or head in self.pos[:-1]:
            return True
        else:
            return False
            
    def getState(self):
        if self.isDead:
            return
        state = ''
        head = self.pos[-1]
        for surrounding in [(head[0], head[1]-1), (head[0]-1, head[1]), (head[0]+1, head[1]), (head[0], head[1]+1)]:
            if surrounding in self.pos or surrounding[0] < 0 or surrounding[0] > self.gridSize[0] or surrounding[1] < 0 or surrounding[1] > self.gridSize[1]:
                state += '1 '
            else:
                state += '0 '
        state += ' 1' if (head[0] > self.food[0] and head[1] > self.food[1]) else ' 0'
        state += ' 1' if (head[0] == self.food[0] and head[1] > self.food[1]) else ' 0'
        state += ' 1' if (head[0] < self.food[0] and head[1] > self.food[1]) else ' 0'
        state += ' 1' if (head[0] > self.food[0] and head[1] == self.food[1]) else ' 0'
        state += ' 1' if (head[0] < self.food[0] and head[1] == self.food[1]) else ' 0'
        state += ' 1' if (head[0] > self.food[0] and head[1] < self.food[1]) else ' 0'
        state += ' 1' if (head[0] == self.food[0] and head[1] < self.food[1]) else ' 0'
        state += ' 1' if (head[0] < self.food[0] and head[1] < self.food[1]) else ' 0'

        return state
    
    def getReward(self):
        reward = 0
        head = self.pos[-1]
        if head == self.food:
            reward += 30
        if self.distFromFood < self.prevDistFromFood:
            reward += 1.5
        elif self.distFromFood >= self.prevDistFromFood:
            reward -= 1.5
        if self.isDead:
            reward -= 100
        return reward

        
    def update(self):
        head = self.pos[-1]
        if self.collision_detect() or self.stepsSinceEaten >= self.maxSteps:
            self.isDead = True
        try:
            if self.growing[0] == self.oldFood:
                self.pos.insert(0, self.oldFood) 
                self.oldFood = self.food
                self.growing.pop(0)
        except:
            pass
        if head == self.food:
            self.growing.append(head)
            self.stepsSinceEaten = 0
            while True:
                self.food = (random.choice(range(self.gridSize[0])), random.choice(range(self.gridSize[1])))
                if self.food not in self.pos:
                    break
        else:
            self.stepsSinceEaten += 1
        self.prevDistFromFood = self.distFromFood
        self.distFromFood = abs(self.food[1] - head[1]) + abs(self.food[0] - head[0])
        self.move()


    # vv this took me ages >:( vv
    def draw(self, screen, squareSize):
        pygame.draw.rect(screen, (205, 0, 0), ((self.food[0]+0.125)*squareSize, (self.food[1]+0.125)*squareSize, squareSize*0.75, squareSize*0.75))

        snakeThinness = 0.25
        for i in range(len(self.pos)):
            c, r = self.pos[i][0], self.pos[i][1]

            if i == 0:
                if c == self.pos[1][0]:
                    if r < self.pos[1][1]:
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, (r+snakeThinness)*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness)*squareSize+1))
                    else:
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, r*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness)*squareSize))
                else:
                    if c < self.pos[1][0]:
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness)*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness)*squareSize+1, (1-snakeThinness)*squareSize))
                    else:
                        pygame.draw.rect(screen, (0, 200, 0), (c*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness)*squareSize))

            elif i == len(self.pos)-1:
                if c == self.pos[-2][0]:
                    if r < self.pos[-2][1]:
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, (r+snakeThinness)*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness)*squareSize+1))
                    else:
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, r*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness)*squareSize))
                else:
                    if c < self.pos[-2][0]:
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness)*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness)*squareSize+1, (1-snakeThinness)*squareSize))
                    else:
                        pygame.draw.rect(screen, (0, 200, 0), (c*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness)*squareSize))

            else:
                if self.pos[i-1][1] == r == self.pos[i+1][1]:
                    pygame.draw.rect(screen, (0, 200, 0), (c*squareSize, (r+snakeThinness*0.5)*squareSize, squareSize, (1-snakeThinness)*squareSize))
                elif self.pos[i-1][0] == c == self.pos[i+1][0]:
                    pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, r*squareSize, (1-snakeThinness)*squareSize, squareSize))
                else:
                    if (self.pos[i-1][0] < c and self.pos[i+1][1] < r) or (self.pos[i-1][1] < r and self.pos[i+1][0] < c):
                        pygame.draw.rect(screen, (0, 200, 0), (c*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness*0.5)*squareSize-1, (1-snakeThinness)*squareSize))
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, r*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness*0.5)*squareSize-1))
                    elif (self.pos[i-1][0] < c and self.pos[i+1][1] > r) or (self.pos[i-1][1] > r and self.pos[i+1][0] < c):
                        pygame.draw.rect(screen, (0, 200, 0), (c*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness*0.5)*squareSize-1, (1-snakeThinness)*squareSize))
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness*0.5)*squareSize+1))
                    elif (self.pos[i-1][1] > r and self.pos[i+1][0] > c) or (self.pos[i-1][0] > c and self.pos[i+1][1] > r):
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness*0.5)*squareSize+1, (1-snakeThinness)*squareSize))
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness*0.5)*squareSize+1))
                    else:
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, (r+snakeThinness*0.5)*squareSize, (1-snakeThinness*0.5)*squareSize+1, (1-snakeThinness)*squareSize))
                        pygame.draw.rect(screen, (0, 200, 0), ((c+snakeThinness*0.5)*squareSize, r*squareSize, (1-snakeThinness)*squareSize, (1-snakeThinness*0.5)*squareSize-1))