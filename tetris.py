import pygame as pg

from pygame.locals import *
import numpy as np
import sys
import random as rd

class Tiles:
    def __init__(self):
        self.type=rd.randint(1,7)
        self.tile=np.arange(16).reshape(4,4)
        self.tile.fill(0)
        self.pos=np.array([3,0])
        
        if (self.type==1):
            self.tile[0,2]=1
            self.tile[1,2]=1
            self.tile[2,2]=1
            self.tile[3,2]=1
            self.color=(0,127,255)
            self.size=np.array([[0,3],[2,2]])
        if (self.type==2):
            self.tile[1,1]=1
            self.tile[1,2]=1
            self.tile[2,2]=1
            self.tile[2,3]=1
            self.color=green
            self.size=np.array([[1,2],[1,3]])
        if (self.type==3):
            self.tile[1,1]=1
            self.tile[1,2]=1
            self.tile[2,1]=1
            self.tile[2,2]=1
            self.color=(255,255,0)
            self.size=np.array([[1,2],[1,2]])
        if (self.type==4):
            self.tile[2,1]=1
            self.tile[2,2]=1
            self.tile[1,2]=1
            self.tile[1,3]=1
            self.color=red
            self.size=np.array([[1,2],[1,3]])
        if (self.type==5):
            self.tile[1,1]=1
            self.tile[2,1]=1
            self.tile[2,2]=1
            self.tile[2,3]=1
            self.color=(255,180,0)
            self.size=np.array([[1,2],[1,3]])
        if (self.type==6):
            self.tile[2,1]=1
            self.tile[1,1]=1
            self.tile[1,2]=1
            self.tile[1,3]=1
            self.color=blue
            self.size=np.array([[1,2],[1,3]])
        if (self.type==7):
            self.tile[1,2]=1
            self.tile[2,2]=1
            self.tile[2,1]=1
            self.tile[3,2]=1
            self.color=(127,0,255)
            self.size=np.array([[1,3],[1,2]])
        #print("type",self.type)
        nb=rd.randint(0,3)
        for i in range(0,nb):
            self.rotate(True)
       
        #self.display()

    def rotate(self,way):
        next=np.arange(16).reshape(4,4)
        for j in range(0,4):
            for i in range(0,4):
                if (way):
                    next[3-j,i]=self.tile[i,j]
                else:
                    next[j,3-i]=self.tile[i,j]
        mem=self.size[0,0]
        self.size[0,0]=3-self.size[1,1]
        self.size[1,1]=self.size[0,1]
        self.size[0,1]=3-self.size[1,0]
        self.size[1,0]=mem
        self.tile=next

    def display(self):
        for j in range(0,4):
            for i in range(0,4):
                print(self.tile[i,j],end=' ')
            print(" ")

    def fall(self,speed,tiles_map):
        
        if(speed=='fast'):
            for i in range(0,3):
                if(self.check_hit()):
                    self.pos[1]+=1
        elif(speed=='normal'):
            if(self.check_hit()):
                    self.pos[1]+=1


class Game:
    def __init__(self,name):
        self.board = np.zeros((10,20)) 
        self.screen = pg.display.set_mode((width, height))
        self.name=name
        self.score=0
        self.bestscore=0
        self.tuile=Tiles()
        self.falling=False

    def display(self):
        map=self.tuile.tile
        for j in range(0,4):
            for i in range(0,4):
                if (map[i,j]==1):
                    self.block(((self.tuile.pos[0]+i)*block+200,(self.tuile.pos[1]+j)*block+300,block,block),self.tuile.color)
        #self.display_board()
        for j in range(0,20):
            for i in range(0,10):
                if(self.board[i,j]!=0):
                    self.block((i*block+200,j*block+300,block,block),self.board[i,j])

    def display_board(self):
        for j in range(0,20):
            for i in range(0,10):
                print(self.board[i,j],end=' ')
            print(" ")                


    def startGame(self):
        #GameLoop
        running = True
        while running:
            pg.time.delay(100)
            speed='normal'
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        self.move('right')
                    if event.key == pg.K_LEFT:
                        self.move('left')
                    if event.key == pg.K_UP:
                        if(self.check_rotate()):
                            self.tuile.rotate(True)
            keys=pg.key.get_pressed()
            if (keys[K_DOWN]):
                self.falling=0
            if(self.falling==0):
                if(self.fall(speed)):
                    running=False
                    self.gameover()
                    
                    pg.display.update()
                    end=True
                    while end:
                        for event in pg.event.get():
                            if event.type == pg.KEYDOWN:
                                if event.key == pg.K_RETURN :
                                    end=False
                            if event.type == pg.QUIT:
                                end=False
                                quit()
                self.falling=3
            else:
                self.falling-=1
            self.background()
            self.display()
            pg.display.update()
    
    def score_change(self,lines):
        if (lines==1):
            self.score+=40
        if (lines==2):
            self.score+=100
        if (lines==3):
            self.score+=300
        if (lines==4):
            self.score+=1200
        
    
    def block(self,coor,color):
        if (color==1):
            color=(0,127,255)
        if (color==2):
            color=green
        if (color==3):
            color=(255,255,0)
        if (color==4):
            color=red
        if (color==5):
            color=(255,180,0)
        if (color==6):
            color=blue
        if (color==7):
            color=(127,0,255)
        stroke=8
        pg.draw.polygon(self.screen,color_darker(color,0.7),((coor[0],coor[1]),(coor[0]+coor[2]/2,coor[1]+coor[3]/2),(coor[0]+coor[2],coor[1])))
        pg.draw.polygon(self.screen,color_darker(color,0.8),((coor[0],coor[1]+coor[2]),(coor[0]+coor[2]/2,coor[1]+coor[3]/2),(coor[0],coor[1])))
        pg.draw.polygon(self.screen,color_darker(color,0.5),((coor[0],coor[1]+coor[2]),(coor[0]+coor[2]/2,coor[1]+coor[3]/2),(coor[0]+coor[2],coor[1]+coor[3])))
        pg.draw.polygon(self.screen,color_darker(color,0.6),((coor[0]+coor[2],coor[1]),(coor[0]+coor[2]/2,coor[1]+coor[3]/2),(coor[0]+coor[2],coor[1]+coor[3])))
        
        pg.draw.rect(self.screen,color,(coor[0]+stroke,coor[1]+stroke,coor[2]-(2*stroke),coor[3]-(2*stroke)))

    def square(self,coor,stroke):
        pg.draw.rect(self.screen,gamecolor,(coor[0]-stroke,coor[1]-stroke,coor[2]+(2*stroke),coor[3]+(2*stroke)))
        pg.draw.rect(self.screen,back,(coor[0],coor[1],coor[2],coor[3]))

    def background(self):
        self.screen.fill(black)
        title="TETRIS"
        img = font.render(title,True, white)
        rect=img.get_rect()
        rect.center=(width/2,100)
        
        self.screen.blit(img,rect)
        score="SCORE: "+str(self.score)
        dis = font.render(score,True, white)
        rect=img.get_rect()
        rect.center=(width/2,250)

        self.screen.blit(dis,rect)
        self.square((100,300,FrameWidth,FrameHeight),3)
        self.square((200,300,utilWidth,utilHeight),3)

    
    def gameover(self):
        self.screen.fill(black)
        title="GAME OVER"
        img = font.render(title,True, white)
        rect=img.get_rect()
        rect.center=(width/2,500)
        
        self.screen.blit(img,rect)
        score="SCORE: "+str(self.score)
        dis = font.render(score,True, white)
        rect=img.get_rect()
        rect.center=(width/2,750)

        self.screen.blit(dis,rect)

    def fall(self,speed):  
        if(speed=='fast'):
            for i in range(0,3):
                if(self.check_fall()):
                    self.tuile.pos[1]+=1
                else:
                    return self.tile_fallen()
        elif(speed=='normal'):
            if(self.check_fall()):
                self.tuile.pos[1]+=1
            else:
                return self.tile_fallen()
        return False

    def move(self,direction):  
        if(direction=='right'):
            if(self.check_wall(direction)):
                self.tuile.pos[0]+=1

        elif(direction=='left'):
            if(self.check_wall(direction)):
                self.tuile.pos[0]-=1

        return False
                
    def tile_fallen(self):
        for j in range(0,4):
            for i in range(0,4):
                if(self.tuile.tile[i,j]==1):
                    pos=self.tuile.pos
                    self.board[i+pos[0],j+pos[1]]=self.tuile.type
        self.tuile=Tiles()
        nbline=self.check_line()
        self.score_change(nbline)
        if(self.check_fall()):
            return False
        
        return True

    def delete_line(self,line):
        for j in range(line,1,-1):
            for i in range(0,10):
                self.board[i,j]=self.board[i,j-1]


    def check_line(self):
        nbline=0
        for j in range(0,20):
            line=True
            for i in range(0,10):
                if(self.board[i,j]==0):
                    line=False
            if(line):
                nbline+=1
                self.delete_line(j)
        return nbline

    def check_rotate(self):
        next=np.arange(16).reshape(4,4)
        for j in range(0,4):
            for i in range(0,4):
                next[3-j,i]=self.tuile.tile[i,j]

        for j in range(0,4):
            for i in range(0,4):
                if(next[i,j]==1):
                    if(j+self.tuile.pos[1]>=20):
                        self.tuile.pos[1]=19-j
                        return True
                    if(i+self.tuile.pos[0]<0):
                        self.tuile.pos[0]=i
                        return True
                    if(i+self.tuile.pos[0]>=10):
                        self.tuile.pos[0]=9-i
                        return True
                    if(i+self.tuile.pos[0]>=0 and i+self.tuile.pos[0]<10  and j+self.tuile.pos[1]<20):
                        if(self.board[i+self.tuile.pos[0],j+self.tuile.pos[1]]!=0):
                            return False
                
        return True

    def check_fall(self):
        for j in range(0,4):
            for i in range(0,4):
                if(self.tuile.tile[i,j]==1):
                    if(j+1+self.tuile.pos[1]==20):
                        return False
                    if(self.board[i+self.tuile.pos[0],j+1+self.tuile.pos[1]]!=0):
                        return False
                
        return True

    def check_wall(self,direction):
        for j in range(0,4):
            for i in range(0,4):
                if(self.tuile.tile[i,j]==1):
                    if(direction=='right'):
                        if(i+1+self.tuile.pos[0]==10):
                            return False
                        if(self.board[i+1+self.tuile.pos[0],j+self.tuile.pos[1]]!=0):
                            return False
                    elif(direction=='left'):
                        if(i+self.tuile.pos[0]==0):
                            return False
                        if(self.board[i-1+self.tuile.pos[0],j+self.tuile.pos[1]]!=0):
                            return False
        return True

 
    

def color_darker(color,k):
    return (int(color[0]*k),int(color[1]*k),int(color[2]*k))
        

#score + make the press button more responsive


""" 10*block   20*block """
pg.init()
utilWidth=600
utilHeight=utilWidth*2
FrameWidth=200+utilWidth
FrameHeight=utilHeight
width=1000
height=1800
block=600/10
back=(12,34,56)
gamecolor=(98,198,255)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
black=(0,0,0)

font = pg.font.Font('freesansbold.ttf', 60)

while(True):
    G=Game("Tetris")
    G.startGame()

