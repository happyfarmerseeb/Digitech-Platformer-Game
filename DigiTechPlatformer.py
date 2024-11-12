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
LastInputs = [False, False, False]
Inputs = [False, False, False]
ball_IV = 0
ball_EV = 0
airtime = 0
ball_max_x_velocity = 10
ball_x_velocity = 0
ball_y_velocity = 0
ball_grounded = False
ball_acceleration = 0
offset = 0
ball_true_x_pos = 200

##Level 1##
L1_Ground_Red_X = 50
L1_Ground_Red_Y = 520
L1_Ground_Red_W = 1080
L1_Ground_Red_H = 200

L1_Ground_Green_X = 1130
L1_Ground_Green_Y = 520
L1_Ground_Green_W = 1080
L1_Ground_Green_H = 200

L1_Ground_Blue_X = 2210
L1_Ground_Blue_Y = 520
L1_Ground_Blue_W = 1080
L1_Ground_Blue_H = 200


##Add ground definitions:##
ground_xpos = 100
ground_ypos = 520
ground_width = L1_Ground_Red_W + L1_Ground_Green_W + L1_Ground_Blue_W
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
    #below code creates an input array which is read later
    LastInputs = Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Inputs[0] = True
            if event.key == pygame.K_RIGHT:
                Inputs[1] = True
            if event.key == pygame.K_UP:
                Inputs[2] = True
	    
        if (Inputs[0] == True and Inputs[1] == True):
            Inputs[0] = LastInputs[1]
            Inputs[1] = LastInputs[0]
		
        if event.type == pygame.KEYUP:         
            if event.key == pygame.K_LEFT:
                 Inputs[0] = False
            if event.key == pygame.K_RIGHT:
                 Inputs[1] = False
            if event.key == pygame.K_UP:
                 Inputs[2] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > button_xpos and mouse_pos[1] > button_ypos and mouse_pos[0] < button_xpos+button_width and mouse_pos[1] < button_ypos+button_height:
                ball_max_x_velocity = random.randint(1,100)
                L1_Ground_Red_X = random.randint(1,400)
                L1_Ground_Red_Y = random.randint(1,300)
                L1_Ground_Red_W = random.randint(1,500)
                L1_Ground_Red_H = random.randint(1,200)

                L1_Ground_Green_X = random.randint(1,400)
                L1_Ground_Green_Y = random.randint(1,300)
                L1_Ground_Green_W = random.randint(1,500)
                L1_Ground_Green_H = random.randint(1,200)

                L1_Ground_Blue_X = random.randint(1,400)
                L1_Ground_Blue_Y = random.randint(1,300)
                L1_Ground_Blue_W = random.randint(1,500)
                L1_Ground_Blue_H = random.randint(1,200)


        

    #end of input array write
    #input array read begin
    #dealing with x acceleration
    if Inputs[0] == True:
        ball_acceleration = -0.5 #makes Left key set leftwards acceleration
    elif Inputs[1] == True:
        ball_acceleration = 0.5 #makes right key set rightwards acceleration
    else:
        if abs(ball_x_velocity)<1: #if velocity is low enough, the game will just set it to 0
            ball_acceleration = 0
            ball_x_velocity = 0
        else: 
            ball_acceleration = -0.04*ball_x_velocity #makes player slow down when there are no inputs due to friction with ground
    #updating x velocity
    ball_x_velocity += ball_acceleration
    #if ball exceeds maximum x velocity:
    if abs(ball_x_velocity) > ball_max_x_velocity:
        ball_x_velocity = ball_max_x_velocity*(ball_x_velocity/abs(ball_x_velocity))


    #dealing with jump inputs (Inputs[2] = True)
    if Inputs[2] == True:
        if ball_grounded == True:
            ball_IV = -15
            airtime = 0
        if ball_grounded == False:
            if airtime >= 75:
                Inputs[2] = False
            airtime += 1
    else:
        ball_IV += 0.5 
        if ball_grounded == True:            
            airtime = 0
            ball_IV = 0
        else:
            airtime += 1
    
    #calculate y velocity of ball
    ball_y_velocity = ball_IV+(airtime*gravity)



       #     elif (key_end == pygame.K_LEFT or pygame.K_RIGHT) and (key_input != pygame.K_LEFT or pygame.K_RIGHT):
        #        ballxchange == 0
         #   elif (key_end == pygame.K_UP or pygame.K_DOWN) and (key_input != pygame.K_UP or pygame.K_DOWN):
          #      ballxchange == 0
                
        
    # pygame.QUIT event means the user clicked X to close your window
    

#Game logic
  
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(WHITE)
    pygame.draw.ellipse(screen, ball_color, (ball_xpos, ball_ypos, ball_width, ball_height))
    ground = pygame.draw.rect(screen, ground_color, (ground_xpos, ground_ypos, ground_width, ground_height), 0, 0, 0) #ground
    
    #Red ground
    L1_Ground_Red = pygame.draw.rect(screen, RED, (L1_Ground_Red_X-ball_true_x_pos+ball_xpos, L1_Ground_Red_Y, L1_Ground_Red_W, L1_Ground_Red_H), 0, 0, 0)
    
    #Green ground
    L1_Ground_Green = pygame.draw.rect(screen, GREEN, (L1_Ground_Green_X-ball_true_x_pos+ball_xpos, L1_Ground_Green_Y, L1_Ground_Green_W, L1_Ground_Green_H), 0, 0, 0)
    
    #Blue ground
    L1_Ground_Blue = pygame.draw.rect(screen, BLUE, (L1_Ground_Blue_X-ball_true_x_pos+ball_xpos, L1_Ground_Blue_Y, L1_Ground_Blue_W, L1_Ground_Blue_H), 0, 0, 0)


    button = pygame.draw.rect(screen, button_color, (button_xpos, button_ypos, button_width, button_height), 0, 0, 0)
    button_text = font.render(f"{button_text}", True, BLACK)
    screen.blit(button_text, [button_xpos, button_ypos])
    # RENDER YOUR GAME HERE

#Position-responsive ball position label:    ball_xpos-20(((screen_width/2)-ball_xpos)/abs((screen_width/2)-ball_xpos)),ball_ypos-20(((screen_height/2)-ball_ypos)/abs((screen_height/2)-ball_ypos))
    
    # updates display
    if ball_x_velocity != 0 or ball_y_velocity != 0:
        ball_xpos += ball_x_velocity
        ball_ypos += ball_y_velocity
        ball_true_x_pos += ball_x_velocity
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
            ball_grounded = True
            ball_y_velocity = -ball_IV

        elif ball_ypos + ball_height > ground_ypos and ball_ypos + ball_height < ground_ypos + ball_height and ball_xpos > ground_xpos - ball_width and ball_xpos < ground_xpos + ground_width:
            ball_ypos = ground_ypos - ball_height
            ball_grounded = True
            ball_y_velocity = -ball_IV

        elif ball_xpos < ground_xpos + ground_width and ball_xpos > ground_xpos + ground_width - ball_width and ball_ypos > ground_ypos - ball_height and ball_ypos < ground_ypos + ground_height:
            ball_xpos = ground_xpos + ground_width
            ball_grounded = True
            ball_y_velocity = -ball_IV

        elif ball_ypos < ground_ypos + ground_height and ball_ypos > ground_ypos + ground_height - ball_height and ball_xpos > ground_xpos - ball_width and ball_xpos < ground_xpos + ground_width:
            ball_ypos = ground_ypos + ground_height
            ball_grounded = True
            ball_y_velocity = -ball_IV

        else:
            ball_grounded = False
        
        if ball_xpos > 0.65*screen_width:
            offset=ball_xpos-0.65*screen_width
            ball_xpos = 0.65*screen_width
        elif ball_xpos < 0.35*screen_width:
            offset=ball_xpos-0.35*screen_width
            ball_xpos = 0.35*screen_width
        else:
            offset = 0        
        
        if ball_true_x_pos < 0:
            ground_xpos = ground_width
        else:
            ground_xpos = L1_Ground_Red_X

        pygame.draw.ellipse(screen, ball_color, (ball_xpos, ball_ypos, ball_width, ball_height))
    
    xpostext = font.render(f"x-pos: {ball_xpos}, True x pos: {ball_true_x_pos}", True, (0, 255, 0))
    ypostext = font.render(f"y-pos: {ball_ypos}", True, (0, 255, 0))
    #xlabelpos = [ball_xpos-20(((screen_width/2)-ball_xpos)/abs((screen_width/2)-ball_xpos)),ball_ypos-20(((screen_height/2)-ball_ypos)/abs((screen_height/2)-ball_ypos))]
    #ylabelpos = [300, 300]
    screen.blit(xpostext, [200, 0])
    screen.blit(ypostext, [700, 0])

    pygame.display.update()

    clock.tick(50)  # limits FPS to 50

pygame.quit()