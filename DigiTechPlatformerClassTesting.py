#pygame class testing
import math
import random #imports random
import pygame #imports pygame library
print("Hello World") #prints "Hello World"

#initialize game
pygame.init()

#define some important values (default colours, screen width and screen height, etc.)#
screen_width = 1536
screen_height = 864
font = pygame.font.SysFont("Calibri", 25)
Red_Val = 1
Green_Val = 1
Blue_Val = 1
Tokens = 128
RED = (255, 0, 0, Red_Val/255)
GREEN = (0, 255, 0, Green_Val/255)
BLUE = (0, 0, 255, Blue_Val/255)
BLACK = (0, 0, 0, 1)
CLEAR = (0, 0, 0, 0)
WHITE = (255, 255, 255)
gravity = 0.42
current_level = "prelevel"
frames = 0

class InputDisplay:
    def __init__(self, x, y, w, h, colour):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h), 0, 0, 0) #individual key display

class Level:
    def __init__(self):
        self.objlist = []

    def addobj(self, object):
        self.objlist.append(object)

    def modify(self):
        ball.grounded = False
        for i in range(0,len(self.objlist)):
            self.objlist[i].x -= ball.offset
            if ball.grounded == False:
                self.objlist[i].collision_check(ball)
            else:
                self.objlist[i].collision_check(ball)
                ball.grounded = True
            self.objlist[i].draw()

class Button:
    def __init__(self, x, y, w, h, colour, text, level, variable, direction):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        self.text = text
        self.level = level
        self.variable = variable
        self.direction = direction

    def draw(self):
        button = pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h), 0, 0, 0)
        button_text = font.render(f"{self.text}", True, BLACK)
        screen.blit(button_text, [self.x, self.y])

##Add ball (player) definitions:##
class Player:
    def __init__(self, x, y, w, h, colour, LastInputs, Inputs, max_x_vel, accel, offset, radius):
        self.x = x #200
        self.y = y #200
        self.w = w #50
        self.h = h #50
        self.colour = (Red_Val, Green_Val, Blue_Val) #(160, 0, 0)
        self.LastInputs = LastInputs #[False, False, False]
        self.Inputs = Inputs #[False, False, False]
        self.IV = 0 #0
        self.jump_speed = 14*math.log(Green_Val)
        self.airtime = 0 #0
        self.max_x_vel = max_x_vel*math.log(Red_Val) #10
        self.x_vel = 0 #0
        self.y_vel = 0 #0
        self.grounded = False #False
        self.jump_ready = False
        self.accel = accel #0
        self.offset = offset #0
        self.true_x = x #200
        #vision field:
        self.vision_radius = radius*math.log(Blue_Val)


        #collision patch {to be completed}:
        self.direction = ["N"]
        #N = No direction or default value
        #L = Left
        #R = Right        
        #U = Up
        #D = Down



    def move(self):
        #input array read begin
        #dealing with x acceleration
        
        if self.Inputs[0] == True:
            self.accel = -0.5 #makes Left key set leftwards acceleration
        elif self.Inputs[1] == True:
            self.accel = 0.5 #makes right key set rightwards acceleration

        else:
            if abs(self.x_vel)<1: #if velocity is low enough, the game will just set it to 0
                self.accel = 0
                self.x_vel = 0
            else: 
                self.accel = -0.04*self.x_vel #makes player slow down when there are no inputs due to friction with ground
        #updating x velocity
        self.x_vel += self.accel
        #if ball exceeds maximum x velocity:
        if abs(self.x_vel) > self.max_x_vel:
            self.x_vel = self.max_x_vel*(self.x_vel/abs(self.x_vel))


        #dealing with jump inputs (Inputs[2] = True)
        if self.Inputs[2] == True:
            if self.jump_ready == True:
                self.IV = -self.jump_speed #IV: Internal Velocity (How far the ball is trying to go)
                self.airtime = 0
                self.jump_ready = False
            else:
                if self.airtime >= 75:
                    self.Inputs[2] = False
                self.airtime += 1
        else:
            self.IV += 0.5 
            if self.grounded == True:            
                self.airtime = 0
                self.IV = 0
            else:
                self.airtime += 1

        #calculate y velocity of ball
        self.y_vel = self.IV+(self.airtime*gravity)

            # updates position to display:
        if self.x_vel != 0 or self.y_vel != 0:
            self.x += self.x_vel
            self.y += self.y_vel
            self.true_x += self.offset
            
            if self.x > 0.65*screen_width:
                self.offset=self.x-0.65*screen_width
                self.x = 0.65*screen_width
            elif self.x < 0.25*screen_width:
                self.offset=self.x-0.25*screen_width
                self.x = 0.25*screen_width
            else:
                self.offset = 0      

            if self.y < 0:
                self.y = 0
            elif self.y >= screen_height-self.h:
                self.y = 100
                if self.true_x > 50:
                    self.offset = 4000-self.true_x
                else:
                    self.offset = 100-self.true_x


            
    def vision_limiter(self, radius): #used ChatGPT for this function
        mask = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 255))  # Start with fully opaque surface
        pygame.draw.circle(mask, (0, 0, 0, 0), ((ball.x+(ball.w)/2),(ball.y+(ball.h)/2)), self.vision_radius)  # Draw transparent circle
        return mask

    # Create an inverted circle mask
    


    # Create a surface for the gradient
    def draw(self):
        # draws ball:
        pygame.draw.ellipse(screen, self.colour, (self.x, self.y, self.w, self.h))
        mask_surface = self.vision_limiter(self.vision_radius)
        screen.blit(mask_surface, (0, 0))

##Add Ground definitions:
class Ground:
    def __init__(self, x, y, w, h, colour, level, reset):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        level.addobj(self)
        self.reset = reset

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h), 0, 0, 0) #ground

    def collision_check(self, sprite):
        if sprite.x + sprite.w > self.x and sprite.x < self.x and sprite.y + sprite.h > self.y and sprite.y < self.y + self.h:
            sprite.x = self.x - sprite.w
            sprite.y_vel = 0 #previously -sprite.IV

        elif sprite.y + sprite.h > self.y and sprite.y < self.y and sprite.x > self.x - sprite.w and sprite.x < self.x + self.w:
            sprite.y = self.y - sprite.h
            sprite.y_vel = 0
            sprite.grounded = True
            sprite.jump_ready = True
            
        elif sprite.x < self.x + self.w and sprite.x > self.x + self.w - sprite.w and sprite.y > self.y - sprite.h and sprite.y < self.y + self.h:
            sprite.x = self.x + self.w
            sprite.y_vel = 0
            
        elif sprite.y < self.y + self.h and sprite.y > self.y + self.h - sprite.h and sprite.x > self.x - sprite.w and sprite.x < self.x + self.w:
            sprite.y = self.y + self.h
            sprite.y_vel = 0
                
        else:
            sprite.grounded = False


screen = pygame.display.set_mode((screen_width, screen_height)) #window dimensions (W, H)
pygame.display.set_caption("Risk and Reward") #window title
clock = pygame.time.Clock() #clock
running = True #status of game running

#create object instances:
InputL = InputDisplay(20, 804, 50, 50, BLACK)
InputR = InputDisplay(80, 804, 50, 50, BLACK)
InputU = InputDisplay(20, 744, 110, 50, BLACK)

prelevel = Level()
RedButtonAdd = Button(100, 120, 150, 50, RED, "Red+", prelevel, Red_Val, 1)
RedButtonMinus = Button(250, 120, 150, 50, RED, "Red-", prelevel, Red_Val, -1)
GreenButtonAdd = Button(400, 120, 150, 50, GREEN, "Green+", prelevel, Green_Val, 1)
GreenButtonMinus = Button(550, 120, 150, 50, GREEN, "Green-", prelevel, Green_Val, -1)
BlueButtonAdd = Button(700, 120, 150, 50, BLUE, "Blue+", prelevel, Blue_Val, 1)
BlueButtonMinus = Button(850, 120, 150, 50, BLUE, "Blue-", prelevel, Blue_Val, -1)
Value_Buttons = [RedButtonAdd, RedButtonMinus, GreenButtonAdd, GreenButtonMinus, BlueButtonAdd, BlueButtonMinus] #control RGB attributes

level1 = Level()
RandButton = Button(1000, 120, 150, 50, GREEN, "Speed", level1, Red_Val, 1)
ball = Player(200, 200, 50, 50, (160, 0, 0), [False, False, False], [False, False, False], 10, 0, 0, 300)
redground = Ground(50, 764, 3600, 100, RED, level1, False)
greenground = Ground(3650, 764, 1300, 100, GREEN, level1, False)
blueground = Ground(4950, 764, 1600, 100, BLUE, level1, False)
redplatform = Ground(2600, 594, 180, 220, RED, level1, False)
redplatform1 = Ground(3000, 364, 180, 220, RED, level1, False)
greenplatform = Ground(3850, 474, 140, 70, GREEN, level1, False)
greenplatform1 = Ground(4650, 474, 180, 80, GREEN, level1, False)
blueplatform = Ground(5200, 364, 60, 500, BLUE, level1, False)
blueplatform1 = Ground(5850, 264, 170, 100, BLUE, level1, False)
game_end = Ground(6620, 300, 200, 200, BLACK, level1, True)



while running:
    # poll for events
    if current_level == "prelevel":
        for event in pygame.event.get():
            #reset canvas
            screen.fill(WHITE)
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > RedButtonAdd.x and mouse_pos[1] > RedButtonAdd.y and mouse_pos[0] < RedButtonAdd.x+RedButtonAdd.w and mouse_pos[1] < RedButtonAdd.y+RedButtonAdd.h:
                    if Red_Val<255:
                        Red_Val += 1
                        Tokens -= 1
                if mouse_pos[0] > RedButtonMinus.x and mouse_pos[1] > RedButtonMinus.y and mouse_pos[0] < RedButtonMinus.x+RedButtonMinus.w and mouse_pos[1] < RedButtonMinus.y+RedButtonMinus.h:
                    if Red_Val>0:
                        Red_Val -= 1
                        Tokens += 1
                if mouse_pos[0] > GreenButtonAdd.x and mouse_pos[1] > GreenButtonAdd.y and mouse_pos[0] < GreenButtonAdd.x+GreenButtonAdd.w and mouse_pos[1] < GreenButtonAdd.y+GreenButtonAdd.h:
                    if Green_Val<255:
                        Green_Val += 1
                        Tokens -= 1
                if mouse_pos[0] > GreenButtonMinus.x and mouse_pos[1] > GreenButtonMinus.y and mouse_pos[0] < GreenButtonMinus.x+GreenButtonMinus.w and mouse_pos[1] < GreenButtonMinus.y+GreenButtonMinus.h:
                    if Green_Val>0:
                        Green_Val -= 1
                        Tokens += 1
                if mouse_pos[0] > BlueButtonAdd.x and mouse_pos[1] > BlueButtonAdd.y and mouse_pos[0] < BlueButtonAdd.x+BlueButtonAdd.w and mouse_pos[1] < BlueButtonAdd.y+BlueButtonAdd.h:
                    if Blue_Val<255:
                        Blue_Val += 1
                        Tokens -= 1
                if mouse_pos[0] > BlueButtonMinus.x and mouse_pos[1] > BlueButtonMinus.y and mouse_pos[0] < BlueButtonMinus.x+BlueButtonMinus.w and mouse_pos[1] < BlueButtonMinus.y+BlueButtonMinus.h:
                    if Blue_Val>0:
                        Blue_Val -= 1
                        Tokens += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    current_level = "level1"       

            if Tokens == 0:
                current_level = "level1"

            ball.colour = (Red_Val, Green_Val, Blue_Val) #(160, 0, 0)

            #functions
            RedButtonAdd.draw()
            RedButtonMinus.draw()
            GreenButtonAdd.draw() 
            GreenButtonMinus.draw()
            BlueButtonAdd.draw()
            BlueButtonMinus.draw()

            ball.max_x_vel = 10*math.log(Red_Val, 10) #10
            ball.jump_speed = 10*math.log(Green_Val, 10)
            ball.vision_radius = 100*math.log(Blue_Val, 10)
        
            xpostext = font.render(f"R: {Red_Val}, G: {Green_Val}, B: {Blue_Val}, Tokens: {Tokens}", True, (0, 255, 0))
            screen.blit(xpostext, [100, 100])

    elif current_level == "level1":
    #below code creates an input array which is read later
        ball.LastInputs = ball.Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ball.Inputs[0] = True
                    InputL.colour = GREEN
                if event.key == pygame.K_RIGHT:
                    ball.Inputs[1] = True
                    InputR.colour = GREEN
                if event.key == pygame.K_UP:
                    ball.Inputs[2] = True
                    InputU.colour = GREEN
                if event.key == pygame.K_r:
                    current_level = "prelevel"


            if ball.Inputs[0] == ball.Inputs[1] == True and ball.LastInputs[0] == True and ball.LastInputs[1] == False:
                ball.Inputs[0] = False
                ball.Inputs[1] = True
            elif ball.Inputs[0] == ball.Inputs[1] == True and ball.LastInputs[0] == False and ball.LastInputs[1] == True:
                ball.Inputs[0] = True
                ball.Inputs[1] = False
            
            if (ball.Inputs[0] == True and ball.Inputs[1] == True):
                ball.Inputs[1] = ball.LastInputs[0]
                ball.Inputs[0] = ball.LastInputs[1]


            if event.type == pygame.KEYUP:         
                if event.key == pygame.K_LEFT:
                    ball.Inputs[0] = False
                    InputL.colour = BLACK
                if event.key == pygame.K_RIGHT:
                    ball.Inputs[1] = False
                    InputR.colour = BLACK
                if event.key == pygame.K_UP:
                    ball.Inputs[2] = False
                    InputU.colour = BLACK

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > RandButton.x and mouse_pos[1] > RandButton.y and mouse_pos[0] < RandButton.x+RandButton.w and mouse_pos[1] < RandButton.y+RandButton.h:
                    ball.max_x_vel = random.randint(1,100)
                    ball.y = 0
                    # L1_Ground_Red_X = random.randint(1,400)
                    # L1_Ground_Red_Y = random.randint(1,300)
                    # L1_Ground_Red_W = random.randint(1,500)
                    # L1_Ground_Red_H = random.randint(1,200)

                    # L1_Ground_Green_X = random.randint(1,400)
                    # L1_Ground_Green_Y = random.randint(1,300)
                    # L1_Ground_Green_W = random.randint(1,500)
                    # L1_Ground_Green_H = random.randint(1,200)

                    # L1_Ground_Blue_X = random.randint(1,400)
                    # L1_Ground_Blue_Y = random.randint(1,300)
                    # L1_Ground_Blue_W = random.randint(1,500)
                    # L1_Ground_Blue_H = random.randint(1,200)
        
        
        
        #functions
        screen.fill(WHITE)
        ball.move()

        if ball.true_x>6400:
            current_level = "levelend"
        #draw objects
        level1.modify()
        RandButton.draw()
        ball.draw()
        
        #value display (for dev testing):
        # xpostext = font.render(f"X: {math.trunc(ball.x)}, True X: {math.trunc(ball.true_x)}, W: {ball.w}, H: {ball.h}, Last: {ball.LastInputs}, Current: {ball.Inputs}, IV: {ball.IV}, Air: {ball.airtime}, MaxVel: {ball.max_x_vel}, XV: {math.trunc(ball.x_vel)}, YV: {math.trunc(ball.y_vel)}, Grounded: {ball.grounded}, Jump: {ball.jump_ready}, Accel: {ball.accel}", True, (0, 255, 0))
        # ypostext = font.render(f"y-pos: {math.trunc(ball.y)}", True, (0, 255, 0))
        # screen.blit(xpostext, [0, 50])
        # screen.blit(ypostext, [ball.x, ball.y-100])

        InputL.draw()
        InputR.draw()
        InputU.draw()
        
        frames += 1

                    
    elif current_level == "levelend":
        # Create a font object with a large size
        font_size = 100  # Adjust this for bigger or smaller text
        font = pygame.font.Font(None, font_size)  # Use default font (None) or load a custom font file

        # Render the text
        game_end_text = font.render(f"Time: {frames/50}s", True, WHITE)
        text_rect = game_end_text.get_rect(center=(400, 300))  # Center the text

        # Main loop

        screen.fill(BLACK)  # Clear the screen with black

        # Draw the text
        screen.blit(game_end_text, text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

    # RENDER YOUR GAME HERE
    pygame.display.update()

    clock.tick(50)  # limits FPS to 50
