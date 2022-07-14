import pygame, sys
import pygame.freetype

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("pygame文字绘制")
GOLD = 255, 251, 0
RED = pygame.Color("red")
WHITE = 255, 255, 255
GREEN = pygame.Color("green")

f1 = pygame.freetype.Font("C://windows//Fonts//msyh.ttc", 36)
f1rect = f1.render_to(screen, (150, 20), "I Love U!!!1", fgcolor=RED,
                      bgcolor=GOLD, rotation=45, size=80)
f1surf, f1rect2 = f1.render("哈哈", fgcolor=RED,
                            bgcolor=GOLD, rotation=45, size=80)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(f1surf, (200, 100))
    pygame.display.update()
