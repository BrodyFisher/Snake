import pygame, sys, random
from pygame.math import Vector2


class APPLE:
    def __init__(self):
        #gets an x and y position
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

    #draw a square
    def draw_apple(self):
        #creates rectangle holding the apple
        applerect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        #draw rectangle
        pygame.draw.rect(screen,(255,2,45), applerect)
class SNAKE:
    def __init__(self):
        self.orig = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.body = self.orig
        self.direction = Vector2(1,0)
    
    def draw_snake(self):
        for block in self.body:
            #creating a rect
            snakerect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            #drawing a rect
            pygame.draw.rect(screen, (30,255,88), snakerect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0]+self.direction)
        self.body = body_copy[:]

#drawing a new apple location
def newapple():
    apple.pos = Vector2(random.randint(0,cell_number-1),random.randint(0,cell_number-1))

    #making sure the new apple doesn't spawn in the snake
    for x in snake.body:
            if x == apple.pos:
                newapple()

#handling when the snake goes too far to any side
def pacman(side):
    if side == "right":
        snake.body[0] += Vector2(-(cell_number+1),0) #goes off the right side

    elif side == "left":
        snake.body[0] += Vector2((cell_number+1),0) #goes off the left side

    elif side == "top":
        snake.body[0] += Vector2(0,(cell_number+1)) #goes off the top

    elif side == "bottom":
        snake.body[0] += Vector2(0,-(cell_number+1)) #goes off the bottom


#initilaizing pygame
pygame.init()

#setting title of the window
pygame.display.set_caption("How do you even code lol")
icon = pygame.image.load("startscreen.png")
pygame.display.set_icon(icon)

#cell details
cell_size = 20
cell_number = 20

#screen stuff
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))

#creating a clock *exlusively to deal with framerate
clock = pygame.time.Clock()

#creating game objects
apple = APPLE()
snake = SNAKE()

#only lets the game update every 150 milliseconds
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#game loop
while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and snake.direction != Vector2(0,1): #for all cases, it won't let you go backwards, thus killing you right away
                snake.direction = Vector2(0,-1) #up key is pressed

            elif event.key == pygame.K_DOWN and snake.direction != Vector2(0,11):
                snake.direction = Vector2(0,1) #down key is pressed

            elif event.key == pygame.K_LEFT and snake.direction != Vector2(1,0): 
                snake.direction = Vector2(-1,0) #left key is pressed

            elif event.key == pygame.K_RIGHT and snake.direction != Vector2(-1,0):
                snake.direction = Vector2(1,0) #rigth key is pressed

            if event.key == pygame.K_ESCAPE: #alternative way to quit the game
                pygame.quit()
                sys.exit()

    #reprinting the screen
    screen.fill((30,144,255))  

    #drawing the apple
    apple.draw_apple()
    #drawing the snake
    snake.draw_snake()

    #collecting apple event
    if snake.body[0] == apple.pos:
        snake.body.append(snake.body[-1]-snake.direction)
        newapple()

    #checks to see if you lost by checking for duplicates in snake.body
    for x in snake.body:
        if snake.body.count(x) > 1:
            snake.body = snake.orig
        else:
            continue

    #reaching the edge event
    if snake.body[0].x > cell_number:
        pacman("right")

    elif snake.body[0].x < 0:
        pacman("left")

    elif snake.body[0].y < 0:
        pacman("top")

    elif snake.body[0].y > cell_number:
        pacman("bottom")

    #drawing all elements
    pygame.display.update()

    #makes the game run at 60 fps
    clock.tick(60)