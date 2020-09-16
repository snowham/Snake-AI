import pygame
from pygame.locals import *
from snake import Snake
import winsound

pygame.init()
 
fps = 12
fpsClock = pygame.time.Clock()
 
squareSize = 27
gridSize = (15, 15)
width, height = squareSize * gridSize[0], squareSize * gridSize[1]
screen = pygame.display.set_mode((width, height))

snake = Snake(gridSize)


while True:
    screen.fill((51, 51, 51))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and snake.dir == 'nope':
        pass
    elif keys[K_RIGHT] and snake.dir != 'l':
        snake.dir = 'r'
    elif keys[K_LEFT] and snake.dir != 'r':
        snake.dir = 'l'
    elif keys[K_UP] and snake.dir != 'd':
        snake.dir = 'u'
    elif keys[K_DOWN] and snake.dir != 'u':
        snake.dir = 'd'
    snake.update()
    if snake.isDead:
        winsound.PlaySound('snake_dead.wav', winsound.SND_ALIAS)
        break
    snake.draw(screen, squareSize)
    pygame.display.flip()
    fpsClock.tick(fps)




font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(f'Your final score was {len(snake.pos)-4}', True, (0, 255, 0), (0, 0, 255))
textRect = text.get_rect()
textRect.center = (width // 2, height // 2)

while True:
    screen.fill((204, 204, 204))
    screen.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()
