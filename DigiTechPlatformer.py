import random #imports random
import pygame #imports pygame library
print("Hello World") #prints "Hello World"

#initialize game
pygame.init()

#define some important values (default colours, screen width and screen height, etc.)#
screen_width = 1280
screen_height = 720
font = pygame.font.SysFont("Calibri", 25)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

##Add button definitions:##
button_xpos = 1000
button_ypos = 120
button_height = 50
button_width = 150
button_color = GREEN
button_text = "Speed"

##Add ball (player) definitions:##
ball_xpos = 200
ball_ypos = 200
ball_width = 50
ball_height = 50
ball_color = (160, 0, 0)
ballxchange = 0
ballychange = 0
ballvelocity = 10
direction = "null"

##Add ground definitions:##
ground_xpos = 100
ground_ypos = 420
ground_width = 1080
ground_height = 200
ground_color = BLACK


#Window Settings
screen = pygame.display.set_mode((screen_width, screen_height)) #window dimensions (W, H)
pygame.display.set_caption("[Insert Game Window Name]") #window title
clock = pygame.time.Clock() #clock
running = True #status of game running

#Main game loop

while running:
    # poll for events
    inputs = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key_input = event.key
            if key_input == pygame.K_LEFT:
                ballxchange = -ballvelocity
            if key_input == pygame.K_RIGHT:
                ballxchange = ballvelocity
            if key_input == pygame.K_UP:
                ballychange = -ballvelocity
            if key_input == pygame.K_DOWN:
                ballychange = ballvelocity

        if event.type == pygame.KEYUP:
            key_end = event.key
            if key_end == pygame.K_LEFT:
                if abs(ballxchange) > ballvelocity:
                    ballxchange += 2*ballvelocity
                else:
                    ballxchange += ballvelocity
            if key_end == pygame.K_RIGHT:
                if abs(ballxchange) > ballvelocity:
                    ballxchange -= 2*ballvelocity
                else:
                    ballxchange -= ballvelocity
            if key_end == pygame.K_UP:
                if abs(ballychange) > ballvelocity:
                    ballychange += 2*ballvelocity
                else:
                    ballychange += ballvelocity
            if key_end == pygame.K_DOWN:
                if abs(ballychange) > ballvelocity:
                    ballychange -= 2*ballvelocity
                else:
                    ballychange -= ballvelocity

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > button_xpos and mouse_pos[1] > button_ypos and mouse_pos[0] < button_xpos+button_width and mouse_pos[1] < button_ypos+button_height:
                ballvelocity = random.randint(1,100)


       #     elif (key_end == pygame.K_LEFT or pygame.K_RIGHT) and (key_input != pygame.K_LEFT or pygame.K_RIGHT):
        #        ballxchange == 0
         #   elif (key_end == pygame.K_UP or pygame.K_DOWN) and (key_input != pygame.K_UP or pygame.K_DOWN):
          #      ballxchange == 0
                
        
    # pygame.QUIT event means the user clicked X to close your window
    

#Game logic
  
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#0230e4")
    pygame.draw.ellipse(screen, ball_color, (ball_xpos, ball_ypos, ball_width, ball_height))
    ground = pygame.draw.rect(screen, ground_color, (ground_xpos, ground_ypos, ground_width, ground_height), 0, 0, 0) #ground
    button = pygame.draw.rect(screen, button_color, (button_xpos, button_ypos, button_width, button_height), 0, 0, 0)
    button_text = font.render(f"{button_text}", True, BLACK)
    screen.blit(button_text, [button_xpos, button_ypos])
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

#ground collision logic:
        if ball_xpos + ball_width > ground_xpos and ball_xpos + ball_width < ground_xpos + ball_width and ball_ypos > ground_ypos - ball_height and ball_ypos < ground_ypos + ground_height:
            ball_xpos = ground_xpos - ball_width
        if ball_ypos + ball_height > ground_ypos and ball_ypos + ball_height < ground_ypos + ball_height and ball_xpos > ground_xpos - ball_width and ball_xpos < ground_xpos + ground_width:
            ball_ypos = ground_ypos - ball_height
        if ball_xpos < ground_xpos + ground_width and ball_xpos > ground_xpos + ground_width - ball_width and ball_ypos > ground_ypos - ball_height and ball_ypos < ground_ypos + ground_height:
            ball_xpos = ground_xpos + ground_width
        if ball_ypos < ground_ypos + ground_height and ball_ypos > ground_ypos + ground_height - ball_height and ball_xpos > ground_xpos - ball_width and ball_xpos < ground_xpos + ground_width:
            ball_ypos = ground_ypos + ground_height
        
        pygame.draw.ellipse(screen, ball_color, (ball_xpos, ball_ypos, ball_width, ball_height))
    
    xpostext = font.render(f"x-pos: {ball_xpos}", True, (0, 255, 0))
    ypostext = font.render(f"y-pos: {ball_ypos}", True, (0, 255, 0))
    #xlabelpos = [ball_xpos-20(((screen_width/2)-ball_xpos)/abs((screen_width/2)-ball_xpos)),ball_ypos-20(((screen_height/2)-ball_ypos)/abs((screen_height/2)-ball_ypos))]
    #ylabelpos = [300, 300]
    screen.blit(xpostext, [200, 0])
    screen.blit(ypostext, [400, 0])

    pygame.display.update()

    clock.tick(50)  # limits FPS to 50

pygame.quit()