import pygame
import sys
import pygame.freetype

pygame.init()
# vInfo = pygame.display.Info()  # 获取当前屏幕信息（current_w = 屏幕宽度，current_h = 屏幕高度）
screenSize = width, height = 1000, 600  # 窗口大小(可另设数字)
screenFlag = pygame.RESIZABLE  # | pygame.NOFRAME | pygame.FULLSCREEN
# screenFlag：屏幕显示设置(pygame.RESIZABLE:窗口大小可调|
# pygame.NOFRAME:窗口没有边界显示|
# pygame.FULLSCREEN:窗口全屏显示(均用|隔开))
speed = [1, 1]  # 速度变量数组
COLOR = 100, 225, 225  # 背景颜色
print(pygame.display.Info())  # 显示当前屏幕信息（current_w = 屏幕宽度，current_h = 屏幕高度）
screen = pygame.display.set_mode(screenSize, screenFlag)  # 游戏屏幕建立
print(pygame.display.Info())  # 显示当前屏幕信息，说明同上
pygame.display.set_caption("myPygame!!!")  # 窗口标题
icon = pygame.image.load("bbb.png")  # 窗口图标
pygame.display.set_icon(icon)  # 建立窗口图标
fps = 500  # 帧数fps大小设置
fclok = pygame.time.Clock()  # 定义帧数控制变量fclok
fclok.tick(fps)  # 帧数控制（每秒fps帧）
still = False  # 鼠标对应运行状态，见57行
bgcolor = pygame.Color(0)  # 定义背景色变量bgcolor("r,g,b")
# r:红色值；g:绿色值；b:蓝色值//"black"="0,0,0";"white"="255,255,255"

GOLD = 255, 251, 0
pos = [230, 160]
f1 = pygame.freetype.Font("C://windows//Fonts//msyh.ttc", 36)
f1rect = f1.render_to(screen, pos, "Love", fgcolor=GOLD, size=50)


def RGBChannel(a):  # 定义RGBChannel函数
    return 0 if a < 0 else (255 if a > 255 else int(a))


ball = pygame.image.load("aaa.gif")  # 游戏对象图标
ballrect = ball.get_rect()

while True:  # 执行模块

    for event in pygame.event.get():  # 事件判断
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:  # 自由拉伸屏幕尺寸实时更新
            screenSize = width, height = event.size[0], event.size[1]
            # event.size[0]，event.size[1]分别存实时的屏幕宽度和高度
            screen = pygame.display.set_mode(screenSize, screenFlag)
            print(pygame.display.Info())  # 显示当前屏幕信息，说明同上
        elif event.type == pygame.KEYDOWN:  # 键盘事件
            if event.key == pygame.K_LEFT:  # 方向左键
                speed[0] = speed[0] \
                    if speed[0] == 0 \
                    else (abs(speed[0] - 1) * int(speed[0] / speed[0]))
            elif event.key == pygame.K_RIGHT:  # 方向右键
                speed[0] = speed[0] + 1 \
                    if speed[0] > 0 \
                    else speed[0] - 1
            elif event.key == pygame.K_UP:  # 方向上键
                speed[1] = speed[1] + 1 \
                    if speed[1] > 0 \
                    else speed[1] - 1
            elif event.key == pygame.K_DOWN:  # 方向下键
                speed[1] = speed[1] \
                    if speed[1] == 0 \
                    else (abs(speed[1] - 1) * int(speed[1] / speed[1]))
            elif event.key == pygame.K_SPACE:  # 空格键暂停
                speed[0] = speed[1] = 0
            elif event.key == pygame.K_ESCAPE:
                sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下事件
            if event.button == 1:  # event.button代表按钮，1代表鼠标左键
                still = True
        elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标松开事件
            still = False
            if event.button == 1:
                ballrect = ballrect.move(event.pos[0] - ballrect.left, event.pos[1] - ballrect.top)
                # 执行小球对应鼠标移动命令
        elif event.type == pygame.MOUSEMOTION:  # 鼠标移动事件
            if event.buttons[0] == 1:
                ballrect = ballrect.move(event.pos[0] - ballrect.left, event.pos[1] - ballrect.top)

    if pygame.display.get_active() and not still:
        # 当窗口在系统中显示（屏幕绘制/非图标化）时返回True,否则返回False
        # 可以判断是否游戏窗口被最小化，从而做出相应响应
        ballrect = ballrect.move(speed[0], speed[1])  # 事件设置
    if pos[0] < 0 or pos[0] + f1rect.width > width:
        speed[0] = - speed[0]
        if width < ballrect.right < ballrect.right + speed[0]:
            speed[0] = - speed[0]
    if pos[1] < 0 or pos[1] + f1rect.height >height:
        speed[1] = - speed[1]
        if height < ballrect.bottom < ballrect.bottom + speed[1]:
            speed[1] = - speed[1]

    pos[0] = pos[0] + speed[0]
    pos[1] = pos[1] + speed[1]

    # bgcolor变量参数(r,g,b)分别赋值(0~255)
    bgcolor.r = RGBChannel(ballrect.left * 255 / width)
    bgcolor.g = RGBChannel(ballrect.top * 255 / height)
    bgcolor.b = RGBChannel(min(speed[0], speed[1]) * 255 / max(speed[0], speed[1], 1))

    screen.fill(bgcolor)  # 背景颜色填充(见12行COLOR 23行bgcolor)
    f1rect = f1.render_to(screen, pos, "Love", fgcolor=GOLD, size=50)
    screen.blit(ball, ballrect)  # 在主图层ball上绘制ballrect图层
    pygame.display.update()  # 仅对窗口变化部分进行更新（区别于flip）
    fclok.tick(fps)
