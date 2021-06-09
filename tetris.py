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
                    pg.draw.rect(self.screen,self.tuile.color,((self.tuile.pos[0]+i)*block+200,(self.tuile.pos[1]+j)*block+300,block,block))
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
            if(pg.key.get_pressed()[K_RIGHT]):
                self.move('right')
            if(pg.key.get_pressed()[K_LEFT]):
                self.move('left')
            if(pg.key.get_pressed()[K_UP]):
                if(self.check_rotate()):
                    self.tuile.rotate(True)
            if(pg.key.get_pressed()[K_DOWN]):
                speed='fast'
            else:
                speed='normal'
            if(self.falling):
                if(self.fall(speed)):
                    running=False
                    print("c'est perdu")
                self.falling=False
            else:
                self.falling=True           

            self.background()
            self.display()
            pg.time.delay(80)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                
            pg.display.update()
    
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
        pg.draw.rect(self.screen,color,(coor[0],coor[1],coor[2],coor[3]))

    def square(self,coor,stroke):
        pg.draw.rect(self.screen,gamecolor,(coor[0]-stroke,coor[1]-stroke,coor[2]+(2*stroke),coor[3]+(2*stroke)))
        pg.draw.rect(self.screen,back,(coor[0],coor[1],coor[2],coor[3]))

    def background(self):
        self.screen.fill(black)
        self.square((100,300,FrameWidth,FrameHeight),3)
        self.square((200,300,utilWidth,utilHeight),3)

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
        self.check_line()
        if(self.check_fall()):
            return False
        
        return True

    def delete_line(self,line):
        for j in range(line,1,-1):
            print(j)
            for i in range(0,10):
                self.board[i,j]=self.board[i,j-1]


    def check_line(self):
        for j in range(0,20):
            line=True
            for i in range(0,10):
                if(self.board[i,j]==0):
                    line=False
            if(line):
                self.delete_line(j)

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

        """for i in range(1, 10):
            pg.draw.line(screen,white,(1000*i//10,0),(1000*i//10,1000)
            pg.draw.line(screen,white,(0,1000*i//10),(1000,1000*i//10))
        for x in range(0,10):
            for y in range(0,10):
                if self.maps[y][x]!='':
                    pg.draw.rect(screen,red,(x*1000/10+1,y*1000//10+1,1000//10 -1,1000//10-1))
                    img = font.render(self.maps[y][x], True, blue)
                    rect=img.get_rect()
                    rect.center=(x*10,y*10)
                    print(rect)
                    screen.blit(img,rect)"""
           


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
font = pg.font.Font('freesansbold.ttf', 20)

G=Game("Tetris")
G.startGame()

