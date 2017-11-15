#PONG pygame

import random
import pygame, sys
from pygame.locals import *
import matplotlib.pyplot as plt
import random

from ai import Dqn

control = False
action = [-10, 0, 10]

# input, nb_actions, gamma
brain = Dqn(3, 3, 0.9, 5)
last_reward_1 = 0
scores_1 = []

pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Pong played by AI')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(3,5)
    vert = random.randrange(3,5)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    global last_reward_1
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)

    last_reward_1 = 0
#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score, paddle1_vel,paddle2_vel
    global last_reward_1, control
    
    last_reward_1 = 0
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    if paddle1_pos[1] <= 40:
        paddle1_pos[1] -= paddle1_vel
    if paddle1_pos[1] >= 360:
        paddle1_pos[1] -= paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        # hit left paddle
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
        last_reward_1 = 100
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        # hit left wall
        r_score += 1
        last_reward_1 = -100
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        # hit right paddle
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)
        

    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))  
    
    
    #last_reward_1 -= (80 + paddle1_pos[1] - ball_pos[1]) * 0.00005
    last_signal_1 = [ball_pos[1], ball_pos[0], paddle1_pos[1]]
    action_1 = brain.update(last_reward_1, last_signal_1)
    
    scores_1.append(brain.score())
    msgControl = "True"
    if (not control):
        paddle1_vel = action[action_1]
        msgControl = "False"

    paddle2_pos[1] = ball_pos[1]
    #paddle2_vel = random.choice(action)
    
    
    myfont3 = pygame.font.SysFont("Arial", 15)
    label3 = myfont3.render(msgControl, 1, (255,255,0))
    canvas.blit(label3, (50, 360))
    
    myfont4 = pygame.font.SysFont("Arial", 15)
    label4 = myfont4.render("Last Reward "+str(last_reward_1), 1, (255,255,0))
    canvas.blit(label4, (100, 360))
    
    myfont5 = pygame.font.SysFont("Arial", 15)
    label5 = myfont5.render("1: Control,  8: Show,  9: Load,  0: Save/Show,  L: Put paddle on middle", 1, (255,255,0))
    canvas.blit(label5, (50, 380))
    
    #paddle2_pos[1] = ball_pos[1]

    #print("reward_1 = ", last_reward_1," action = ", action_1)
   
#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel, control, paddle1_pos
    
    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8
    elif event.key == K_0:
        brain.save()
        plt.plot(scores_1)
        plt.show()
    elif event.key == K_9: 
        brain.load()
    elif event.key == K_8:
        plt.plot(scores_1)
        plt.show()
    elif event.key == K_1:
        if(control):
            control = False
        else:
            control = True
    elif event.key == K_l:
        paddle1_pos[1] = 150

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

init()


#game loop
while True:

    draw(window)
    
    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fps.tick(60)