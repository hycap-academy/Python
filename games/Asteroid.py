import math
import cmath
import pygame, sys
import time
from random import randint

from pygame.locals import *

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()


 # set up the colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
TRANSPARENT = (255,255,255,0)

P1points=0
P2points=0
gamestate = 0
pygame.init()
DISPLAYSURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Asteroid!')


fontObj = pygame.font.Font('freesansbold.ttf', 32)

def makeNewBall(player):
    ball={}
    ball['num']=player['num']
    balltypeprob = randint(1, 100)
    ball['velocity'] = 20
    ball['direction'] = player['rotation']
    ball['type']=player['num']
    ball['Rect'] = pygame.Rect(player['Rect'].centerx, player['Rect'].centery, 10, 10)
    ball['Surf'] = pygame.Surface((ball['Rect'].width, ball['Rect'].height))
    ball['Surf'].fill(GREEN)
    if player['num']==1:
        pygame.draw.circle(ball['Surf'], BLUE, (10,10) , 5, 0)
    elif player['num']==2:
        pygame.draw.circle(ball['Surf'], RED, (10, 10), 5, 0)
    return ball


def makeNewPlayer(playernum):
    player={}
    player['ballcount']=0
    player['num']=playernum
    player['moveup']=False
    player['movedown']=False
    player['turnleft']=False
    player['turnright']=False
    player['speed']=1
    player['rotation']=0
    player['movedirection']=0
    player['rotationspeed']=5
    player['xspeed']=0
    player['yspeed']=0



    if playernum==2:
        player['left'] = 5
        player['img'] = pygame.transform.scale(pygame.image.load('redplayertr.png'), (50, 50))
    else:
        player['left']=760
        player['img'] = pygame.transform.scale(pygame.image.load('blueplayertr.png'), (50, 50))

    player['Rect']=pygame.Rect(player['left'], 100, 50, 50)
    player['Rect'].center=(player['Rect'].centerx, player['Rect'].centery)
    #pygame.draw.rect(player['img'], WHITE, (0, 0, player['Rect'].width, player['Rect'].height))
    #pygame.draw.rect(player['img'], TRANSPARENT, (0, 0, 30, 30))


    return player

def playerReset(player):
    player['Rect'].top=randint(50,500)
    if player['num']==2:
        player['Rect'].left = 5
    elif player['num']==1:
        player['Rect'].left=760

    player['xspeed']=0
    player['yspeed']=0
    player['rotation']=0


P1 = makeNewPlayer(1)
P2 = makeNewPlayer(2)
Players=[]
Players.append(P1)
Players.append(P2)

Balls=[]
#Balls.append(makeNewBall())
lastBallTime=time.time()

P1lastshot=time.time()
P2lastshot=time.time()


while True: # main game loop

    DISPLAYSURF.fill(GREEN)
    if(gamestate == 1):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key==K_DOWN:
                    P1['movedown']=True
                elif event.key==K_UP:
                    P1['moveup']=True

                if event.key==K_LEFT:
                    P1['turnleft']=True
                elif event.key==K_RIGHT:
                    P1['turnright']=True


                if event.key==K_m and Players[0]['ballcount'] < 2:
                    Balls.append(makeNewBall(P1))


                if event.key==K_w:
                    P2['moveup']=True
                elif event.key==K_s:
                    P2['movedown']=True

                if event.key == K_a:
                    P2['turnleft']=True
                elif event.key == K_d:
                    P2['turnright']=True

                if event.key==K_f and Players[1]['ballcount'] < 2:
                    Balls.append(makeNewBall(P2))


            elif event.type == KEYUP:
                if event.key==K_DOWN:
                    P1['movedown']=False
                elif event.key==K_UP:
                    P1['moveup']=False

                if event.key==K_LEFT:
                    P1['turnleft']=False
                elif event.key==K_RIGHT:
                    P1['turnright']=False

                if event.key==K_w:
                    P2['moveup']=False
                elif event.key==K_s:
                    P2['movedown']=False

                if event.key == K_a:
                    P2['turnleft']=False
                elif event.key == K_d:
                    P2['turnright']=False

        for player in Players:

            if (player['moveup']==True):
                player['xspeed'] -= player['speed']*math.sin(math.radians(player['rotation']))
                player['yspeed'] -= player['speed'] * math.cos(math.radians(player['rotation']))

            elif player['movedown']==True:
                player['xspeed'] += player['speed'] * math.sin(math.radians(player['rotation']))
                player['yspeed'] += player['speed'] * math.cos(math.radians(player['rotation']))


            if player['Rect'].top <=0 and player['yspeed'] < 0:
                player['yspeed'] = player['yspeed']*-1

            if player['Rect'].top >=570 and player['yspeed'] > 0:
                player['yspeed'] = player['yspeed']*-1

            if player['Rect'].left <=0 and player['xspeed'] < 0:
                player['xspeed'] = player['xspeed']*-1

            if player['Rect'].left >=770 and player['xspeed'] > 0:
                player['xspeed'] = player['xspeed']*-1


            player['Rect'].x += int(player['xspeed'])
            player['Rect'].y += int(player['yspeed'])



            if player['turnleft']==True:
                player['Rect'].center = (player['Rect'].centerx, player['Rect'].centery)
                player['rotation'] += player['rotationspeed']
            if player['turnright']==True:
                player['Rect'].center = (player['Rect'].centerx, player['Rect'].centery)
                player['rotation'] -= player['rotationspeed']

            if player['rotation'] < 0:
                player['rotation']+=360
            elif player['rotation'] > 359:
                player['rotation']-=360

            DISPLAYSURF.blit(pygame.transform.rotate(player['img'], player['rotation']) ,player['Rect'])


        #if time.time()-lastBallTime > 3:
        #    Balls.append(makeNewBall())
        #    lastBallTime=time.time()

        if Players[0]['Rect'].colliderect(Players[1]['Rect']):
            playerReset(Players[0])
            playerReset(Players[1])

        for ball in Balls:
            ball['Rect'].x -= int(ball['velocity']*math.sin(math.radians(ball['direction'])))
            ball['Rect'].y -= int(ball['velocity']*math.cos(math.radians(ball['direction'])))


            for player in Players:
                if (ball['Rect'].colliderect(player['Rect']) and ball['num'] != player['num']):
                    ball['direction'] = 360-ball['direction']
                    if player['num']==2:
                        P2points += 1
                    elif player['num']==1:
                        P1points +=1
                    del Balls[i]
                    playerReset((player))

            DISPLAYSURF.blit(ball['Surf'], ball['Rect'])

        Players[0]['ballcount']=0
        Players[1]['ballcount']=0
        for i in range(len(Balls)-1, -1,-1):
            if Balls[i]['Rect'].x < 0 or Balls[i]['Rect'].x > 800 or Balls[i]['Rect'].y < 0 or Balls[i]['Rect'].y > 600:
                del Balls[i]
            else:
                if Balls[i]['num']==1:
                    Players[0]['ballcount']=Players[0]['ballcount']+1
                elif Balls[i]['num']==2:
                    Players[1]['ballcount']=Players[1]['ballcount']+1


    #   SCORE
        textSurfaceObj1 = fontObj.render('Player 1:' + str(P1points), True, GREEN, BLUE)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (100, 50)
        textSurfaceObj2 = fontObj.render('Player 2:' + str(P2points), True, GREEN, BLUE)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (700, 50)

        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)

        if(P1points>= 10 or P2points>=10):
            gamestate = 0
    elif(gamestate==0):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    P1points = 0
                    P2points = 0
                    gamestate = 1

        screentext=""
        if(P1points > P2points):
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