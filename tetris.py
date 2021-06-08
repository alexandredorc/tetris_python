import pygame as pg
import numpy as np
import sys
import random as rd

class Tiles:
    def __init__(self):
        type=rd.randint(1,7)
        self.tile=np.arange(16).reshape(4,4)
        self.tile.fill(0)
        self.pos=np.array([0,0])
        
        if (type==1):
            self.tile[0,2]=1
            self.tile[1,2]=1
            self.tile[2,2]=1
            self.tile[3,2]=1
            self.color=(0,127,255)
            self.size=np.array([[0,3],[2,2]])
        if (type==2):
            self.tile[1,1]=1
            self.tile[1,2]=1
            self.tile[2,2]=1
            self.tile[2,3]=1
            self.color=green
            self.size=np.array([[1,2],[1,3]])
        if (type==3):
            self.tile[1,1]=1
            self.tile[1,2]=1
            self.tile[2,1]=1
            self.tile[2,2]=1
            self.color=(255,255,0)
            self.size=np.array([[1,2],[1,2]])
        if (type==4):
            self.tile[2,1]=1
            self.tile[2,2]=1
            self.tile[1,2]=1
            self.tile[1,3]=1
            self.color=red
            self.size=np.array([[1,2],[1,3]])
        if (type==5):
            self.tile[1,1]=1
            self.tile[2,1]=1
            self.tile[2,2]=1
            self.tile[2,3]=1
            self.color=(255,180,0)
            self.size=np.array([[1,2],[1,3]])
        if (type==6):
            self.tile[2,1]=1
            self.tile[1,1]=1
            self.tile[1,2]=1
            self.tile[1,3]=1
            self.color=blue
            self.size=np.array([[1,2],[1,3]])
        if (type==7):
            self.tile[1,2]=1
            self.tile[2,2]=1
            self.tile[2,1]=1
            self.tile[3,2]=1
            self.color=(127,0,255)
            self.size=np.array([[1,3],[1,2]])
        print("type",type)
        nb=rd.randint(0,3)
        for i in range(0,nb):
            self.rotate(True)
        print(self.size[0,0])
        print(self.size[0,1])
        print(self.size[1,0])
        print(self.size[1,1])
        self.display()

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

class Game:
    def __init__(self,name):
        self.board = np.arange(200).reshape(10,20) 
        self.screen = pg.display.set_mode((width, height))
        self.name=name
        self.score=0
        self.bestscore=0
        self.tuile=Tiles()

    def display(self):
        map=self.tuile.tile
        for j in range(0,4):
            for i in range(0,4):
                if (map[i,j]==1):
                    pg.draw.rect(self.screen,self.tuile.color,((self.tuile.pos[0]+i)*block+200,(self.tuile.pos[1]+j)*block+300,block,block))                   

    def startGame(self):
        #GameLoop
        running = True
        while running:
            
            #self.tuile.rotate(True)

            #self.tuile.pos[1]+=1
            if (self.tuile.pos[1]>20):
                self.tuile=Tiles()
            self.background()
            self.display()
            pg.time.delay(200)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            pg.display.update()

    def square(self,coor,stroke):
        pg.draw.rect(self.screen,gamecolor,(coor[0]-stroke,coor[1]-stroke,coor[2]+(2*stroke),coor[3]+(2*stroke)))
        pg.draw.rect(self.screen,back,(coor[0],coor[1],coor[2],coor[3]))

    def background(self):
        self.screen.fill(black)
        self.square((100,300,FrameWidth,FrameHeight),3)
        self.square((200,300,utilWidth,utilHeight),3)


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

