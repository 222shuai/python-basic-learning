from turtle import *

import random


def draw(numOfLine,lenghth):#numOfLine代表边数，lenghth边长
    for i in range(numOfLine):
        forward(lenghth)
        right(180-180*(numOfLine-2)/numOfLine)

def runTurtle(numOfObj,angle,numofL,Len):#numOfObj形状个数，angle旋转角度
    for i in range(numOfObj):
        draw(numofL,Len)
        right(angle)

def main(num):
    screensize(800,600,'white')
    for i in range(num):
        turtleX=random.randint(-400,400)
        turtleY=random.randint(-300,300)
        penup()
        goto(turtleX,turtleY)
        pendown()
        
runTurtle(36,10,4,100*random.random())
