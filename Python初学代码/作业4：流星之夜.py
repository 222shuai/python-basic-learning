import turtle
import random
#基本设置
turtle.screensize(1280,1080,"royal blue")
turtle.setup(0.9,0.8)
turtle.pensize(2)
#草地
for i in range(160):
    turtle.penup()
    turtle.goto(800,-270-i)
    turtle.pendown()
    turtle.setheading(156)
    turtle.pencolor("green")
    turtle.speed(500)
    turtle.circle(2000,100)
for j in range(145):
    turtle.penup()
    turtle.goto(-800,-259-j)
    turtle.pendown()
    turtle.setheading(0)
    turtle.pencolor("green")
    turtle.speed(200)
    turtle.forward(1600)
#利用随机数画星星
x=0
y=0
t=0
z=0
for i in range(60):
    if i<60:
        x=random.randint(-700,700)
        y=random.randint(200,300)
        t=random.randint(1,4)
        z=random.randint(7,15)
        if t==1:
            t="red"
        elif t==2:
            t="blue"
        elif t==3:
            t="yellow"
        elif t==4:
            t="orange"
        turtle.penup()
        turtle.goto(x,y)
        turtle.pendown()
        turtle.color(t,t)
        for _ in range(5):
            turtle.begin_fill()
            turtle.forward(z)
            turtle.right(144)
            turtle.end_fill()
        turtle.setheading (180+_)
        turtle.circle(2000,60)
#草地画星星
for i in range(100):
    if i<100:
        x=random.randint(-700,700)
        y=random.randint(-350,-220)
        t=random.randint(1,4)
        z=random.randint(7,15)
        if t==1:
            t="red"
        elif t==2:
            t="blue"
        elif t==3:
            t="yellow"
        elif t==4:
            t="orange"
        turtle.penup()
        turtle.goto(x,y)
        turtle.pendown()
        turtle.color(t,t)
        for _ in range(5):
            turtle.begin_fill()
            turtle.forward(z)
            turtle.right(144)
            turtle.end_fill()
#画笑脸
turtle.penup()
turtle.goto(200,-50)
turtle.pendown()
turtle.circle(50,360)
turtle.color('black','pink')
turtle.begin_fill()
turtle.circle(50,360)
turtle.end_fill()
turtle.color('black','black')
turtle.begin_fill()
turtle.penup()
turtle.goto(230,-50)
turtle.pendown()
turtle.circle(4,360)
turtle.penup()
turtle.goto(250,-50)
turtle.pendown()
turtle.circle(4,360)
turtle.end_fill()
turtle.penup()
turtle.goto(220,-85)
turtle.setheading(-30)
turtle.pendown()
turtle.circle(50,60)
turtle.hideturtle()
#写字
turtle.penup()
turtle.goto(150,0)
turtle.pendown()
turtle.color("red")
turtle.write("H a p p y!",font=('Arial', 40, 'normal'))
