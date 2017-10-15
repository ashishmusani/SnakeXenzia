import pygame, sys, random
from pygame.locals import *

import pymysql as MySQLdb


screenX = 1210
screenY = 710
snakeSegSize = 20   #defines pixels occupied by each snake block


def overlap(x0, y0, fX, fY, lenS, lenF):
    foodCenterX = fX + (lenF/2) 
    foodCenterY = fY + (lenF/2) 
    if (x0<=foodCenterX and foodCenterX<=x0+lenS and y0<=foodCenterY and foodCenterY<=y0+lenS):
        return True
    else:
        return False


def checkWallCollide(headX, headY):
    if(headX<0 or headX>screenX-snakeSegSize or headY<0 or headY>screenY-snakeSegSize):
        return True
    else:
        return False

def checkInternalCollide(X0, Xi, Y0, Yi, lenS, lenF):
    CenterX = X0 + (lenF/2) 
    CenterY = Y0 + (lenF/2) 
    if (Xi<=CenterX and CenterX<=Xi+lenS and Yi<=CenterY and CenterY<=Yi+lenS):
        return True
    else:
        return False

def checkObstacleCollide(X0, Xi, Y0, Yi, lenS, lenO):
    CenterX = X0 + (lenS/2) 
    CenterY = Y0 + (lenS/2) 
    if (Xi<=CenterX and CenterX<=Xi+lenO and Yi<=CenterY and CenterY<=Yi+lenO):
        return True
    else:
        return False

#################################################################### DIE() Function ###########################################################################
def die(score):
    Display.fill((255,255,255))


    exitText =  "Game Over ! Your score is "+ str(score) +". "

    # render text
    exit_msg = myfont.render(exitText, 1, (255,0,0))
    Display.blit(exit_msg, (400, 100))


    
    #exit button
    exitButtonStartX = 500
    exitButtonStartY = 350
    exitButtonWidth = 125
    exitButtonHeight = 50

    #Blit "Exit" button
    pygame.draw.rect(Display, (0,0,255), (exitButtonStartX,exitButtonStartY,exitButtonWidth,exitButtonHeight))

    #Blit "Exit" label on button
    Display.blit(gameFont.render("Exit", 1, (255,255,255)), (exitButtonStartX+20,exitButtonStartY+15))
    pygame.display.update()    
	
    #HighScoreList variables
    scorelistX=400
    scorelistY=450
	

    while True:

        mouseLocX, mouseLocY = pygame.mouse.get_pos()
        pygame.draw.rect(Display, (0,0,255), (exitButtonStartX,exitButtonStartY,exitButtonWidth,exitButtonHeight))
        Display.blit(gameFont.render("Exit", 1, (255,255,255)), (exitButtonStartX+30,exitButtonStartY+15))
        
        if(mouseLocX >= exitButtonStartX and mouseLocX <= exitButtonStartX+exitButtonWidth and
              mouseLocY >= exitButtonStartY and mouseLocY <= exitButtonStartY+exitButtonHeight):
                    pygame.draw.rect(Display, (255,0,0), (exitButtonStartX,exitButtonStartY,exitButtonWidth,exitButtonHeight))
                    Display.blit(gameFont.render("Exit", 1, (255,255,255)), (exitButtonStartX+30,exitButtonStartY+15))
                    pygame.display.update()
        else :
                    pygame.draw.rect(Display, (0,0,255), (exitButtonStartX,exitButtonStartY,exitButtonWidth,exitButtonHeight))
                    Display.blit(gameFont.render("Exit", 1, (255,255,255)), (exitButtonStartX+30,exitButtonStartY+15))
                    pygame.display.update()


        #Game exit conditions
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN :
                clickPosX, clickPosY = pygame.mouse.get_pos()
                
                if(clickPosX >= exitButtonStartX and clickPosX <= exitButtonStartX+exitButtonWidth and
                       clickPosY >= exitButtonStartY and clickPosY <= exitButtonStartY+exitButtonHeight):
                            pygame.quit()
                            sys.exit()

            elif e.type == KEYDOWN and e.key ==K_ESCAPE :
                pygame.quit()
                sys.exit()




#################################################################### DIE() Function ends ###########################################################################



############################################################################# MAIN ###########################################################################
pygame.init()

clk = pygame.time.Clock()

myfont = pygame.font.SysFont("monospace", 15)

screen = (screenX,screenY)
Display = pygame.display.set_mode(screen)
Display.fill((255,255,255))


pygame.display.set_mode(screen, pygame.FULLSCREEN)
pygame.display.set_caption('Snake Xenzia')


#SNAKE Variables
xCord = [347,347+(1*snakeSegSize),347+(2*snakeSegSize),347+(3*snakeSegSize),347+(4*snakeSegSize)]        #Array to store x coordinates of the segment
yCord = [350,350,350,350,350]   #Array to store y coordinates of the segment
currentDir = 3; #Direction variable 0->up 1->right 2->down 3->left
imgSeg = pygame.Surface((snakeSegSize,snakeSegSize))    #Snake Segments
imgSeg.fill((255,0,0))

#FOOD Variables
food = pygame.Surface((5,5))      #Food surface
food.fill((0,0,255))
foodX = random.randint(snakeSegSize,screenX-20)
foodY = random.randint(snakeSegSize,screenY-20)


#IN-GAME Variables
gameFont = pygame.font.SysFont("monospace",20)
score = 0
addScore = 10
baseFreq = 1
freq = baseFreq

#Obstacle Variables
obstacleActive=False
obstacleX = 500
obstacleY = 300
obstacleDimension = 100
obstacleDimension = 100
obstacle = pygame.Surface((obstacleDimension,obstacleDimension))
obstacle.fill((255,0,0))


#MAIN INFINITE LOOP
while True:

    
    clk.tick(freq)
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit();sys.exit();
        elif e.type == KEYDOWN:
            if e.key == K_UP and currentDir != 2:
                currentDir = 0
            elif e.key == K_DOWN and currentDir != 0:
                currentDir = 2
            elif e.key == K_LEFT and currentDir != 1:
                currentDir = 3
            elif e.key == K_RIGHT and currentDir != 3:
                currentDir = 1
            elif e.key == K_r:
                imgSeg.fill((255,0,0))
            elif e.key == K_g:
                imgSeg.fill((0,255,0))
            elif e.key == K_b:
                imgSeg.fill((0,0,255))
            elif e.key == K_ESCAPE:
                pygame.quit();sys.exit();
            elif e.key == K_f:
                freq+=2
                addScore += 5
            elif e.key == K_s:
                if(freq != baseFreq):
                    freq-=2
                    addScore-=5

    #Check food overlap
    #--------------------------------------------------------------------
    if(overlap(xCord[0],yCord[0],foodX,foodY,snakeSegSize,5)):
        foodX = random.randint(snakeSegSize,screenX-20)       
        foodY = random.randint(snakeSegSize,screenY-20)       
        score += addScore
        xCord.append(screenX)
        yCord.append(screenY)
    #--------------------------------------------------------------------

        
    #Move Snake
    #--------------------------------------------------------------------
    count = len(xCord)-1
    while(count>=1):
        xCord[count] = xCord[count-1]
        yCord[count] = yCord[count-1]
        count -= 1        

    if(currentDir == 0):
        yCord[0] -= snakeSegSize
    elif (currentDir == 1):
        xCord[0] += snakeSegSize
    elif (currentDir == 2):
        yCord[0] += snakeSegSize
    elif (currentDir == 3):
        xCord[0] -= snakeSegSize
    #--------------------------------------------------------------------


    Display.fill((255,0,0))
    pygame.draw.rect(Display,(255,255,255), (5,5,1200,700)) 


    #blit snake blocks
    #--------------------------------------------------------------------
    for count in range (0, len(xCord)):   
        Display.blit(imgSeg,(xCord[count],yCord[count]))
    #--------------------------------------------------------------------

    #blit food block
    #--------------------------------------------------------------------
    Display.blit(food,(foodX,foodY))
    #--------------------------------------------------------------------

    #blit obstacle block
    #--------------------------------------------------------------------
    if (score>500) :
        obstacleActive=True

    if obstacleActive == True:
        Display.blit(obstacle,(obstacleX,obstacleY))
    #--------------------------------------------------------------------

        
    #Check Wall Collide Condition
    #--------------------------------------------------------------------
    if (checkWallCollide(xCord[0], yCord[0])):
            die(score);
    #--------------------------------------------------------------------


    #Check Obstacle Collide Condition
    #--------------------------------------------------------------------
    if obstacleActive == True:
        if(checkObstacleCollide(xCord[0],obstacleX,yCord[0],obstacleY,snakeSegSize,obstacleDimension)):
            die(score);
    #--------------------------------------------------------------------


    #Check Internal Collide Condition
    #--------------------------------------------------------------------
    count = len(xCord)-1
    while(count>=2):
        if(checkInternalCollide(xCord[0],xCord[count],yCord[0],yCord[count],snakeSegSize,5)):
            die(score);
        count = count-1
    #--------------------------------------------------------------------

    #update score
    #--------------------------------------------------------------------
    scoreLabel = gameFont.render("Your Score : " + str(score) + "  Speed : " + str(freq),1,(255,0,0))
    Display.blit(scoreLabel, (500,10))
    #--------------------------------------------------------------------

    pygame.display.update()
############################################################################# MAIN ends ###########################################################################
