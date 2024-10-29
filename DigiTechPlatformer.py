import random #imports random
import pygame #imports pygame library
print("Hello World") #prints "Hello World"

#initialize game
pygame.init()


##Add definitions:##
class Ball:
    def __init__(self):
        self.xpos = 200
        self.ypos = 200
        self.width = 50
        self.height = 50
        self.color = (160, 0, 0)
        self.ball = pygame.draw.ellipse(screen, self.color, [self.xpos, self.ypos, self.width, self.height])


#Window Settings
screen = pygame.display.set_mode((700, 500)) #window dimensions (W, H)
pygame.display.set_caption("[Insert Game Window Name]") #window title
clock = pygame.time.Clock() #clock
running = True #status of game running

#Main game loop

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#Game logic
  
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#0230e4")

    # RENDER YOUR GAME HERE
    ball = Ball()
    key_input = pygame.key.get_pressed()
    if key_input == [pygame.K_LEFT]:
        Ball.xpos -= 10
    if key_input == [pygame.K_RIGHT]:
        Ball.xpos += 10
    if key_input == [pygame.K_UP]:
        Ball.ypos -= 10
    if key_input == [pygame.K_DOWN]:
        Ball.ypos += 10

    # updates display
    pygame.display.update()

    clock.tick(30)  # limits FPS to 30

pygame.quit()