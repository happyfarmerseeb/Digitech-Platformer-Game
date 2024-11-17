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
Red_A_Val = 1
Green_A_Val = 1
Blue_A_Val = 1
RED = (255, 0, 0, Red_A_Val)
GREEN = (0, 255, 0, Green_A_Val)
BLUE = (0, 0, 255, Blue_A_Val)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
gravity = 0.42

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
            self.objlist[i].draw()

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

##Add ball (player) definitions:##
class Player:
    def __init__(self, x, y, w, h, colour, LastInputs, Inputs, max_x_vel, accel, offset):
        self.x = x #200
        self.y = y #200
        self.w = w #50
        self.h = h #50
        self.colour = colour #(160, 0, 0)
        self.LastInputs = LastInputs #[False, False, False]
        self.Inputs = Inputs #[False, False, False]
        self.IV = 0 #0
        self.airtime = 0 #0
        self.max_x_vel = max_x_vel #10
        self.x_vel = 0 #0
        self.y_vel = 0 #0
        self.grounded = False #False
        self.jump_ready = False
        self.accel = accel #0
        self.offset = offset #0
        self.true_x = x #200

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
                self.IV = -15 #IV: Internal Velocity (How far the ball is trying to go)
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
                self.y = screen_height-self.h
            
    def draw(self):
        # draws ball:
        pygame.draw.ellipse(screen, self.colour, (self.x, self.y, self.w, self.h))

##Add Ground definitions:
class Ground:
    def __init__(self, x, y, w, h, colour, level):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        level.addobj(self)

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h), 0, 0, 0) #ground

    def collision_check(self, sprite):
        if sprite.x + sprite.w > self.x and sprite.x < self.x and sprite.y + sprite.h > self.y and sprite.y < self.y + self.h:
            sprite.x = self.x - sprite.w
            sprite.y_vel = 0 #previously -sprite.IV
            sprite.grounded = True
        elif sprite.y + sprite.h > self.y and sprite.y < self.y and sprite.x > self.x - sprite.w and sprite.x < self.x + self.w:
            sprite.y = self.y - sprite.h
            sprite.y_vel = 0
            sprite.grounded = True
            sprite.jump_ready = True
        elif sprite.x < self.x + self.w and sprite.x > self.x + self.w - sprite.w and sprite.y > self.y - sprite.h and sprite.y < self.y + self.h:
            sprite.x = self.x + self.w
            sprite.y_vel = 0
            sprite.grounded = True
        elif sprite.y < self.y + self.h and sprite.y > self.y + self.h - sprite.h and sprite.x > self.x - sprite.w and sprite.x < self.x + self.w:
            sprite.y = self.y + self.h
            sprite.y_vel = 0
            sprite.grounded = True
        else:
            sprite.grounded = False
    
    

screen = pygame.display.set_mode((screen_width, screen_height)) #window dimensions (W, H)
pygame.display.set_caption("[Insert Game Window Name]") #window title
clock = pygame.time.Clock() #clock
running = True #status of game running

#create object instances:
level1 = Level()
RandButton = Button(1000, 120, 150, 50, GREEN, "Speed")
ball = Player(200, 200, 50, 50, (160, 0, 0), [False, False, False], [False, False, False], 10, 0, 0)
redground = Ground(50, 664, 1080, 200, RED, level1)
greenground = Ground(1130, 664, 1080, 200, GREEN, level1)
blueground = Ground(2210, 664, 1080, 200, BLUE, level1)
redplatform = Ground(300, 594, 380, 60, RED, level1)
redplatform1 = Ground(700, 364, 180, 60, RED, level1)
greenplatform = Ground(1350, 474, 140, 50, GREEN, level1)
greenplatform1 = Ground(1850, 474, 280, 80, GREEN, level1)
blueplatform = Ground(2500, 464, 310, 240, BLUE, level1)
blueplatform1 = Ground(2950, 264, 170, 100, BLUE, level1)


while running:
# poll for events
    #below code creates an input array which is read later
    ball.LastInputs = ball.Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.Inputs[0] = True
            if event.key == pygame.K_RIGHT:
                ball.Inputs[1] = True
            if event.key == pygame.K_UP:
                ball.Inputs[2] = True

        if (ball.Inputs[0] == True and ball.Inputs[1] == True):
            ball.Inputs[0] = ball.LastInputs[1]
            ball.Inputs[1] = ball.LastInputs[0]

        if event.type == pygame.KEYUP:         
            if event.key == pygame.K_LEFT:
                ball.Inputs[0] = False
            if event.key == pygame.K_RIGHT:
                ball.Inputs[1] = False
            if event.key == pygame.K_UP:
                ball.Inputs[2] = False

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
    
    
    #reset canvas
    screen.fill(WHITE)
    
    #functions
    ball.move()

    #draw objects
    level1.modify()
    RandButton.draw()
    ball.draw()
    
    xpostext = font.render(f"X: {math.trunc(ball.x)}, True X: {math.trunc(ball.true_x)}, W: {ball.w}, H: {ball.h}, Last: {ball.LastInputs}, Current: {ball.Inputs}, IV: {ball.IV}, Air: {ball.airtime}, MaxVel: {ball.max_x_vel}, XV: {math.trunc(ball.x_vel)}, YV: {math.trunc(ball.y_vel)}, Grounded: {ball.grounded}, Jump: {ball.jump_ready}, Accel: {ball.accel}", True, (0, 255, 0))
    ypostext = font.render(f"y-pos: {math.trunc(ball.y)}", True, (0, 255, 0))
    screen.blit(xpostext, [0, 50])
    screen.blit(ypostext, [ball.x, ball.y-100])
    
    
    # RENDER YOUR GAME HERE
    pygame.display.update()

    clock.tick(50)  # limits FPS to 50
