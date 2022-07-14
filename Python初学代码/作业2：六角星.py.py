import turtle
import time

turtle.screensize(800,700)
turtle.setup(700,600,300,175)
turtle.pensize(5)
turtle.color("red")
turtle.fillcolor("yellow")

turtle.begin_fill()

for _ in range(3):
    turtle.forward(200)
    turtle.right(120)

turtle.penup()
turtle.goto(0,-100)
turtle.pendown()
turtle.color("red")
turtle.fillcolor("yellow")
for _ in range(3):
    turtle.forward(200)
    turtle.left(120)
turtle.end_fill()
time.sleep(1.5)

turtle.penup()
turtle.goto(60,-75)
turtle.pendown()
turtle.color("blue")
turtle.write("Ok!",font=('Arial', 40, 'normal'))
time.sleep(1)
