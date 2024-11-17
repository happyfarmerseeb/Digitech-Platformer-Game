#pygame class testing
import random #imports random
import pygame #imports pygame library
print("Hello World") #prints "Hello World"

#initialize game
pygame.init()

#define some important values (default colours, screen width and screen height, etc.)#
screen_width = 1280
screen_height = 720
font = pygame.font.SysFont("Calibri", 25)
Red_A_Val = 1
Green_A_Val = 1
Blue_A_Val = 1
RED = (255, 0, 0, Red_A_Val)
GREEN = (0, 255, 0, Green_A_Val)
BLUE = (0, 0, 255, Blue_A_Val)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
gravity = 0.42

class Button:
    def __init__(self, x, y, w, h, colour, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        self.text = text

    def draw(self):
        button = pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h), 0, 0, 0)
        button_text = font.render(f"{self.text}", True, BLACK)
        screen.blit(button_text, [self.x, self.y])     

screen = pygame.display.set_mode((screen_width, screen_height)) #window dimensions (W, H)
pygame.display.set_caption("[Insert Game Window Name]") #window title
clock = pygame.time.Clock() #clock
running = True #status of game running

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    
    
    
    RandButton = Button(1000, 120, 150, 50, GREEN, "Speed")
    RandButton.draw()

    # RENDER YOUR GAME HERE

    pygame.display.update()

    clock.tick(50)  # limits FPS to 50
