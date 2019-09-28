import math
import cmath
import pygame, sys
import time
from random import randint

from pygame.locals import *

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
pygame.init()
DISPLAYSURF = pygame.display.set_mode((800, 600))
gamestate = 0

fontObj = pygame.font.Font('freesansbold.ttf', 32)

 # set up the colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
TRANSPARENT = (255,255,255,0)

HELISPEEDX = 4
HELISPEEDY = 8

P1Speed=2
CANNONLENGTH=30
GRAVITY=10.0
Balls=[]

def makeNewBall(velocity, direction):
    ball={}
    ball['velocity'] = velocity
    ball['direction'] = direction
    ball['Rect'] = pygame.Rect(20, 580, 10, 10)
    ball['Surf'] = pygame.Surface((ball['Rect'].width, ball['Rect'].height))
    ball['Surf'].fill(RED)
    pygame.draw.circle(ball['Surf'], RED, (10,10) , 5, 0)
    ball['Time0']=time.time()
    return ball


def P2Reset(player):
    player['Rect'].left=720
    player['Rect'].top=randint(200,500)


P1points=0
P2points=0

P2={}
P2['img']= pygame.transform.scale(pygame.image.load('helicopter.png'), (70, 50))
P2['Rect']=pygame.Rect(720, 100, 70, 50)
P2['moveup']=False
P2['movedown']=False
P2Reset(P2)


P1={}
P1['direction']=0
P1['moveup']=False
P1['movedown']=False

LPRect = pygame.Rect(20, 580, 50, 20)
LPSurf = pygame.Surface((LPRect.width, LPRect.height))
LPSurf.fill(RED)
pygame.draw.rect(LPSurf, BLUE, LPRect)







while True: # main game loop
    DISPLAYSURF.fill(GREEN)

    if(gamestate == 1):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    P2['movedown'] = True
                elif event.key == K_UP:
                    P2['moveup'] = True
                if event.key == K_s:
                    P1['movedown'] = True
                elif event.key == K_w:
                    P1['moveup'] = True

                if (len(Balls) < 3):
                    if event.key == K_d:
                        Balls.append(makeNewBall(10, P1['direction']))
                    if event.key == K_f:
                        Balls.append(makeNewBall(15, P1['direction']))
                    if event.key == K_g:
                        Balls.append(makeNewBall(20, P1['direction']))

            elif event.type == KEYUP:
                if event.key == K_DOWN:
                    P2['movedown'] = False
                elif event.key == K_UP:
                    P2['moveup'] = False
                if event.key == K_s:
                    P1['movedown'] = False
                elif event.key == K_w:
                    P1['moveup'] = False


        if (P2['moveup'] == True and P2['Rect'].top > 0):
            P2['Rect'].top -= HELISPEEDY
        elif (P2['movedown'] == True and P2['Rect'].top < 560):
            P2['Rect'].top += HELISPEEDY

        if (P1['moveup'] == True and P1['direction'] > 0):
            P1['direction'] -= P1Speed
        elif (P1['movedown'] == True and P1['direction'] < 90):
            P1['direction'] += P1Speed

        P2['Rect'].left-=HELISPEEDX

        if P2['Rect'].left <=-10:
            P2points+=1
            P2Reset(P2)

        pygame.draw.line(DISPLAYSURF, BLACK, (20, 580), (20+CANNONLENGTH*math.sin(math.radians(P1['direction'])), 580-CANNONLENGTH*math.cos(math.radians(P1['direction']))))

        for ball in Balls:
            ball['Rect'].x += int(ball['velocity'] * math.sin(math.radians(ball['direction'])))
            ball['Rect'].y -= int(ball['velocity'] * math.cos(math.radians(ball['direction'])))
            ball['Rect'].y += int(((time.time()-ball['Time0'])*(time.time()-ball['Time0']))*GRAVITY)


            if (ball['Rect'].colliderect(P2['Rect'])):

                P1points += 1
                del Balls[i]
                P2Reset(P2)

            DISPLAYSURF.blit(ball['Surf'], ball['Rect'])

        for i in range(len(Balls) - 1, -1, -1):
            if Balls[i]['Rect'].x < 0 or Balls[i]['Rect'].x > 800 or Balls[i]['Rect'].y < 0 or Balls[i]['Rect'].y > 600:
                del Balls[i]



    #   SCORE
        textSurfaceObj1 = fontObj.render('Player 1:' + str(P1points), True, GREEN, BLUE)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (100, 50)
        textSurfaceObj2 = fontObj.render('Player 2:' + str(P2points), True, GREEN, BLUE)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (700, 50)

        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)

        DISPLAYSURF.blit(P2['img'], P2['Rect'])
        DISPLAYSURF.blit(LPSurf, LPRect)

        if (P1points >=10 or P2points >=10):
            gamestate=0

    elif (gamestate == 0):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    P1points = 0
                    P2points = 0
                    gamestate = 1

        screentext = ""
        if (P1points > P2points):
            screentext = "P1 Wins!"
        elif (P2points > P1points):
            screentext = 'P2 Wins!'
        else:
            screentext = "Press space to start"

        textSurfaceObj3 = fontObj.render(screentext, True, GREEN, BLUE)
        textRectObj3 = textSurfaceObj3.get_rect()
        textRectObj3.center = (300, 500)

        DISPLAYSURF.blit(textSurfaceObj3, textRectObj3)


    pygame.display.update()
    fpsClock.tick(FPS)