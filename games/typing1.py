import math
import cmath
import pygame, sys
import time
import random
import winsound

from pygame.locals import *

def createPhrase(length, chars):
    strTyper = ""
    strTyping = "a;sldkfjghqpwoeirutyzz/x.c,vmbn1234567890"
    spaceApart = random.randint(2,6)
    for n in range(sLength):

        strTyper += strTyping[random.randrange(0, i)]
        if n==spaceApart:
            strTyper += " "
            spaceApart=n+random.randint(3,7)

    return strTyper


def showTouch(letter, KBL, KBT):
    kb = {}
    kb["q"] = (0, 0)
    kb["w"] = (46, 0)
    kb["e"] = (92, 0)
    kb["r"] = (138, 0)
    kb["t"] = (184, 0)
    kb["y"] = (230, 0)
    kb["u"] = (276, 0)
    kb["i"] = (322, 0)
    kb["o"] = (374, 0)
    kb["p"] = (420, 0)
    # -- line 2
    kb["a"] = (17, 67)
    kb["s"] = (63, 67)
    kb["d"] = (109, 67)
    kb["f"] = (155, 67)
    kb["g"] = (201, 67)
    kb["h"] = (247, 67)
    kb["j"] = (293, 67)
    kb["k"] = (339, 67)
    kb["l"] = (391, 67)
    kb[";"] = (437, 67)
    # -- line 3
    kb["z"] = (34, 132)
    kb["x"] = (63, 132)
    kb["c"] = (109, 132)
    kb["v"] = (155, 132)
    kb["b"] = (201, 132)
    kb["n"] = (247, 132)
    kb["m"] = (293, 132)
    kb[","] = (339, 132)
    kb["."] = (391, 132)
    kb["/"] = (437, 132)
    kb[" "] = (201, 199)

    return pygame.Rect(KBL + kb[letter][0], KBT + kb[letter][1], 50, 60)


FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

sLength = 30

 # set up the colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
TRANSPARENT = (255,255,255,0)

KBL = 100
KBT = 300

imgKeyboard = pygame.transform.scale(pygame.image.load('keyboard.png'), (500, 200))
rectKeyboard = pygame.Rect(KBL, KBT, 500, 200)

imgTouch = pygame.transform.scale(pygame.image.load('touch.png'), (50, 60))


pygame.init()
DISPLAYSURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Typer!')

fontObj = pygame.font.Font('freesansbold.ttf', 32)

#while True: # main game loop

points=0
strikes=0


for i in range(2, 32, 2):
    strTyper=""
    strTyped=""
    strTyper = createPhrase(sLength, i)

    charnum = 0
    passed=False
    gameover=False
    starttime=0
    mistakes=0

    while not passed:  # main game loop
        if len(strTyped)==1:
            starttime=time.time()-.1
        DISPLAYSURF.fill(BLACK)

        if charnum <len(strTyper):
            rectTouch = showTouch(strTyper[charnum], KBL, KBT)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                print(event.key)
                if strTyped == strTyper:
                    winsound.Beep(2500, 50)
                    msg = ""
                    if CPS > 3 and Accuracy > 90:
                        passed = True
                        gameover=True
                        points += round(CPS * Accuracy)
                        msg = "Congratulations!  You passed!  Press enter to continue!  Your total points are " + str(points)

                    else:
                        gameover=True
                        strTyped=""
                        mistakes=0
                        charnum=0
                        strTyper = createPhrase(sLength, i)
                        strikes+=1
                        if strikes <3:
                            msg = "You must type faster than 1 CPS and have accuracy greater than 90%.  Press enter to try again"
                        else:
                            msg = "Sorry!  Game over.  That's strike 3.  Your total points are " + str(points)
                    fontCont = pygame.font.Font('freesansbold.ttf', 16)
                    tsPause = fontCont.render(msg, True, WHITE, BLUE)
                    trPause = tsPause.get_rect()
                    trPause.center = (400, 250)
                    DISPLAYSURF.blit(tsPause, trPause)
                else:
                    if chr(event.key) == strTyper[charnum]:
                        strTyped += chr(event.key)
                        charnum += 1
                        winsound.Beep(1000, 5)
                    else:
                        winsound.Beep(5000,5)
                        mistakes+=1



        textSurfaceObj1 = fontObj.render(strTyper, True, WHITE, BLUE)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (300, 50)

        textSurfaceObj2 = fontObj.render(strTyped, True, WHITE, BLUE)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (300, 100)

        if len(strTyped)>0:
            CPS = round(len(strTyped)/(time.time()-starttime),2)
        else:
            CPS=0.0

        tsCPS  = fontObj.render(str(CPS) + " CPS", True, WHITE, BLUE)
        trCPS = tsCPS.get_rect()
        trCPS.center = (200, 200)

        if len(strTyped) > 0:
            Accuracy = round((1 - (mistakes / (len(strTyped)+mistakes)))*100,3)
        else:
            Accuracy=100.0

        tsAccuracy = fontObj.render(str(Accuracy) + "%", True, WHITE, BLUE)
        trAccuracy = tsAccuracy.get_rect()
        trAccuracy.center = (400, 200)



        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
        DISPLAYSURF.blit(tsCPS, trCPS)
        DISPLAYSURF.blit(tsAccuracy, trAccuracy)
        DISPLAYSURF.blit(imgKeyboard, rectKeyboard)
        DISPLAYSURF.blit(imgTouch, rectTouch)

        pygame.display.update()
        fpsClock.tick(FPS)

        if gameover:
            restart = False
            while not restart:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            if strikes < 3:
                                restart = True
                                gameover=False
                            else:
                                exit()




