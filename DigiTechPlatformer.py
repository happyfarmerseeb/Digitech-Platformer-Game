import random #imports random
import pygame #imports pygame library
print("Hello World") #prints "Hello World"

#initialize game
pygame.init()

#define some important values (default colours, screen width and screen height, etc.)#
screen_width = 1200
screen_height = 500
font = pygame.font.SysFont("Calibri", 25)

##Add ball (player) definitions:##
ball_xpos = 200
ball_ypos = 200
ball_width = 50
ball_height = 50
ball_color = (160, 0, 0)
ballxchange = 0
ballychange = 0
direction = "null"


#Window Settings
screen = pygame.display.set_mode((screen_width, screen_height)) #window dimensions (W, H)
pygame.display.set_caption("[Insert Game Window Name]") #window title
clock = pygame.time.Clock() #clock
running = True #status of game running

#Main game loop

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key_input = event.key
            if key_input == pygame.K_LEFT:
                ballxchange = -10
            if key_input == pygame.K_RIGHT:
                ballxchange = 10
            if key_input == pygame.K_UP:
                ballychange = -10
            if key_input == pygame.K_DOWN:
                ballychange = 10
                           
        if event.type == pygame.KEYUP:
            key_end = event.key
            if key_end == key_input:
                ballxchange = 0
                ballychange = 0
            elif key_end == pygame.K_LEFT:
                ballxchange += 10
            elif key_end == pygame.K_RIGHT:
                ballxchange -= 10
            elif key_end == pygame.K_UP:
                ballychange += 10
            elif key_end == pygame.K_DOWN:
                ballychange -= 10

       #     elif (key_end == pygame.K_LEFT or pygame.K_RIGHT) and (key_input != pygame.K_LEFT or pygame.K_RIGHT):
        #        ballxchange == 0
         #   elif (key_end == pygame.K_UP or pygame.K_DOWN) and (key_input != pygame.K_UP or pygame.K_DOWN):
          #      ballxchange == 0
                
        
    # pygame.QUIT event means the user clicked X to close your window
    

#Game logic
  
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#0230e4")
    pygame.draw.ellipse(screen, ball_color, (ball_xpos, ball_ypos, ball_width, ball_height))
    # RENDER YOUR GAME HERE

#Position-responsive ball position label:    ball_xpos-20(((screen_width/2)-ball_xpos)/abs((screen_width/2)-ball_xpos)),ball_ypos-20(((screen_height/2)-ball_ypos)/abs((screen_height/2)-ball_ypos))
    
    # updates display
    if ballxchange != 0 or ballychange != 0:
        ball_xpos += ballxchange
        ball_ypos += ballychange
        if ball_xpos < 0:
            ball_xpos = 0
        elif ball_xpos >= screen_width-ball_width:
            ball_xpos = screen_width-ball_width
        
        if ball_ypos < 0:
            ball_ypos = 0
        elif ball_ypos >= screen_height-ball_height:
            ball_ypos = screen_height-ball_height

        
        pygame.draw.ellipse(screen, ball_color, (ball_xpos, ball_ypos, ball_width, ball_height))
    
    xpostext = font.render(f"x-pos: {ball_xpos}", True, (0, 255, 0))
    ypostext = font.render(f"y-pos: {ball_ypos}", True, (0, 255, 0))
    #xlabelpos = [ball_xpos-20(((screen_width/2)-ball_xpos)/abs((screen_width/2)-ball_xpos)),ball_ypos-20(((screen_height/2)-ball_ypos)/abs((screen_height/2)-ball_ypos))]
    #ylabelpos = [300, 300]
    screen.blit(xpostext, [200, 0])
    screen.blit(ypostext, [400, 0])

    pygame.display.update()

    clock.tick(30)  # limits FPS to 30

pygame.quit()