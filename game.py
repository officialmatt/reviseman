import pygame 
import random

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN =(0,255,0)
RED      = (255,0,0)
PURPLE=(191,17,107)
LIGHTBLUE=(15,216,242)
LIGHTPURPLE=(242,15,227)
GREENISH=(15,242,113)
YELLOW=(255,255,0) 

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 660
flag3=False

class Food(pygame.sprite.Sprite): #This class is for the 'food'
    def __init__(self, colour, width, height,x,y):#each piece has attributes...
        pygame.sprite.Sprite.__init__(self)#...colour,width,height,x and y
        self.image=pygame.Surface([width,height])#Give each piece its width and height
        pygame.draw.ellipse(self.image, colour, [0, 0, width, height])#the food is an ellipse
        self.rect = self.image.get_rect()#Get the x and y coordinates
        self.rect.x=x#set the coordinates
        self.rect.y=y

def texts(text_flag, a,b,d,f): #Class for the questions from the file
    font=pygame.font.Font(None,30)#font definition
    qsFile = open("questions.txt", "r")#open file containing q and a's
    qLine = qsFile.read().splitlines()[a]#[a] determins which line in the file
    question=(qLine.split(",")[0])#[0] means the first part of line i.e question
    text=font.render(str(question), 1, (WHITE)) #turn question into text for screen

    correct_answer=(qLine.split(",")[1])#[1] means answer from samw line as above
    text1=font.render(str(correct_answer), 1, (colour1))

    qsFile = open("questions.txt", "r")#open file
    line2 = qsFile.read().splitlines()[b]#determins which line
    wrong_answer=(line2.split(",")[1])
    text2=font.render(str(wrong_answer), 1, (colour2))

    qsFile = open("questions.txt", "r")#open file
    line3 = qsFile.read().splitlines()[d]#determins which line
    wrong_answer2=(line3.split(",")[1])
    text3=font.render(str(wrong_answer2), 1, (colour3))

    qsFile = open("questions.txt", "r")#open file
    line4 = qsFile.read().splitlines()[f]#determins which line
    wrong_answer3=(line4.split(",")[1])
    text4=font.render(str(wrong_answer3), 1, (colour4))

    screen.blit(text3, (300,coord3))#Puts the text on the screen
    screen.blit(text4, (300,coord4))
    screen.blit(text, (300,560))
    screen.blit(text1, (300,coord1))
    screen.blit(text2, (300,coord2))

class Pill(pygame.sprite.Sprite): #Pill that when eaten will launch mode 2
    def __init__(self, colour, width, height):#has these attributes
        pygame.sprite.Sprite.__init__(self)#is a sprite
        self.image=pygame.Surface([width,height])#give it its width and height
        self.image.fill(colour)#Fill it with the specified colour
        self.rect = self.image.get_rect()#get the x and y position

class Player(pygame.sprite.Sprite):#The player class is defined as a sprite class
    def __init__(self):#Initiallising the class
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pacman5.png").convert()#Loading the image which will become the player
        self.left=pygame.transform.rotate(self.image,180)#Rotate 180 degrees
        self.down=pygame.transform.rotate(self.image,-90)#Rotate 90 degrees clockwise
        self.up=pygame.transform.rotate(self.image,90)#Rotate 90 degrees anti clockwise
        self.rect=self.image.get_rect()

    def move(self, dx, dy):#Dx and dy are supplied depending which key is pressed
        if dx != 0: #This is moving the x (dx) and y (dy) directions seperately
            self.move_player_direction(dx, 0)
        if dy != 0:
            self.move_player_direction(0, dy)

        if self.rect.x<0:#code for the tunnel
            self.rect.x=800 #off the screen to the right
        elif self.rect.x>800:#off the screen to the left
            self.rect.x=0
    
    def move_player_direction(self, dx, dy):      
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls: #Looping through the list containing the walls
            if self.rect.colliderect(wall.rect):#Automatically detects a collision
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left #The right position of the player
                                                    #equals the left of the wall
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right#The left position of the player
                                                    #equals the right of the wall
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top#The bottom position of the player
                                                    #equals the top of the wall
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom#The top position of the player
                                                    #equals the bottom of the wall


class Wall(object): #This defines the class "Wall" and sets it as an object
    
    def __init__(self,pos): #This assigns the value pos to each wall block
                            #which is its current position in an array
        walls.append(self) #When each block is created, it is added to the list
                           #called walls
        self.rect=pygame.Rect(pos[0],pos[1],10,10) #This makes the block a square
                                                   #of 10x10

blocklist=[]#some list definitions
enemyblocklist=pygame.sprite.Group()
player_list=pygame.sprite.Group()

class Enemy(pygame.sprite.Sprite): #Enemy class created


    cornered1=False  #this will stay changed if altered in a function
    cornered2=False     #this is top left cornered
    hitLeft=False
    hitRight=False
    hitBottom=False
    hitTop=False
    moving=True
    x=22
    calledPatrol=True
    formery=1
    formerx=1
    topLeftCorner=False
    topRightCorner=False
    hitBottomLeft=False
    hitBottomRight=False
    onPatrol=False
    bottomLeftCorner=False
    movingup=True
    collide=True
    start=True
    choice=-1
    def __init__(self, colour, width, height):
        pygame.sprite.Sprite.__init__(self)#enemy is a sprite
        self.image=pygame.Surface([width,height])#The image will have width and height
        self.image.fill(colour)#All enemies will have a different colour
        self.callenemy=False#used in patrol function
        self.rect = self.image.get_rect()#This finds the x and y coordinates
        self.speed=2#define speed
#########################
###########################
    def colour(self,colour):#Function to change colour of enemy
        self.image.fill(colour)
       
    def patrol(self): #This function generates a random number and
        if self.calledPatrol==True:#then assigns a target for one of the three enemys to go to
            x=random.randint(1,4)#random number
            if self.choice==x:
                self.patrol()
            else:
                self.choice=x   
            self.calledPatrol=False#only runs that code once
        
        if self.choice==1:#assigning the targets
            self.newgoLeft()
        elif self.choice==2:
            self.newgoRight()
        elif self.choice==3:
            self.newgoBottomRight()
        elif self.choice==4:
            self.newgoBottomLeft()
###################
##################
    def move(self, q, r, dx, dy):
        if self.rect.x>q:#q and r have been defined below
            dx=-1        #they are x and y pos of player
        if self.rect.x<q:#this is the x direction
            dx=1
        if self.rect.y>r:#this is the y direction
            dy=-1
        if self.rect.y<r:
            dy=1
        
        #We are moving x and y separately
        if dx != 0:
            self.move_enemy_direction(dx, 0)#Calling a separate function to move
        if dy != 0:
            self.move_enemy_direction(0, dy)

##############TARGET FUNCTIONS####################
    def newgoLeft(self): #Top Left Pill
        if not self.topLeftCorner:#Hasn't reached target
            self.rect.y-=1#Move up

        for wall in walls:#collision code
            if self.rect.colliderect(wall.rect):#If a collision is detected
                if self.rect.y<self.formery: #Moving up here
                    self.rect.y+=1
                    self.hitTop=True  #now he's hit the top
                    if self.hitTop and not self.hitRight:#Has hit the top but not the right and not at the very top
                        self.rect.x-=2#now moving left
                    elif self.hitTop==True and self.hitRight and self.rect.y!=10:#has hit top and right
                        self.rect.x+=2#so should move right
                    elif self.hitTop==True and self.hitLeft==True:#hit top and hit left
                        self.rect.x-=2#so needs to move left again
                    elif self.hitTop==True and self.rect.y==10 and self.hitRight: #is now in line with the pill
                        self.rect.x-=2
                        
                elif self.rect.x>self.formerx:#moving right
                    self.rect.x-=1
                    self.hitRight=False #flag to show moved has hit the right side
                    self.hitLeft=True #flag to show  hit left
                    
                elif self.rect.x<self.formerx:#moving left
                    self.rect.x+=1  #now needs to move right
                    self.bottomLeftCorner=False #not hit the bottom left
                    self.hitLeft=False #flag to show left side wasn't hit
                    self.hitRight=True #Has hit right again

                    if self.rect.y==10: #As the very top
                        self.topLeftCorner=True #Has hit the target
                        self.hitBottomRight=False #Has not hit the other targets
                        self.calledPatrol=True
                        self.onPatrol=False
                        self.hitBottomLeft=False
                        self.topRightCorner=False

        self.formery=self.rect.y#records the current postition before movement
        self.formerx=self.rect.x#records the current postition before movement

######################################################
##########GO RIGHT#########################
    def newgoRight(self):
        if not self.topRightCorner:#Hasn't reached target
            self.rect.y-=1#Move up

        for wall in walls:#collision code
            if self.rect.colliderect(wall.rect):#If a collision is detected
                if self.rect.y<self.formery: #Moving up here
                    self.rect.y+=1
                    self.hitTop=True  #now he's hit the top
                    if self.hitTop and not self.hitRight and self.rect.y!=10:#Has hit the top but not the right and not at the very top
                        self.rect.x-=2#now moving left
                    elif self.hitTop==True and self.hitRight:
                        self.rect.x+=2#so should move right
                    elif self.hitTop==True and self.hitLeft==True:#hit top and hit left
                        self.rect.x-=2#so needs to move left again
                    elif self.hitTop==True and self.rect.y==10 and not self.hitRight: #is now in line with the pill
                        self.rect.x+=2
                        
                elif self.rect.x>self.formerx:#moving right
                    self.rect.x-=1
                    self.hitRight=False #flag to show moved has hit the right side
                    self.hitLeft=True #flag to show  hit left

                    if self.rect.y==10: #As the very top
                        self.topLeftCorner=False #Has hit the target
                        self.hitBottomRight=False #Has not hit the other targets
                        self.hitBottomLeft=False
                        self.topRightCorner=True
                        self.calledPatrol=True
                        self.onPatrol=False
                        
                elif self.rect.x<self.formerx:#moving left
                    self.rect.x+=1  #now needs to move right
                    self.bottomLeftCorner=False #not hit the bottom left
                    self.hitLeft=False #flag to show left side wasn't hit
                    self.hitRight=True #Has hit right again

        self.formery=self.rect.y#records the current postition before movement
        self.formerx=self.rect.x#records the current postition before movement##################################################

#############################
#######BOTTOM LEFT##########
    def newgoBottomLeft(self):

        if not self.hitBottomLeft:#Hasn't reached target
            self.rect.y+=1#Move down

        for wall in walls:#collision code
            if self.rect.colliderect(wall.rect):#If a collision is detected
                if self.rect.y>self.formery: #Moving down here
                    self.rect.y-=1
                    self.hitBottom=True  #now he's hit the bottom
                    if self.hitBottom and not self.hitRight:#Has hit the bottom but not the right and not at the very top
                        self.rect.x-=2#now moving left
                    elif self.hitBottom==True and self.hitRight and self.rect.y!=510:#has hit bottom and right
                        self.rect.x+=2#so should move right
                    elif self.hitBottom==True and self.hitLeft==True:#hit bottom and hit left
                        self.rect.x-=2#so needs to move left again
                    elif self.hitBottom==True and self.rect.y==510 and self.hitRight: #is now in line with the pill
                        self.rect.x-=2

                elif self.rect.x>self.formerx:#moving right
                    self.rect.x-=1
                    self.hitRight=False #flag to show moved has hit the right side
                    self.hitLeft=True #flag to show  hit left
                    
                elif self.rect.x<self.formerx:#moving left
                    self.rect.x+=1  #now needs to move right
                    self.bottomLeftCorner=False #not hit the bottom left
                    self.hitLeft=False #flag to show left side wasn't hit
                    self.hitRight=True #Has hit right again

                    if self.rect.y==510: #At the very bottom
                        self.topLeftCorner=False #Has hit the target
                        self.hitBottomRight=False #Has not hit the other targets
                        self.hitBottomLeft=True
                        self.topRightCorner=False
                        self.calledPatrol=True
                        self.onPatrol=False

        self.formery=self.rect.y#records the current postition before movement
        self.formerx=self.rect.x#records the current postition before movement

#####################################
#############BOTTOM RIGHT##############
    def newgoBottomRight(self):

        if not self.hitBottomRight:#Hasn't reached target
            self.rect.y+=1#Move down

        for wall in walls:#collision code
            if self.rect.colliderect(wall.rect):#If a collision is detected
                if self.rect.y>self.formery: #Moving down here
                    self.rect.y-=1
                    self.hitBottom=True  #now he's hit the bottom
                    if self.hitBottom and not self.hitRight and self.rect.y!=510:#Has hit the bottom but not the right and not at the very top
                        self.rect.x-=2#now moving left
                    elif self.hitBottom==True and self.hitRight:
                        self.rect.x+=2#so should move right
                    elif self.hitBottom==True and self.hitLeft==True:#hit bottom and hit left
                        self.rect.x-=2#so needs to move left again
                    elif self.hitBottom==True and self.rect.y==510 and not self.hitRight: #is now in line with the pill
                        self.rect.x+=2
                elif self.rect.x>self.formerx:#moving right
                    self.rect.x-=1
                    self.hitRight=False #flag to show moved has hit the right side
                    self.hitLeft=True #flag to show  hit left

                    if self.rect.y==510: #As the very bottom
                        self.topLeftCorner=False #Has hit the target
                        self.hitBottomRight=True #Has not hit the other targets
                        self.hitBottomLeft=False
                        self.topRightCorner=False
                        self.calledPatrol=True
                        self.onPatrol=False
                        
                elif self.rect.x<self.formerx:#moving left
                    self.rect.x+=1  #now needs to move right
                    self.bottomLeftCorner=False #not hit the bottom left
                    self.hitLeft=False #flag to show left side wasn't hit
                    self.hitRight=True #Has hit right again

        self.formery=self.rect.y#records the current postition before movement
        self.formerx=self.rect.x#records the current postition before movement
##################################   
    def move_enemy_direction(self, dx, dy):      
        # Move the rect by the amount specified in move()
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):#Collision detection (as in player class)
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
###################################
###################################

def getScore():#Get current saved score
    # Default high score
    high_score = 0
    # Try to read the high score from a file
    high_score_file = open("highScores.txt", "r")#open file
    high_score = int(high_score_file.read())#turn into an integer
    high_score_file.close()#close the file
    return high_score#return score for comparrison

def addHighScore(score):#replace high score
    # Write the score to file
    high_score_file = open("highScores.txt", "w")
    high_score_file.write(str(score))#turn back into a string
    high_score_file.close()#close the file

# Call this function so the Pygame library can initialize itself
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) 
# Set the title of the window
pygame.display.set_caption("Matt's Project") 
allSprites = pygame.sprite.Group()# List to hold all the sprites
food_list = pygame.sprite.Group()#lists used during game
dotgroup=pygame.sprite.Group()
pill_group=pygame.sprite.Group()
foodlist=pygame.sprite.Group()
enemy1group=pygame.sprite.Group()
enemy2group=pygame.sprite.Group()
enemy3group=pygame.sprite.Group()
enemy4group=pygame.sprite.Group()
wall_list=pygame.sprite.Group()
block_list=pygame.sprite.Group()
enemy_list=pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
enemy1list = pygame.sprite.Group()
enemy2list = pygame.sprite.Group()
enemy3list = pygame.sprite.Group()
enemy4list = pygame.sprite.Group()
walls=[]
levels=[]
#add each map to the levels list
levels.append([
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                                                              W",
    "W  P       .   . . . . . . . . . . . .    . . . . . . . . . . . . . . .      P W",
    "W                                                                              W",
    "W                  .                 .    .               .                    W",
    "W    WWWWWWWWWWWWW    WWWWWWWWWWWWW    W    WWWWWWWWWWWWW      WWWWWWWWWWWW    W",
    "W  .   X           .                 .    .               .                 .  W",
    "W                                                                              W",
    "W  .       . . . . . . . . . . . . . . . . . .  . . . . . . . . . . . . . . .  W",
    "W                                                                              W",
    "W  . WWWWWWWWWWWWW .     .   WWWWWWWWWWWWWWWWWWWWW    .     .  WWWWWWWWWWWW .  W",
    "W                     W               W                   W                    W",
    "W  . . . . . . .   .  W  . . . . . .  W . . . . . . . .   W . . . . . . . . .  W",
    "W                     W               W                   W                    W",
    "W                  .  W            .  W .                 W .                  W",
    "WWWWWWWWWWWWWWWWWW    WWWWWWWWWWWW    W    WWWWWWWWWWWWWWWW    WWWWWWWWWWWWWWWWW",
    "W                W .  W            .    .                 W    W               W",
    "W                W    W                                   W    W               W",
    "W                W .  W  . . . . .   . . . . . . . . . .  W .  W               W",
    "W                W    W                                   W    W               W",
    "W                W         WWWWWWWWWWWWWWWWWWWWWWWWWWW         W               W",
    "W                W . . . . W                         W . . . . W               W",
    "WWWWWWWWWWWWWWWWWW         W                         W         WWWWWWWWWWWWWWWWW",
    "                   .     . W                         W .    .                   ",
    "                      W    W                         W    W                     ",
    "                   .  W  . W                         W    W .                   ",
    "                      W    WWWWWWWWWWWWWWWWWWWWWWWWWWW    W                     ",
    "WWWWWWWWWWWWWWWWWW .  W  .                             .  W .  WWWWWWWWWWWWWWWWW",
    "W                WB   W                                   W    W               W",
    "W                W .  W  . . . . . .   S . . . . . . . .  W .  W               W",
    "W                W    W                                   W    W               W",
    "W                W .  W  . WWWWWWWWWWWWWWWWWWWWWWWWWWW .  W .  W               W",
    "W                W                      W A                    W               W",
    "W                W . . . . . . . . . .  W    . . . . . . .  .  W               W",
    "W                W                      W                      W               W",
    "WWWWWWWWWWWWWWWWWW .                    W                   .  WWWWWWWWWWWWWWWWW",
    "W                     WWWWWWWWWWWWW     W    WWWWWWWWWWWWWW                    W",
    "W  . . . . . . . . .                                        . . . . . . . . . .W",
    "W                                                                              W",
    "W  .               .  . . . . . . . . . .       . . . . . . .               .  W",
    "W    WWWWWWWWWWWWW                                             WWWWWWWWWWWW    W",
    "W  .             W .   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW .  W            .  W",
    "W                W                      W                      W               W",
    "W  . . . . . . . W .  . . . . . . . . . W .D. . . . . . . . .  W  . . . . . .  W",
    "W                W                      W                      W               W",
    "W  . WWWWWWWW  . W .                    W                   .  W     WWWWWW    W",
    "W                      WWWWWWWWWWWWW    W    WWWWWWWWWWWWWW    W               W",
    "W  . . . . . . .   .   W           W    W    W            W .  W  . . . . . .  W",
    "W                      W           W    W    W            W                    W",
    "W  .               .   W           W         W            W .                  W",
    "W    WWWWWWWWWWWWW C   WWWWWWWWWWWWW         WWWWWWWWWWWWWW          WWWWWW    W",
    "W                                                           .                  W",
    "W                                                                              W",
    "W   P     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       P  W",
    "W                                                                              W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ])
levels.append([
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W           X                                                                  W",
    "W  P         .   . . . . . . . .  . . . . . . .   . .    . . . . . . . . . . P W",
    "W                                                                              W",
    "W  .               .                 .    .               .                 .  W",
    "W    WWWWWWWWWWWWW    WWWWWWWWWWWWW    W    WWWWWWWWWWWWW      WWWWWWWWWWWW    W",
    "W  . W             .              W  . W  . W             .               W .  W",
    "W    W                            W    W    W                             W    W",
    "W  . W     . . . . . . . . . . . .W  . W . .W.  . . . . . . . . . . . . . W .  W",
    "W    W                            W    W    W                  WWWWWWW    W    W",
    "W  . W    WWWWWW .  WWWWWWWWWW  .      W         WWWWWWWWWW    W          W .  W",
    "W    W         W                       W                       W          W    W",
    "W  . W . . . . W .       . . . . . .   W. . . . . . . .     . .W. . . . . W .  W",
    "W    W         W                       W                       W          W    W",
    "W    W         W                       W                       W          W    W",
    "W    W         W .    WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW .  W          W    W",
    "W         W    W                                               W     W         W",
    "W         W    W .                 .    .                      W     W         W",
    "W         W    W .     .   . . . .   . . . . . . . . . .    .  W     W         W",
    "W         W    W                                               W     W         W",
    "WWWWWW    W    W           WWWWWWWWWWWWWWWWWWWWWWWWWWW         W     W    WWWWWW",
    "     W    W       . .  . . W                         W . . . .       W    W     ",
    "     W    W                W                         W               W    W     ",
    "     W    W          W     W                         W    W          W    W     ",
    "     W    W       .  W   . W                         W    W .        W    W     ",
    "WWWWWW    W     W    W     WWWWWWWWWWWWWWWWWWWWWWWWWWW    W    W     W    WWWWWW",
    "W         W     W .  W   .                             .  W .  W     W         W",
    "W         W     WB   W                                    W    W     W         W",
    "W         W     W .  W  .  . . . . .     . . . . . . . .  W .  W     W         W",
    "W         W     W    W                                    W    W     W         W",
    "W               W .  WWWWWWWWWWWW      W      WWWWWWWWWWWWW .  W               W",
    "W               W                      W   A                   W               W",
    "W               W . . . . . . . . . .  W    .   . . . . .   .  W               W",
    "W               W                      W                       W               W",
    "W         WWWWWWW .                    W                    .  WWWWWWWW        W",
    "W                     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                    W",
    "W  . . . . . . . . .                                        . . . . . . . . . .W",
    "W                                                                              W",
    "W  .               .  . . . . . . . . . .       . . . . . . .               .  W",
    "W    WWWWWWWWWWWWW                                             WWWWWWWWWWWW    W",
    "W  .             W .   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW .  W            .  W",
    "W                W                      W  D                   W               W",
    "W                W                      W                      W               W",
    "W  . . . . . . . W .  . . . . . . . . . W . . . . . . . . . .  W  . . . . . .  W",
    "W                W                      W                      W               W",
    "WWWWWWWWWWW    . W .   WWWWWWWWWW       W      WWWWWWWWWWWW    W     WWWWWWWWWWW",
    "                                        W                                       ",
    "   . . . . . . .   .                    W                   .     . . . . . .   ",
    "                                        W                                       ",
    "                   .                                        .                   ",
    "WWWWWWWWWWW      WWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWW      WWWWWWWWWWW",
    "W  .                C                                       .                  W",
    "W                                                                              W",
    "W   P. . . . . . .   . . . . . . . . . . . . . . . . . . . . . . . . . . . . P W",
    "W                                                                              W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ])
levels.append([
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W          X          W            W         W           W                     W",
    "W  P  . . . . . . .   W            W . . . . W           W. . . .  . . . . . . W",
    "W                     W            W         W           W                     W",
    "W  .               .  W            W .     . W           W .                .  W",
    "W    WWWWWWWWWWWWW    WWWWWWWWWWWWWW    W    WWWWWWWWWWWWW     WWWWWWWWWWWW    W",
    "W  . W           W .                 .     .               .   W          W .  W",
    "W    W           W                                             W          W    W",
    "W  . W           W . . . . . . . . . . . . . .  . . . . . . . .W          W .  W",
    "W    W           W                                             W          W    W",
    "W  . WWWWWWWWWWWWW .  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW .  WWWWWWWWWWWW .  W",
    "W                     W                                   W                    W",
    "W  . . . . . . . . .  W                                   W . . . . . . . . .  W",
    "W                     W                                   W                    W",
    "W                  .  W                                   W .                  W",
    "WWWWWWWWWWWWWWWWWW    W                                   W    WWWWWWWWWWWWWWWWW",
    "W                W .  W                                   W .  W               W",
    "W                W .  W                                   W .  W               W",
    "W                W    W                                   W    W               W",
    "W                W    W                                   W .  W               W",
    "W                W . .W                                   W    W               W",
    "WWWWWWWWWWWWWWWWWW    WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW .  WWWWWWWWWWWWWWWWW",
    "                   .     .                             .                         ",
    "                                                            .                     ",
    "                                                                                 ",
    "                   .     .                                  .                    ",
    "                           WWWWWWWWWWWWWWWWWWWWWWWWWWW                           ",
    "W    WWWWWWWWWWWWW .  W  . W                         W .  W  . WWWWWWWWWWWW    W ",
    "W    W           WB   W    W                         W    W    W          W    W ",
    "W    W           W .  W  . W                         W .  W    W          W    W ",
    "W    W           W    W    W                         W    W    W          W    W ",
    "W    W           W .  W  . WWWWWWWWWWWWWWWWWWWWWWWWWWW .  W .  W          W    W ",
    "W    W           W    W                 W                 W    W          W    W ",
    "W    W           W    W  . . . . . . . .W  . . . . . . . .W    W          W    W ",
    "W    WWWWWWWWWWWWW .  W                 W                 W .  WWWWWWWWWWWW    W ",
    "W                     W                 W  .              W                    W",
    "W  . . . . . . . . .  WWWWWWWWWWWWW          WWWWWWWWWWWWWW . . . . . . . . . .W",
    "W                                          .                                   W",
    "W  .               .  . . . . . . . A. . .       . . . . . . .               . W",
    "W  .                                       .                                  .W",
    "WWWWWW    WWWWWWWW                                             WWWWWWW    WWWWWW",
    "W  .             W .   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW .  W            .  W",
    "W                W                      W                      W               W",
    "W  . . . . . . . W .  . . . . . . . . . W .D. . . . . . . . .  W  . . . . . .  W",
    "W                W                      W                      W               W",
    "W  . WWWWWWWW  . W .                    W                   .  W     WWWWWW    W",
    "W    W      W          WWWWWWWWWWWWW    W    WWWWWWWWWWWWWW    W     W    W    W",
    "W  . W      W. .   .   W           W    W    W            W .  W  . .W    W .  W",
    "W    W      W          W           W    W    W            W          W    W    W",
    "W  . W      W      .   W           W         W            W .        W    W    W",
    "W    WWWWWWWW          WWWWWWWWWWWWW         WWWWWWWWWWWWWW          WWWWWW    W",
    "W  .               C                                        .                  W",
    "W                                                                              W",
    "W   3. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 W",
    "W                                                                              W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ])

def drawMap(mapNo):#draw map function
    global pill1 #All of these variables must be set as global
    global pill2 # so that they exist throughout all of the code
    global block
    global enemy1
    global enemy2
    global enemy3
    global enemy4
    global player
    global enemy1startx
    global enemy1starty
    global enemy2startx
    global enemy2starty
    global enemy3startx
    global enemy3starty
    global enemy4startx
    global enemy4starty
    global playerstartx
    global playerstarty    
    x = 0 #The first block is drawn at 0,0
    y = 0 #which is the top left corner
    for row in levels[mapNo]: #mapNo is initially 1 and will incremnt each time
        for col in row:
            if col == "W": #If W then draw a wall block
               wall = Wall((x,y))
            if col== ".": #If a . then draw a food piece
                food=Food(GREEN,10,10,x,y)
                foodlist.add(food) #This adds each piece to the relavent lists
                all_sprites_list.add(food)
                food_list.add(food)#add each piece to this list

            if col== "A":#Creating the enemies
                enemy1 = Enemy(RED, 40, 40)
                enemy1startx=x#defining the start positions
                enemy1starty=y
                enemy1.rect.x=x#Current position
                enemy1.rect.y=y
                all_sprites_list.add(enemy1)#add to lists
                enemy_list.add(enemy1)
                enemyblocklist.add(enemy1)
                enemy1list.add(enemy1)

            if col== "B":
                enemy2 = Enemy(GREEN, 40, 40)
                enemy2.rect.x=x
                enemy2.rect.y=y
                enemy2startx=x
                enemy2starty=y
                all_sprites_list.add(enemy2)
                enemy_list.add(enemy2)
                enemyblocklist.add(enemy2)
                enemy2list.add(enemy2)

            if col== "C":
                enemy3 = Enemy(BLUE, 40, 40)
                enemy3.rect.x=x
                enemy3.rect.y=y
                enemy3startx=x
                enemy3starty=y
                all_sprites_list.add(enemy3)
                enemy_list.add(enemy3)
                enemyblocklist.add(enemy3)
                enemy3list.add(enemy3)

            if col== "D":
                enemy4 = Enemy(PURPLE, 40, 40)
                enemy4.rect.x=x
                enemy4.rect.y=y
                enemy4startx=x
                enemy4starty=y
                all_sprites_list.add(enemy4)
                enemy_list.add(enemy4)
                enemyblocklist.add(enemy4)
                enemy4list.add(enemy4)

            if col== "P":#Create the pill
                pill = Pill(RED, 15, 15)
                pill.rect.x=x#position on ma
                pill.rect.y=y
                all_sprites_list.add(pill)#add to lists
                pill_group.add(pill)

            if col== "X":
                player = Player()#Creating the player
                player.rect.x=x#position on map
                player.rect.y=y
                playerstartx=x
                playerstarty=y
                all_sprites_list.add(player)#add to lists
                player_list.add(player)

            x += 10#Here we increment x by 1p which is the size of one block
        y += 10#Here we move down the page
        x = 0

current_map=0 #Set the first map to appear in the game
drawMap(current_map) #Drawing the map onto the screen including the enemies, pills and player
clock = pygame.time.Clock()
score=0#initialise score as 0
correct=True#Initialise flags used throughout game
mode=0
been_caught=0
game_start=1
level_completed=False
Flagx=0
Flagy=0
level_no =1#initialise level number
food_eaten=0
gotBottomLeftPill=False
hit_enemy=False
hit=False
lostallLives=False
done = False
font = pygame.font.SysFont('Calibri', 36, True, False)
RESETEVENT=pygame.USEREVENT+1
#-------------------------------------Main Program Loop--------------------------------------------
start_screen=True #This is the start screen
while start_screen==True:
    screen.fill(BLACK)#Black background    
    instructions= pygame.image.load("instructions.png").convert()#Labeled image
    begin= pygame.image.load("begin.png").convert()#Click to begin image
    myfont=pygame.font.SysFont("Britannic Bold", 40)#Defining different fonts
    myfont2=pygame.font.SysFont("Britannic Bold", 30)
    myfont3=pygame.font.SysFont("Britannic Bold", 75)

    welcome=myfont3.render("Welcome", 1, (255, 0, 0))#All of the text that will be on the screen
    escape=myfont.render("Press escape to exit", 1, (255, 0, 0))
    howPlay=myfont2.render("How to play:", 1, (WHITE))#Instructions
    arrows=myfont2.render("Use the arrow keys to move the player", 1, (WHITE))
    increaseScore=myfont2.render("Eat the green food to increase your score", 1, (WHITE))
    mode2activation=myfont2.render("Eat the red pill to activate mode 2", 1, (WHITE))
    answering=myfont2.render("Match up the colour of the answer with the colour of the enemy", 1, (WHITE))
    scoreChange=myfont2.render("Eat the enemy and watch score change", 1, (WHITE))

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            start_screen=False#If mouse is clicked, start game
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Escape pressed - game quits")
                pygame.quit()#quit if escape is pressed
                sys.exit()
            
    screen.blit(howPlay,(0,100))#Output all of the above to the screen
    screen.blit(arrows,(0,150))#at specified x and y coordinates
    screen.blit(increaseScore,(0,175))
    screen.blit(mode2activation,(0,200))
    screen.blit(answering,(0,225))
    screen.blit(scoreChange,(0,250))
    screen.blit(escape,(525,0))
    screen.blit(instructions,(25,300))
    screen.blit(begin,(500,400))
    screen.blit(welcome,(10,0))
    
    pygame.display.update()#update the screen
    clock.tick(30)#number of clock ticks


running = True #Main game now
while running:#Main program loop
    clock.tick(60)#Set the clock ticks
    
    for e in pygame.event.get():#Stop running if quit
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False #escape to quit

        if e.type==RESETEVENT:#what to do if userevent is called
            mode=0  #ghosts not scared any more
            game_start=1#reset all variables to mode 1 
            flag3=False
            pygame.time.set_timer(RESETEVENT, 0)
            
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()#This finds out what key was pressed
    if key[pygame.K_LEFT]:
        player.move(-4, 0)#These are (x,y) coordinates
        player.image=player.left#rotate the image
    if key[pygame.K_RIGHT]:        
        player.move(4, 0)
        player.image = pygame.image.load("pacman5.png").convert()#starting direction
        player.image.set_colorkey(WHITE)
    if key[pygame.K_UP]:        
        player.move(0, -4)#rotate the image
        player.image=player.up
    if key[pygame.K_DOWN]:
        player.move(0, 4)#rotate the image
        player.image=player.down


    q=player.rect.x #original position of player
    r=player.rect.y
    originalx=enemy1.rect.x #original positions of enemies
    originaly=enemy1.rect.y
    originalx2=enemy2.rect.x
    originaly2=enemy2.rect.y
    originalx3=enemy3.rect.x
    originaly3=enemy3.rect.y
    originalx4=enemy4.rect.x
    originaly4=enemy4.rect.y
    #------------------------Game logic----------------------
    for x in enemyblocklist: #works out where enemy is relative to player
        if x.rect.x>q:
            dx=-1#used when calling move function below
        if x.rect.x<q:
            dx=1#used when calling move function below
        if x.rect.y>r:
            dy=-1#used when calling move function below
        if x.rect.y<r:
            dy=1#used when calling move function below

    while game_start==1:#Game start defined as 1 above
        enemy1.x=random.randint(0,3) #assign these variables to a random number
        enemy2.x=random.randint(0,3)#between 0 and 3
        enemy3.x=random.randint(0,3)
        
        game_start=2 #game start is 2
        mode=1 #now mode is 1

    if enemy1.x==0: #assigning a target depending of the number above
        enemy1.newgoLeft()
    elif enemy1.x==1:
        enemy1.newgoRight()
    elif enemy1.x==2:
        enemy1.newgoBottomLeft()
    elif enemy1.x==3:
        enemy1.newgoBottomRight()

    if enemy2.x==0:
        enemy2.newgoLeft()
    elif enemy2.x==1:
        enemy2.newgoRight()
    elif enemy2.x==2:
        enemy2.newgoBottomLeft()
    elif enemy2.x==3:
        enemy2.newgoBottomRight()

    if enemy3.x==0:
        enemy3.newgoLeft()
    elif enemy3.x==1:
        enemy3.newgoRight()
        enemy3.newgoBottomLeft()
    elif enemy3.x==3:
        enemy3.newgoBottomRight()

    #if mode==1:#this used to be in an if - now occurs at any time (mode0,1 or 2)
    if enemy1.topLeftCorner==True or enemy1.topRightCorner==True or enemy1.hitBottomLeft==True or enemy1.hitBottomRight==True:
        enemy1.x=22 #this is set to any number that isn't 0-3 so that the above code won't run
        enemy1.patrol()#now patrol is called
    if enemy2.topLeftCorner==True or enemy2.topRightCorner==True or enemy2.hitBottomLeft==True or enemy2.hitBottomRight==True:
        enemy2.x=22
        enemy2.patrol()
    if enemy3.topLeftCorner==True or enemy3.topRightCorner==True or enemy3.hitBottomLeft==True or enemy3.hitBottomRight==True:
        enemy3.x=22
        enemy3.patrol()

    enemy4.move(q,r,dx,dy) #chase the player
    
    if mode==1 or mode==0: #Only occurs at start up or mode 1
        enemy1.colour(RED)#Turns each enemy their specific colour
        enemy2.colour(GREEN)
        enemy3.colour(BLUE)
        enemy4.colour(PURPLE)
        
    if mode==2: #Only occurs in mode 2
        enemy1.colour(LIGHTBLUE)
        enemy2.colour(LIGHTPURPLE)
        enemy3.colour(GREENISH)
        enemy4.colour(YELLOW)

    if mode==1:#Detecting collision between player and enemy during mode 1 - player disappears
        playerVenemy=pygame.sprite.groupcollide(player_list, enemyblocklist, True, False)
 
        
    if mode==2:#Lists between player and each enemy - player remains visible, enemy disappears
        list5=pygame.sprite.groupcollide(player_list, enemy1list, False, True)
        list6=pygame.sprite.groupcollide(player_list, enemy2list, False, True)
        list7=pygame.sprite.groupcollide(player_list, enemy3list, False, True)
        list8=pygame.sprite.groupcollide(player_list, enemy4list, False, True)
          
    foodEaten=pygame.sprite.groupcollide(player_list, foodlist, False, True)#Collision between player and food
    modedetector=pygame.sprite.groupcollide(player_list, pill_group, False, True)

    if len(food_list)==0: #no more food left
        level_completed=True#so level is complete

    if len(playerVenemy)!=0:#Mode 1 collision detected 
        been_caught+=1#Player has been caught 
        player = Player()#Creating the player again
        player.rect.x=playerstartx
        player.rect.y=playerstarty
        all_sprites_list.add(player)
        player_list.add(player)


    if mode==2 and len(list5)!=0:#collision detected between player and enemy
        hit=True #create a flag showing an enemy has been hit
        enemy1 = Enemy(RED, 40, 40)#call the enemy class again to create a new objec
        enemy1.rect.x=enemy1startx#position to redraw the enemy
        enemy1.rect.y=enemy1starty
        all_sprites_list.add(enemy1)#add to all lists again
        enemy_list.add(enemy1)
        enemyblocklist.add(enemy1)
        enemy1list.add(enemy1)
        enemyhitcolour=LIGHTBLUE#Variable containing mode 2 colour

    if mode==2 and len(list6)!=0:
        hit=True
        enemy2 = Enemy(GREEN, 40, 40)
        enemy2.rect.x=enemy2startx
        enemy2.rect.y=enemy2starty
        all_sprites_list.add(enemy2)
        enemy_list.add(enemy2)
        enemyblocklist.add(enemy2)
        enemy2list.add(enemy2)
        enemyhitcolour=LIGHTPURPLE#Variable containing mode 2 colour

    if mode==2 and len(list7)!=0:
        hit=True 
        enemy3 = Enemy(BLUE, 40, 40)
        enemy3.rect.x=enemy3startx
        enemy3.rect.y=enemy3starty
        all_sprites_list.add(enemy3)
        enemy_list.add(enemy3)
        enemyblocklist.add(enemy3)
        enemy3list.add(enemy3)
        enemyhitcolour=GREENISH#Variable containing mode 2 colour

    if mode==2 and len(list8)!=0:
        hit=True
        enemy4 = Enemy(PURPLE, 40, 40)
        enemy4.rect.x=enemy4startx
        enemy4.rect.y=enemy4starty
        all_sprites_list.add(enemy4)
        enemy_list.add(enemy4)
        enemyblocklist.add(enemy4)
        enemy4list.add(enemy4)
        enemyhitcolour=YELLOW#Variable containing mode 2 colour

    while hit==True:#A question has been answered
        if enemyhitcolour==colour1:#Colour 1 is the colour of correct answer
            score=score+100#correct so increment score by 100
            hit=False#no longer hit
            print(score)  
        else:
            score=0#Wrong, so score is 0
            hit=False#Hit no longer True

    font = pygame.font.SysFont('Calibri', 25, True, False)#defining font
    text = font.render(str(score),True,WHITE)#used for score displayed on screen
    
    
    if len(modedetector)!=0:#This works out if the player has eaten a pill. If so then the mode is changed to 2
        mode=2 #change the mode to 2
        pygame.time.set_timer(RESETEVENT, 10000)  #set the timer to start  defined RESTARTEVENT in that number of milliseconds
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall)

    heartx=725#X position of first heart on screen
    while heartx<800:#Repeats for all three hearts
        full_lives = pygame.image.load("heartfill.png").convert()
        full_lives.set_colorkey(WHITE)#All three lives still
        hearty=590#Y value
        screen.blit(full_lives, [heartx,hearty])#Print to screen
        heartx=heartx+25#Move on to next heart
    if been_caught==1:#One life lost - unfill a heart
        lost_lives = pygame.image.load("heartempty.png").convert()
        lost_lives.set_colorkey(WHITE)#Removes background of image
        hearty=590#x and y coords 
        heartx=725
        screen.blit(lost_lives, [heartx,hearty])
    if been_caught==2:#two lives lost
        lost_lives = pygame.image.load("heartempty.png").convert()
        lost_lives.set_colorkey(WHITE)
        hearty=590#x and y coords 
        heartx=725
        screen.blit(lost_lives, [heartx,hearty])
        lost_lives2 = pygame.image.load("heartempty.png").convert()
        lost_lives2.set_colorkey(WHITE)
        hearty=590#x and y coords 
        heartx=750
        screen.blit(lost_lives2, [heartx,hearty])
    if been_caught==3:#All lives now lost - no more filled hearts
        lostallLives=True #Flag showing all lives lost
        lost_lives = pygame.image.load("heartempty.png").convert()
        lost_lives.set_colorkey(WHITE)
        hearty=590#x and y coords 
        heartx=725
        screen.blit(lost_lives, [heartx,hearty])
        lost_lives2 = pygame.image.load("heartempty.png").convert()
        lost_lives2.set_colorkey(WHITE)
        hearty=590#x and y coords 
        heartx=750
        screen.blit(lost_lives2, [heartx,hearty])
        lost_lives3 = pygame.image.load("heartempty.png").convert()
        lost_lives3.set_colorkey(WHITE)
        hearty=590#x and y coords 
        heartx=775
        screen.blit(lost_lives3, [heartx,hearty])

    if len(modedetector)!=0: #mode is 2
        text_flag=True
        flag3=True
        c=0  
        if flag3==True: #only when this flag is true and mode is 2
            question_list=(random.sample((0,1,2,3,4,5),4))
            question_order=random.sample((1,2,3,4),4)
            a=question_list[0]#assign each variable a number
            b=question_list[1]
            d=question_list[2]
            f=question_list[3]
            c=random.randint(1,2)
            x=random.randint(1,3)        

    for food in foodEaten: #loop through list
        score=score+1#increment score

    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render(str(score),True,WHITE)#turn score into a string, give colour
    
    if len(modedetector)!=0: #This deals with the question which is being asked 
        j=random.randint(1,3) 
        colourint=random.sample((1,2,3,4),4)
        question_order=random.sample((1,2,3,4),4)
        if colourint[0]==1: #This assigns each answer with a different colour. The random
                            #numbers are used so that the answers are not the same colour each time
            colour1=LIGHTBLUE
            colour2=LIGHTPURPLE
            colour3=GREENISH
            colour4=YELLOW
        elif colourint[0]==2:
            colour1=YELLOW
            colour2=LIGHTBLUE
            colour3=LIGHTPURPLE
            colour4=GREENISH
        elif colourint[0]==3:
            colour1=GREENISH
            colour2=YELLOW
            colour3=LIGHTBLUE
            colour4=LIGHTPURPLE
        elif colourint[0]==4:
            colour1=LIGHTPURPLE
            colour2=GREENISH
            colour3=YELLOW
            colour4=LIGHTBLUE
        if question_order[0]==1: #This now sets the order which the questions are displayed.
            coord1=580          #Otherwise the correct answer will always be in the same                    
            coord2=600          #position which will become apparent to the player
            coord3=620
            coord4=640
        elif question_order[1]==1:
            coord1=600
            coord2=620
            coord3=640
            coord4=580
        elif question_order[2]==1:
            coord1=620
            coord2=640
            coord3=580
            coord4=600
        elif question_order[3]==1:
            coord1=640
            coord2=580
            coord3=600
            coord4=620


    if flag3==True: #Once the above has been completed, the texts function is 
        texts(text_flag, a,b,d,f) #called which will actually display the question and answers on the screen
        
    if lostallLives:#Game will now restart
        game_start=1#reset all variables
        been_caught=0
        high_score = getScore() #This now checks the current score...
        if score> high_score:# and works out if it becomes the high score 
            addHighScore(score)
        player_list.remove(player)#Remove all items from lists
        all_sprites_list.remove(player,enemy1,enemy2,enemy3,enemy4)
        enemyblocklist.remove(enemy1,enemy2,enemy3,enemy4)
        enemy1list.remove(enemy1)
        enemy2list.remove(enemy2)
        enemy3list.remove(enemy3)
        enemy4list.remove(enemy4)
        lostallLives=False
        pygame.time.delay(4000) #This pauses the screen for 4000ms before the game restarts 
        level_no=1#back to level 1
        current_map=0
        score=0
        drawMap(current_map)#Re-draw the map

    if level_completed:#level complete
        game_start=1#reset all variables
        been_caught=0
        player_list.remove(player)#remove all items from the lists
        all_sprites_list.remove(player,enemy1,enemy2,enemy3,enemy4)
        enemyblocklist.remove(enemy1,enemy2,enemy3,enemy4)
        enemy1list.remove(enemy1)
        enemy2list.remove(enemy2)
        enemy3list.remove(enemy3)
        enemy4list.remove(enemy4)
        high_score = getScore() #This now checks the current score...        
        if score> high_score:# and works out if it becomes the high score 
            addHighScore(score)#if so, replace old high score with new one
        lostallLives=False
        pygame.time.delay(4000) #This pauses the screen for 4000ms before the game restarts 
        walls=[] #empty list so new map not drawn over old map
        current_map+=1#the map will now be the next one in the list
        drawMap(current_map)#draw new map
        restart=True
        level_completed=False
        level_no+=1 #next level

    font = pygame.font.SysFont('Calibri', 25, True, False)
    high_score=getScore()#Get high score from function
    highScore1 = font.render(str(high_score),True,WHITE)#Turn into string
    highScore2 = font.render("High Score",True,WHITE)#Text that says 'High Score'
    screen.blit(highScore1, [50, 585])#Put these two items on the screen
    screen.blit(highScore2, [10, 565])
    levelWord = font.render("Level",True,WHITE)#Text that says 'Level'
    level_current = font.render(str(level_no),True,WHITE)#Turn into string
    screen.blit(level_current, [170, 585])#Put these two items on the screen
    screen.blit(levelWord, [150, 565])
    all_sprites_list.draw(screen)
    screen.blit(text, [750, 565])#output to screen at 750,565
    pygame.display.flip()
pygame.quit()
