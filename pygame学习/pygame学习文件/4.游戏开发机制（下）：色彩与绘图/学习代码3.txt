# Unit PYG05: Pygame Font Draw
import pygame, sys
import pygame.freetype

pygame.init()
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption("Pygame文字绘制")
GOLD = 255, 251, 0

f1 = pygame.freetype.Font("C://Windows//Fonts//msyh.ttc", 36)
f1rect = f1.render_to(screen, (200,160), "世界和平", fgcolor=GOLD, size=50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()