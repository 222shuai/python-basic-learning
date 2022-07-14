import random
import sys
import time
import requests
import pygame
import threading
from pygame.locals import *

pygame.init()
pygame.display.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode([512, 768])


class Resource:
    FPS = 60  # 帧率
    nowtime_zdjb = 0  # 子弹加倍计时器
    nowtime_xx = 0  # 吸血计时器
    nowtime_hd = 0  # 护盾计时器
    clock = pygame.time.Clock()  # 时钟
    pre = False
    run = False
    rel = False
    th1 = False
    version = 1.3
    shuxing = open('./data/shuxing.txt', 'r', encoding='utf-8')
    shuxingr = list(map(lambda x: x.replace('\n', ''), shuxing.readlines()))
    shuxing.close()
    coin = shuxingr[0]
    blood_my = 100
    harm_bullet_my = 4
    image_back = [
        './image/bg1.png',
        './image/bg2.png',
        './image/bg3.png',
        './image/bg4.png',
        './image/bg5.png'
    ]
    image_my = [
        './image/my1.png'
    ]
    bullet_my = pygame.image.load('./image/bullet_my/bullet.png')
    bm_cut = [
        bullet_my.subsurface((84, 91, 16, 75)),
        bullet_my.subsurface((119, 338, 26, 75)),
        bullet_my.subsurface((119, 338, 26, 75)),
        bullet_my.subsurface((119, 338, 26, 75)),
        bullet_my.subsurface((226, 55, 30, 59)),
        bullet_my.subsurface((226, 55, 30, 59)),
        bullet_my.subsurface((226, 55, 30, 59)),
        bullet_my.subsurface((226, 55, 30, 59)),
        bullet_my.subsurface((226, 55, 30, 59)),
        bullet_my.subsurface((226, 55, 30, 59)),
    ]
    bes_cut = [
        bullet_my.subsurface((272, 182, 25, 25)),
    ]
    bm_bomb = [
        './image/bm_bomb/bomb.png'
    ]
    enemy_small = pygame.USEREVENT
    pygame.time.set_timer(enemy_small, 1000)
    enemy_small_image_list = [
        './image/enemy_small.png',
    ]
    enemy_big = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_big, 20000)
    enemy_big_image_list = [
        './image/enemy_big.png'
    ]
    fire = pygame.USEREVENT + 2
    pygame.time.set_timer(fire, 100)
    add_bullet_image_list = [
        './image/add_bullet.png',
    ]
    # tib(take in blood)
    tib_image_list = [
        './image/takeinblood.png',
    ]
    # hd(护盾)
    hd_image_list = [
        './image/defend.png',
        [
            './image/defence/defence1.png',
            './image/defence/defence2.png',
            './image/defence/defence3.png',
            './image/defence/defence4.png',
        ],
    ]
    bullet_my_list = []  # 我的子弹
    bm_rect = []
    es_list = []  # 敌方小飞机
    es_rect = []
    eb_list = []  # 敌方大飞机
    eb_rect = []
    bes_list = []  # 敌方小飞机子弹
    bes_rect = []
    beb_list = [[], []]  # 敌方大飞机子弹
    beb_rect = [[], []]
    bm_two_list = [[], []]  # 我的子弹2
    bm_two_rect = [[], []]
    adbm_list = []  # 添加子弹
    adbm_rect = []
    tib_list = []  # 添加吸血
    tib_rect = []
    hd_list = []  # 添加护盾
    hd_rect = []
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (135, 206, 250)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    ORANGE = (255, 128, 0)
    GREY = (128, 128, 128)
    blood_enemy_small = 50
    blood_enemy_big = 160
    myhero_rect = Rect(200, 600, 110, 109)
    bomb = pygame.image.load('./image/bomb.png')
    my_bomb = [
        pygame.image.load(image_my[0]),
        bomb.subsurface((315, 0, 155, 155)),
        bomb.subsurface((159, 318, 155, 155)),
        bomb.subsurface((162, 158, 155, 155)),
        bomb.subsurface((164, 1, 155, 155)),
        bomb.subsurface((2, 316, 155, 155)),
        bomb.subsurface((2, 160, 155, 155)),
        bomb.subsurface((3, 3, 155, 155)),
    ]
    eb_bomb = [
        pygame.image.load(enemy_big_image_list[0]),
        bomb.subsurface((315, 0, 155, 155)),
        bomb.subsurface((159, 318, 155, 155)),
        bomb.subsurface((162, 158, 155, 155)),
        bomb.subsurface((164, 1, 155, 155)),
        bomb.subsurface((2, 316, 155, 155)),
        bomb.subsurface((2, 160, 155, 155)),
        bomb.subsurface((3, 3, 155, 155)),
    ]
    es_bomb = [
        pygame.image.load(enemy_small_image_list[0]),
        bomb.subsurface((721, 390, 50, 50)),
        bomb.subsurface((701, 450, 50, 50)),
        bomb.subsurface((673, 398, 50, 50)),
        bomb.subsurface((701, 450, 50, 50)),
        bomb.subsurface((605, 398, 50, 50)),
        bomb.subsurface((701, 450, 50, 50)),
        bomb.subsurface((651, 459, 50, 50)),
        bomb.subsurface((701, 450, 50, 50)),
        bomb.subsurface((602, 462, 50, 50)),
        bomb.subsurface((721, 390, 50, 50)),
    ]
    bullet_index = 0
    tib_index = 0
    hd_index = 0
    # living back music(lbm)
    lbm = pygame.mixer.Sound('./music/dt_music.wav')
    # ing back music(ibm)
    ibm = pygame.mixer.Sound('./music/ing_music.wav')
    # biu back music(bbm)
    bbm = pygame.mixer.Sound('./music/biu.wav')
    # bomb small-big-my back music(bsbmbm)
    bsbmbm = pygame.mixer.Sound('./music/bomb.wav')
    # get tool back music(gtbm)
    gtbm = pygame.mixer.Sound('./music/tool_music.wav')
    # button music(btm)
    btm = pygame.mixer.Sound('./music/button_music.wav')


class background():
    def __init__(self):
        self.bgspeed = 1
        self.y1 = 0
        self.y2 = -768
        self.back = pygame.image.load(
            Resource.image_back[random.randint(0, 4)])

    def show_bg1(self):
        self.y1 += self.bgspeed
        if self.y1 >= 768:
            self.y1 = -768
        background.display(self.y1)

    def show_bg2(self):
        self.y2 += self.bgspeed
        if self.y2 >= 768:
            self.y2 = -768
        background.display(self.y2)

    def display(self, Y):
        screen.blit(self.back, [0, Y])


class myhero():
    def __init__(self):
        self.coin = 0
        self.index = 0
        self.bloodmax = float(Resource.blood_my)
        self.blood = self.bloodmax
        self.coins = 0
        self.def_index = 0
        self.zs = pygame.font.Font('./font/jtz.ttf', 13)  # 道具注释
        self.dj = pygame.font.Font('./font/jtz.ttf', 13)  # 道具记录

    def display(self):
        self.image = Resource.my_bomb[self.index]
        if self.blood <= 0:
            if self.index < len(Resource.my_bomb) - 1:
                if random.randint(0, 5) == 0:
                    self.index += 1
        if self.index < len(Resource.my_bomb) - 1:
            screen.blit(
                self.image, [Resource.myhero_rect.x, Resource.myhero_rect.y])
        if self.index >= len(Resource.my_bomb) - 1:
            Resource.bsbmbm.play()
            if random.randint(0, 10) == 0:
                Resource.ibm.stop()
                relax()
        if Resource.hd_index != 0:
            hd_image = pygame.image.load(
                Resource.hd_image_list[1][self.def_index])
            screen.blit(
                hd_image, [Resource.myhero_rect.x - 19, Resource.myhero_rect.y - 19])
        if self.def_index < 2:
            self.def_index += 1
        else:
            self.def_index = 0

    def moveUp(self):
        if Resource.myhero_rect.y >= -50:
            Resource.myhero_rect.y -= 6

    def moveDown(self):
        if Resource.myhero_rect.y <= 728:
            Resource.myhero_rect.y += 6

    def moveLeft(self):
        if Resource.myhero_rect.x >= -50:
            Resource.myhero_rect.x -= 6

    def moveRight(self):
        if Resource.myhero_rect.x <= 460:
            Resource.myhero_rect.x += 6

    def blood_my(self):
        if self.blood > 0:
            self.index = 0
            pygame.draw.rect(screen, Resource.BLACK,
                             (Resource.myhero_rect.x, Resource.myhero_rect.y - 10, 110, 4))
            pygame.draw.rect(screen, Resource.GREEN, (Resource.myhero_rect.x + 1, Resource.myhero_rect.y + 0.5 - 10,
                                                      110 * 0.99 * float(self.blood) / float(self.bloodmax), 4 * 0.95))
            if Resource.bullet_index > 0:
                if 0 < Resource.bullet_index <= 3:
                    xb = ' x2'
                else:
                    xb = ' x3 max'
                ctime1 = 10 - time.time() + Resource.nowtime_zdjb  # 时间差
                djmc1 = self.dj.render(str(
                    Resource.bullet_index) + ' ' * 55 + str(int(ctime1)) + 's', True, Resource.RED)  # 时间+等级
                djzs1 = self.zs.render('子弹加倍' + xb, True, Resource.RED)  # 道具名
                uplines1 = 0  # 进度条向上偏移的距离
                last1 = 10  # 道具持续时间
                djtxs(ctime1, djmc1, djzs1, uplines1, last1)  # 调用显示道具条
            if Resource.tib_index > 0:
                ctime2 = 8 - time.time() + Resource.nowtime_xx
                djmc2 = self.dj.render(
                    str(Resource.tib_index) + ' ' * 55 + str(int(ctime2)) + 's', True, Resource.RED)
                djzs2 = self.zs.render('吸血', True, Resource.RED)
                uplines2 = 0
                last2 = 8
                if Resource.bullet_index != 0:
                    uplines2 += 1
                djtxs(ctime2, djmc2, djzs2, uplines2, last2)
            if Resource.hd_index > 0:
                ctime3 = 6 - time.time() + Resource.nowtime_hd
                djmc3 = self.dj.render(
                    str(Resource.hd_index) + ' ' * 55 + str(int(ctime3)) + 's', True, Resource.RED)
                djzs3 = self.zs.render('护盾', True, Resource.RED)
                uplines3 = 0
                last3 = 6
                if Resource.bullet_index != 0:
                    uplines3 += 1
                if Resource.tib_index != 0:
                    uplines3 += 1
                djtxs(ctime3, djmc3, djzs3, uplines3, last3)
        else:
            pass
        if self.blood > self.bloodmax:
            self.blood = self.bloodmax

    def show_coins(self):
        font = pygame.font.Font('./font/jtz.ttf', 20)
        fontr = font.render('得分：' + str(self.coins), True, Resource.YELLOW)
        screen.blit(fontr, [10, 10])

    def addcoins(self, adc):
        self.coins += adc

    def reduceblood(self, bnum):
        if Resource.hd_index == 0:
            self.blood -= bnum

    def addblood(self, num):
        if self.blood < self.bloodmax:
            self.blood += num

    def fire_my(self):
        Resource.bbm.play()
        if Resource.bullet_index == 0:
            new_bm = bullet()
            new_bmxy = Rect(Resource.myhero_rect.x + 48,
                            Resource.myhero_rect.y - 45, 16, 75)
            Resource.bullet_my_list.append(new_bm)
            Resource.bm_rect.append(new_bmxy)
        elif 0 < Resource.bullet_index <= 3:
            new_bm1 = bullet()
            new_bm1xy = Rect(Resource.myhero_rect.x + 16,
                             Resource.myhero_rect.y + 6, 26, 75)
            Resource.bm_two_list[0].append(new_bm1)
            Resource.bm_two_rect[0].append(new_bm1xy)
            new_bm2 = bullet()
            new_bm2xy = Rect(Resource.myhero_rect.x + 71,
                             Resource.myhero_rect.y + 6, 26, 75)
            Resource.bm_two_list[1].append(new_bm2)
            Resource.bm_two_rect[1].append(new_bm2xy)
        elif 3 < Resource.bullet_index <= 5:
            new_bm = bullet()
            new_bmxy = Rect(Resource.myhero_rect.x + 40,
                            Resource.myhero_rect.y - 40, 30, 59)
            Resource.bullet_my_list.append(new_bm)
            Resource.bm_rect.append(new_bmxy)
            new_bm1 = bullet()
            new_bm1xy = Rect(Resource.myhero_rect.x + 16,
                             Resource.myhero_rect.y + 6, 30, 59)
            Resource.bm_two_list[0].append(new_bm1)
            Resource.bm_two_rect[0].append(new_bm1xy)
            new_bm2 = bullet()
            new_bm2xy = Rect(Resource.myhero_rect.x + 65,
                             Resource.myhero_rect.y + 6, 30, 59)
            Resource.bm_two_list[1].append(new_bm2)
            Resource.bm_two_rect[1].append(new_bm2xy)

    def add_es(self):
        new_es = enemy_small()
        new_esxy = Rect(random.randint(0, 460),
                        random.randint(-90, -50), 55, 45)
        Resource.es_list.append(new_es)
        Resource.es_rect.append(new_esxy)

    def add_eb(self):
        new_eb = enemy_big()
        new_ebxy = Rect(random.randint(0, 402),
                        random.randint(-140, -110), 110, 90)
        Resource.eb_list.append(new_eb)
        Resource.eb_rect.append(new_ebxy)

    def add_bullet(self):
        suijinum = random.randint(0, 1500)
        if suijinum <= 1:
            new_adbm = ad_bm()
            new_adbmxy = Rect(random.randint(0, 480),
                              random.randint(-100, -79), 35, 40)
            Resource.adbm_list.append(new_adbm)
            Resource.adbm_rect.append(new_adbmxy)
        elif suijinum == 2:
            new_tib = t_i_b()
            new_tibxy = Rect(random.randint(0, 480),
                             random.randint(-100, -79), 35, 46)
            Resource.tib_list.append(new_tib)
            Resource.tib_rect.append(new_tibxy)
        elif suijinum == 3:
            new_hd = h_d()
            new_hdxy = Rect(random.randint(0, 480),
                            random.randint(-100, -79), 35, 48)
            Resource.hd_list.append(new_hd)
            Resource.hd_rect.append(new_hdxy)


def bianli():
    for es in Resource.es_list:  # 遍历敌方小飞机列表
        es.movees()
        es.show_esblood()
        es.fire_es()
        es.showes()
    for eb in Resource.eb_list:  # 遍历敌方大飞机列表
        eb.moveeb()
        eb.show_ebblood()
        eb.fire_eb()
        eb.showeb()
    for bm in Resource.bullet_my_list:  # 遍历我方子弹一号列表
        bm.move_bm_one()
        bm.show_bm_one()
    for bm_so in Resource.bm_two_list[0]:  # 遍历我方子弹二号列表1
        bm_so.move_bm_two0()
        bm_so.show_bm_two0()
    for bm_st in Resource.bm_two_list[1]:  # 遍历我方子弹二号列表2
        bm_st.move_bm_two1()
        bm_st.show_bm_two1()
    for bes in Resource.bes_list:  # 遍历敌方小飞机子弹列表
        bes.movebes()
        bes.showbes()
    for beb in Resource.beb_list[0]:  # 遍历敌方大飞机子弹1列表
        beb.movebeb0()
        beb.showbeb0()
    for beb in Resource.beb_list[1]:  # 遍历敌方大飞机子弹2列表
        beb.movebeb1()
        beb.showbeb1()
    for jzd in Resource.adbm_list:  # 遍历添加子弹列表
        jzd.move_adbm()
        jzd.show_adbm()
    for jxx in Resource.tib_list:  # 遍历添加吸血列表
        jxx.move_tib()
        jxx.show_tib()
    for jhd in Resource.hd_list:  # 遍历添加护盾列表
        jhd.move_hd()
        jhd.show_hd()
    for esb in Resource.es_rect:  # 我方一号子弹和敌方小飞机碰撞检测
        for bmb in Resource.bm_rect:
            if esb.colliderect(bmb):
                try:
                    Resource.es_list[Resource.es_rect.index(
                        esb)].reduce_es()
                    Resource.bullet_my_list[Resource.bm_rect.index(
                        bmb)].reduce_bm_one(bmb)
                except:
                    pass
    for eme in Resource.es_rect:  # 我方飞机和敌方小飞机碰撞检测
        if eme.colliderect(Resource.myhero_rect):
            try:
                if myhero.index < len(Resource.my_bomb) - 1:
                    Resource.es_list[Resource.es_rect.index(eme)].kill_es()
            except:
                pass
    for ebm in Resource.eb_rect:  # 我方飞机和敌方大飞机碰撞检测
        if ebm.colliderect(Resource.myhero_rect):
            try:
                if myhero.index < len(Resource.my_bomb) - 1:
                    Resource.eb_list[Resource.eb_rect.index(ebm)].kill_eb()
            except:
                pass
    for ebb in Resource.eb_rect:  # 我方一号子弹与敌方大飞机碰撞检测
        for bmm in Resource.bm_rect:
            if ebb.colliderect(bmm):
                try:
                    Resource.eb_list[Resource.eb_rect.index(
                        ebb)].reduce_eb()
                    Resource.bullet_my_list[Resource.bm_rect.index(
                        bmm)].reduce_bm_one(bmm)
                except:
                    pass
    for besr in Resource.bes_rect:  # 敌方小飞机子弹与我方飞机碰撞监测
        if besr.colliderect(Resource.myhero_rect):
            try:
                if myhero.index < len(Resource.my_bomb) - 1:
                    Resource.bes_list[Resource.bes_rect.index(
                        besr)].reduce_bes()
                    myhero.reduceblood(random.randint(4, 6))
            except:
                pass
    for bebr1 in Resource.beb_rect[0]:  # 敌方大飞机子弹1与我方飞机碰撞监测
        if bebr1.colliderect(Resource.myhero_rect):
            try:
                if myhero.index < len(Resource.my_bomb) - 1:
                    Resource.beb_list[0][Resource.beb_rect[0].index(
                        bebr1)].reduce_beb0(bebr1)
                    myhero.reduceblood(random.randint(3, 5))
            except:
                pass
    for bebr2 in Resource.beb_rect[1]:  # 敌方大飞机子弹2与我方飞机碰撞监测
        if bebr2.colliderect(Resource.myhero_rect):
            try:
                if myhero.index < len(Resource.my_bomb) - 1:
                    Resource.beb_list[1][Resource.beb_rect[1].index(
                        bebr2)].reduce_beb1(bebr2)
                    myhero.reduceblood(random.randint(3, 5))
            except:
                pass
    for bm_sor in Resource.bm_two_rect[0]:  # 我方二号子弹1与敌方小飞机碰撞检测
        for esb in Resource.es_rect:
            if bm_sor.colliderect(esb):
                try:
                    Resource.es_list[Resource.es_rect.index(
                        esb)].reduce_es()
                    Resource.bm_two_list[0][Resource.bm_two_rect[0].index(
                        bm_sor)].remove_bm_two0(bm_sor)
                except:
                    pass
    for bm_str in Resource.bm_two_rect[1]:  # 我方二号子弹2与敌方小飞机碰撞检测
        for esb in Resource.es_rect:
            if bm_str.colliderect(esb):
                try:
                    Resource.es_list[Resource.es_rect.index(
                        esb)].reduce_es()
                    Resource.bm_two_list[1][Resource.bm_two_rect[1].index(
                        bm_str)].remove_bm_two1(bm_str)
                except:
                    pass
    for bm_sor in Resource.bm_two_rect[0]:  # 我方二号子弹1与敌方大飞机碰撞检测
        for ebb in Resource.eb_rect:
            if bm_sor.colliderect(ebb):
                try:
                    Resource.eb_list[Resource.eb_rect.index(
                        ebb)].reduce_eb()
                    Resource.bm_two_list[0][Resource.bm_two_rect[0].index(
                        bm_sor)].remove_bm_two0(bm_sor)
                except:
                    pass
    for bm_str in Resource.bm_two_rect[1]:  # 我方二号子弹2与敌方大飞机碰撞检测
        for ebb in Resource.eb_rect:
            if bm_str.colliderect(ebb):
                try:
                    Resource.eb_list[Resource.eb_rect.index(
                        ebb)].reduce_eb()
                    Resource.bm_two_list[1][Resource.bm_two_rect[1].index(
                        bm_str)].remove_bm_two1(bm_str)
                except:
                    pass
    for adbm in Resource.adbm_rect:  # 我方飞机和增加子弹的碰撞检测
        if adbm.colliderect(Resource.myhero_rect):
            try:
                Resource.adbm_list[Resource.adbm_rect.index(adbm)].kill_adbm()
            except:
                pass
    for tib in Resource.tib_rect:  # 我方飞机和增加吸血的碰撞检测
        if tib.colliderect(Resource.myhero_rect):
            try:
                Resource.tib_list[Resource.tib_rect.index(tib)].kill_tib()
            except:
                pass
    for hd in Resource.hd_rect:  # 我方飞机和增加护盾的碰撞检测
        if hd.colliderect(Resource.myhero_rect):
            try:
                Resource.hd_list[Resource.hd_rect.index(hd)].kill_hd()
            except:
                pass


def oppositetime():
    if time.time() - Resource.nowtime_zdjb >= 8:
        Resource.nowtime_zdjb = time.time()
        if Resource.bullet_index > 0:
            Resource.bullet_index -= 1
    if time.time() - Resource.nowtime_xx >= 8:
        Resource.nowtime_xx = time.time()
        if Resource.tib_index > 0:
            Resource.tib_index -= 1
    if time.time() - Resource.nowtime_hd >= 6:
        Resource.nowtime_hd = time.time()
        if Resource.hd_index > 0:
            Resource.hd_index -= 1


def djtxs(ctime, djmc, djzs, uplines, last):  # 道具条显示
    pygame.draw.rect(screen, Resource.BLACK,
                     (Resource.myhero_rect.x, Resource.myhero_rect.y - 30 - uplines * 20, 110, 2))
    pygame.draw.rect(screen, Resource.BLUE,
                     (Resource.myhero_rect.x + 1, Resource.myhero_rect.y + 0.5 - 30 - uplines * 20,
                      110 * 0.99 * ctime / last, 2 * 0.95))
    pygame.draw.circle(screen, Resource.BLACK, [
        Resource.myhero_rect.x - 1, Resource.myhero_rect.y - 31 - uplines * 20], 9)
    screen.blit(djmc, [Resource.myhero_rect.x - 4,
                       Resource.myhero_rect.y - uplines * 20 - 40])
    screen.blit(djzs, [Resource.myhero_rect.x + 6,
                       Resource.myhero_rect.y - uplines * 20 - 45])


class enemy_small():
    def __init__(self):
        self.blood = Resource.blood_enemy_small
        self.index = 0
        self.yspeed = 2
        self.xspeed = 0

    def movees(self):
        Resource.es_rect[Resource.es_list.index(self)].y += self.yspeed
        Resource.es_rect[Resource.es_list.index(
            self)].x += self.xspeed
        if self.blood > 0:
            self.xspeed += random.randint(-1, 1) * 0.1
            self.yspeed += random.randint(-1, 1) * 0.1
        try:
            if Resource.es_rect[Resource.es_list.index(self)].y > 768:
                del Resource.es_list[0]
                del Resource.es_rect[0]
            if Resource.es_rect[Resource.es_list.index(self)].y < -100:
                self.yspeed *= -1
            if Resource.es_rect[Resource.es_list.index(self)].x <= -55 or Resource.es_rect[
                Resource.es_list.index(self)].x >= 512:
                self.xspeed *= -1
        except:
            pass

    def showes(self):
        self.esimage = Resource.es_bomb[self.index]
        if self.blood <= 0:
            self.yspeed = 0
            self.xspeed = 0
            if self.index < len(Resource.es_bomb) - 1:
                if random.randint(0, 1) == 0:
                    self.index += 1
        try:
            screen.blit(self.esimage, [Resource.es_rect[Resource.es_list.index(
                self)].x, Resource.es_rect[Resource.es_list.index(self)].y])
        except:
            pass
        if self.index >= len(Resource.es_bomb) - 1:
            del Resource.es_rect[Resource.es_list.index(self)]
            del Resource.es_list[Resource.es_list.index(self)]
            Resource.bsbmbm.play()
            myhero.addcoins(random.randint(1, 5))

    def show_esblood(self):
        if self.blood > 0:
            try:
                pygame.draw.rect(screen, Resource.BLACK,
                                 (Resource.es_rect[Resource.es_list.index(self)].x - 4,
                                  Resource.es_rect[Resource.es_list.index(self)].y - 2, 60, 3))
                pygame.draw.rect(screen, Resource.RED, (Resource.es_rect[Resource.es_list.index(self)].x - 3,
                                                        Resource.es_rect[Resource.es_list.index(self)].y - 1.5,
                                                        60 * 0.99 * self.blood / 50, 3 * 0.95))
            except:
                pass

    def reduce_es(self):
        self.blood -= float(Resource.harm_bullet_my)

    def kill_es(self):
        self.blood = 0
        if self.yspeed != 0:
            myhero.reduceblood(random.randint(10, 20))

    def fire_es(self):
        if random.randint(0, 1000) <= 5:
            try:
                new_bes = bullet_es()
                new_besxy = Rect(Resource.es_rect[Resource.es_list.index(self)].x + 15,
                                 Resource.es_rect[Resource.es_list.index(self)].y + 38, 25, 25)
                Resource.bes_list.append(new_bes)
                Resource.bes_rect.append(new_besxy)
            except:
                pass


class enemy_big():
    def __init__(self):
        self.blood = Resource.blood_enemy_big
        self.index = 0
        self.xspeed = 0
        self.yspeed = 2

    def moveeb(self):
        try:
            Resource.eb_rect[Resource.eb_list.index(self)].x += self.xspeed
            Resource.eb_rect[Resource.eb_list.index(self)].y += self.yspeed
            if self.blood > 0:
                self.xspeed += random.randint(-1, 1) * 0.1
                self.yspeed += random.randint(-1, 1) * 0.1
            if Resource.eb_rect[Resource.eb_list.index(self)].y > 770:
                del Resource.eb_list[0]
                del Resource.eb_rect[0]
            if Resource.eb_rect[Resource.eb_list.index(self)].y < -150:
                self.yspeed *= -1
            if Resource.eb_rect[Resource.eb_list.index(self)].x <= -110 or Resource.eb_rect[
                Resource.eb_list.index(self)].x > 512:
                self.xspeed *= -1
        except:
            pass

    def showeb(self):
        self.ebimage = Resource.eb_bomb[self.index]
        if self.blood <= 0:
            self.xspeed, self.yspeed = 0, 0
            if self.index < len(Resource.eb_bomb) - 1:
                if random.randint(0, 3) == 0:
                    self.index += 1
        try:
            screen.blit(self.ebimage, [Resource.eb_rect[Resource.eb_list.index(
                self)].x, Resource.eb_rect[Resource.eb_list.index(self)].y])
        except:
            pass
        if self.index >= len(Resource.eb_bomb) - 1:
            del Resource.eb_rect[Resource.eb_list.index(self)]
            del Resource.eb_list[Resource.eb_list.index(self)]
            Resource.bsbmbm.play()
            myhero.addcoins(random.randint(50, 100))
            if myhero.blood > 0:
                myhero.addblood((myhero.bloodmax - myhero.blood)
                                * random.randint(5, 7) * 0.1)

    def show_ebblood(self):
        if self.blood > 0:
            try:
                pygame.draw.rect(screen, Resource.BLACK,
                                 (Resource.eb_rect[Resource.eb_list.index(self)].x - 10,
                                  Resource.eb_rect[Resource.eb_list.index(self)].y - 3, 130, 3))
                pygame.draw.rect(screen, Resource.RED, (Resource.eb_rect[Resource.eb_list.index(self)].x - 9,
                                                        Resource.eb_rect[Resource.eb_list.index(self)].y - 2.5,
                                                        130 * 0.99 * self.blood / 160, 3 * 0.95))
            except:
                pass

    def kill_eb(self):
        self.blood = 0
        if self.xspeed != 0:
            myhero.reduceblood(random.randint(40, 60))

    def reduce_eb(self):
        self.blood -= float(Resource.harm_bullet_my)

    def fire_eb(self):
        if random.randint(0, 150) <= 5:
            try:
                new_beb0 = bullet_eb()
                new_beb0xy = Rect(Resource.eb_rect[Resource.eb_list.index(self)].x + 17,
                                  Resource.eb_rect[Resource.eb_list.index(self)].y + 55, 20, 49)
                Resource.beb_list[0].append(new_beb0)
                Resource.beb_rect[0].append(new_beb0xy)
                new_beb1 = bullet_eb()
                new_beb1xy = Rect(Resource.eb_rect[Resource.eb_list.index(self)].x + 73,
                                  Resource.eb_rect[Resource.eb_list.index(self)].y + 55, 20, 49)
                Resource.beb_list[1].append(new_beb1)
                Resource.beb_rect[1].append(new_beb1xy)
            except:
                pass


class bullet():
    def __init__(self):
        self.image = Resource.bm_cut[Resource.bullet_index]

    def move_bm_one(self):
        Resource.bm_rect[Resource.bullet_my_list.index(self)].y -= 15
        if Resource.bm_rect[Resource.bullet_my_list.index(self)].y < -75:
            del Resource.bullet_my_list[0]
            del Resource.bm_rect[0]

    def show_bm_one(self):
        try:
            screen.blit(self.image, [Resource.bm_rect[Resource.bullet_my_list.index(
                self)].x, Resource.bm_rect[Resource.bullet_my_list.index(self)].y])
        except:
            pass

    def reduce_bm_one(self, bmb):
        bomb = pygame.image.load(Resource.bm_bomb[0])
        screen.blit(bomb, [Resource.bm_rect[Resource.bullet_my_list.index(
            self)].x, Resource.bm_rect[Resource.bullet_my_list.index(self)].y - 10])
        del Resource.bullet_my_list[Resource.bm_rect.index(bmb)]
        del Resource.bm_rect[Resource.bm_rect.index(bmb)]
        if Resource.tib_index != 0:
            myhero.addblood(Resource.harm_bullet_my *
                            random.randint(25, 40) * 0.01)

    def move_bm_two0(self):
        Resource.bm_two_rect[0][Resource.bm_two_list[0].index(self)].y -= 15
        if Resource.bm_two_rect[0][Resource.bm_two_list[0].index(self)].y <= -75:
            del Resource.bm_two_list[0][0]
            del Resource.bm_two_rect[0][0]

    def show_bm_two0(self):
        try:
            screen.blit(self.image, [Resource.bm_two_rect[0][Resource.bm_two_list[0].index(
                self)].x, Resource.bm_two_rect[0][Resource.bm_two_list[0].index(self)].y])
        except:
            pass

    def remove_bm_two0(self, bms):
        bomb = pygame.image.load(Resource.bm_bomb[0])
        screen.blit(bomb, [Resource.bm_two_rect[0][Resource.bm_two_list[0].index(
            self)].x + 5, Resource.bm_two_rect[0][Resource.bm_two_list[0].index(self)].y - 10])
        del Resource.bm_two_list[0][Resource.bm_two_rect[0].index(bms)]
        del Resource.bm_two_rect[0][Resource.bm_two_rect[0].index(bms)]
        if Resource.tib_index != 0:
            myhero.addblood(Resource.harm_bullet_my *
                            random.randint(25, 40) * 0.01)

    def move_bm_two1(self):
        Resource.bm_two_rect[1][Resource.bm_two_list[1].index(self)].y -= 15
        if Resource.bm_two_rect[1][Resource.bm_two_list[1].index(self)].y <= -75:
            del Resource.bm_two_list[1][0]
            del Resource.bm_two_rect[1][0]

    def show_bm_two1(self):
        try:
            screen.blit(self.image, [Resource.bm_two_rect[1][Resource.bm_two_list[1].index(
                self)].x, Resource.bm_two_rect[1][Resource.bm_two_list[1].index(self)].y])
        except:
            pass

    def remove_bm_two1(self, bms):
        bomb = pygame.image.load(Resource.bm_bomb[0])
        screen.blit(bomb, [Resource.bm_two_rect[1][Resource.bm_two_list[1].index(
            self)].x + 5, Resource.bm_two_rect[1][Resource.bm_two_list[1].index(self)].y - 10])
        del Resource.bm_two_list[1][Resource.bm_two_rect[1].index(bms)]
        del Resource.bm_two_rect[1][Resource.bm_two_rect[1].index(bms)]
        if Resource.tib_index != 0:
            myhero.addblood(Resource.harm_bullet_my *
                            random.randint(25, 40) * 0.01)


class bullet_eb():
    def __init__(self):
        self.image = pygame.image.load('./image/bullet_eb.png')

    def movebeb0(self):
        Resource.beb_rect[0][Resource.beb_list[0].index(self)].y += 10
        if Resource.beb_rect[0][Resource.beb_list[0].index(self)].y > 800:
            del Resource.beb_list[0][0]
            del Resource.beb_rect[0][0]

    def showbeb0(self):
        try:
            screen.blit(self.image, [Resource.beb_rect[0][Resource.beb_list[0].index(
                self)].x, Resource.beb_rect[0][Resource.beb_list[0].index(self)].y])
        except:
            pass

    def reduce_beb0(self, bebr):
        del Resource.beb_list[0][Resource.beb_rect[0].index(bebr)]
        del Resource.beb_rect[0][Resource.beb_rect[0].index(bebr)]

    def movebeb1(self):
        Resource.beb_rect[1][Resource.beb_list[1].index(self)].y += 10
        if Resource.beb_rect[1][Resource.beb_list[1].index(self)].y > 800:
            del Resource.beb_list[1][0]
            del Resource.beb_rect[1][0]

    def showbeb1(self):
        try:
            screen.blit(self.image, [Resource.beb_rect[1][Resource.beb_list[1].index(
                self)].x, Resource.beb_rect[1][Resource.beb_list[1].index(self)].y])
        except:
            pass

    def reduce_beb1(self, bebr):
        del Resource.beb_list[1][Resource.beb_rect[1].index(bebr)]
        del Resource.beb_rect[1][Resource.beb_rect[1].index(bebr)]


class bullet_es():
    def __init__(self):
        self.image = Resource.bes_cut[0]

    def movebes(self):
        Resource.bes_rect[Resource.bes_list.index(self)].y += 6
        if Resource.bes_rect[Resource.bes_list.index(self)].y > 800:
            del Resource.bes_list[0]
            del Resource.bes_rect[0]

    def showbes(self):
        try:
            screen.blit(self.image, [Resource.bes_rect[Resource.bes_list.index(
                self)].x, Resource.bes_rect[Resource.bes_list.index(self)].y])
        except:
            pass

    def reduce_bes(self):
        del Resource.bes_rect[Resource.bes_list.index(self)]
        del Resource.bes_list[Resource.bes_list.index(self)]


class ad_bm():
    def __init__(self):
        self.image = pygame.image.load(Resource.add_bullet_image_list[0])
        self.xspeed = 2.1

    def move_adbm(self):
        try:
            Resource.adbm_rect[Resource.adbm_list.index(self)].y += 2.1
            Resource.adbm_rect[Resource.adbm_list.index(self)].x += self.xspeed
            if Resource.adbm_rect[Resource.adbm_list.index(self)].y > 770:
                del Resource.adbm_list[0]
                del Resource.adbm_rect[0]
            if Resource.adbm_rect[Resource.adbm_list.index(self)].x <= 0 or Resource.adbm_rect[
                Resource.adbm_list.index(self)].x > 482:
                self.xspeed *= -1
        except:
            pass

    def show_adbm(self):
        try:
            screen.blit(self.image, [Resource.adbm_rect[Resource.adbm_list.index(
                self)].x, Resource.adbm_rect[Resource.adbm_list.index(self)].y])
        except:
            pass

    def kill_adbm(self):
        Resource.gtbm.play()
        del Resource.adbm_rect[Resource.adbm_list.index(self)]
        del Resource.adbm_list[Resource.adbm_list.index(self)]
        if Resource.bullet_index < 5:
            Resource.bullet_index += 1
        Resource.nowtime_zdjb = time.time()


class t_i_b():
    def __init__(self):
        self.image = pygame.image.load(Resource.tib_image_list[0])
        self.xspeed = 2.1

    def move_tib(self):
        try:
            Resource.tib_rect[Resource.tib_list.index(self)].y += 2.1
            Resource.tib_rect[Resource.tib_list.index(self)].x += self.xspeed
            if Resource.tib_rect[Resource.tib_list.index(self)].y > 770:
                del Resource.tib_list[0]
                del Resource.tib_rect[0]
            if Resource.tib_rect[Resource.tib_list.index(self)].x <= 0 or Resource.tib_rect[
                Resource.tib_list.index(self)].x > 482:
                self.xspeed *= -1
        except:
            pass

    def show_tib(self):
        try:
            screen.blit(self.image, [Resource.tib_rect[Resource.tib_list.index(
                self)].x, Resource.tib_rect[Resource.tib_list.index(self)].y])
        except:
            pass

    def kill_tib(self):
        Resource.gtbm.play()
        del Resource.tib_rect[Resource.tib_list.index(self)]
        del Resource.tib_list[Resource.tib_list.index(self)]
        if Resource.tib_index < 5:
            Resource.tib_index += 1
        Resource.nowtime_xx = time.time()


class h_d():
    def __init__(self):
        self.image = pygame.image.load(Resource.hd_image_list[0])
        self.xspeed = 2.1

    def move_hd(self):
        try:
            Resource.hd_rect[Resource.hd_list.index(self)].y += 2.1
            Resource.hd_rect[Resource.hd_list.index(self)].x += self.xspeed
            if Resource.hd_rect[Resource.hd_list.index(self)].y > 770:
                del Resource.hd_list[0]
                del Resource.hd_rect[0]
            if Resource.hd_rect[Resource.hd_list.index(self)].x <= 0 or Resource.hd_rect[
                Resource.hd_list.index(self)].x > 482:
                self.xspeed *= -1
        except:
            pass

    def show_hd(self):
        try:
            screen.blit(self.image, [Resource.hd_rect[Resource.hd_list.index(
                self)].x, Resource.hd_rect[Resource.hd_list.index(self)].y])
        except:
            pass

    def kill_hd(self):
        Resource.gtbm.play()
        del Resource.hd_rect[Resource.hd_list.index(self)]
        del Resource.hd_list[Resource.hd_list.index(self)]
        if Resource.hd_index < 5:
            Resource.hd_index += 1
        Resource.nowtime_hd = time.time()


class main:
    def __init__(self):
        pass

    def start(self):
        Resource.pre = False
        Resource.run = True
        Resource.ibm.play(-1)
        while Resource.run:
            background.show_bg1()
            background.show_bg2()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shuxing = open('./data/shuxing.txt', 'r', encoding='utf-8')
                    shuxingr = list(
                        map(lambda x: x.replace('\n', ''), shuxing.readlines()))
                    shuxing.close()
                    if myhero.coins >= float(shuxingr[0]):
                        with open('./data/shuxing.txt', 'w', encoding='utf-8') as later:
                            later.write(str(myhero.coins))
                            later.close()
                    Resource.myhero_rect.x, Resource.myhero_rect.y = 200, 600
                    myhero.coins = 0
                    myhero.index = 0
                    Resource.bullet_index = 0
                    myhero.blood = myhero.bloodmax
                    Resource.ibm.stop()
                    prepare()
                    run = False
                if event.type == Resource.enemy_small:
                    myhero.add_es()
                if event.type == Resource.enemy_big:
                    myhero.add_eb()
                if event.type == Resource.fire:
                    key_list1 = pygame.key.get_pressed()
                    if key_list1[pygame.K_SPACE] and myhero.blood > 0:
                        myhero.fire_my()
            key_list = pygame.key.get_pressed()
            if myhero.blood > 0:
                if key_list[pygame.K_UP] or key_list[pygame.K_w]:
                    myhero.moveUp()
                if key_list[pygame.K_DOWN] or key_list[pygame.K_s]:
                    myhero.moveDown()
                if key_list[pygame.K_LEFT] or key_list[pygame.K_a]:
                    myhero.moveLeft()
                if key_list[pygame.K_RIGHT] or key_list[pygame.K_d]:
                    myhero.moveRight()
            bianli()
            oppositetime()
            myhero.display()
            myhero.add_bullet()
            myhero.blood_my()
            myhero.show_coins()
            pygame.display.update()
            Resource.clock.tick(Resource.FPS)
            pygame.display.set_caption('飞机大战  FPS:' + str(int(Resource.clock.get_fps())))


def clear():
    Resource.bullet_index = 0
    Resource.tib_index = 0
    Resource.hd_index = 0
    Resource.bullet_my_list.clear()
    Resource.es_list.clear()
    Resource.es_rect.clear()
    Resource.bm_rect.clear()
    Resource.eb_list.clear()
    Resource.eb_rect.clear()
    Resource.bes_list.clear()
    Resource.bes_rect.clear()
    Resource.beb_list[0].clear()
    Resource.beb_rect[0].clear()
    Resource.beb_list[1].clear()
    Resource.beb_rect[1].clear()
    Resource.bm_two_list[0].clear()
    Resource.bm_two_rect[0].clear()
    Resource.bm_two_list[1].clear()
    Resource.bm_two_rect[1].clear()
    Resource.adbm_list.clear()
    Resource.adbm_rect.clear()
    Resource.tib_list.clear()
    Resource.tib_rect.clear()
    Resource.hd_list.clear()
    Resource.hd_rect.clear()


def relax():
    Resource.run = False
    Resource.rel = True
    Resource.myhero_rect.x = 200
    Resource.myhero_rect.y = 600
    myhero.bloodmax = float(Resource.blood_my)
    myhero.blood = myhero.bloodmax
    Resource.lbm.play(-1)
    shuxing = open('./data/shuxing.txt', 'r', encoding='utf-8')
    shuxingr = list(map(lambda x: x.replace('\n', ''), shuxing.readlines()))
    shuxing.close()
    if myhero.coins >= float(shuxingr[0]):
        with open('./data/shuxing.txt', 'w', encoding='utf-8') as later:
            later.write(str(myhero.coins))
            later.close()
    jiesuan = myhero.coins
    myhero.coins = 0
    myhero.index = 0
    clear()
    font = pygame.font.Font('./font/jtz.ttf', 20)
    fontr = font.render('得分：' + str(jiesuan), True, Resource.YELLOW)
    while Resource.rel:
        background.show_bg1()
        background.show_bg2()
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                myhero.coins = 0
                Resource.bullet_index = 0
                Resource.lbm.stop()
                prepare()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 226 <= mousex <= 286 and 512 <= mousey <= 572:
                    Resource.lbm.stop()
                    Resource.btm.play()
                    main.start()
                    Resource.rel = False
        if 226 <= mousex <= 286 and 512 <= mousey <= 572:
            screen.blit(pygame.image.load('./image/restartb.png'), [216, 502])
        else:
            screen.blit(pygame.image.load('./image/restarts.png'), [226, 512])
        screen.blit(pygame.image.load('./image/idead.png'), [80, 200])
        screen.blit(fontr, [220, 300])
        pygame.display.update()
        Resource.clock.tick(Resource.FPS)
        pygame.display.set_caption('飞机大战  FPS:' + str(int(Resource.clock.get_fps())))


def check_new_version():  # 检测更新（自行添加）
    Resource.th1 = True
    while Resource.th1:
        try:
            im1 = requests.get('').content
            print(im1)
        except:
            pass


def prepare():
    shuxing = open('./data/shuxing.txt', 'r', encoding='utf-8')
    shuxingr = list(map(lambda x: x.replace('\n', ''), shuxing.readlines()))
    shuxing.close()
    coin = shuxingr[0]
    font = pygame.font.Font('./font/jtz.ttf', 20)
    fontr = font.render('历史最高得分：' + str(coin), True, Resource.YELLOW)
    font1 = pygame.font.Font('./font/jtz.ttf', 10)
    font1r = font1.render('version:V' + str(Resource.version), True, Resource.WHITE)
    Resource.lbm.play(-1)
    clear()
    Resource.pre = True
    while Resource.pre:
        background.show_bg1()
        background.show_bg2()
        screen.blit(pygame.image.load('./image/fjdz.png'), [55, 180])
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Resource.lbm.stop()
                Resource.th1 = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 196 <= mousex <= 316 and 512 <= mousey <= 581:
                    Resource.btm.play()
                    Resource.lbm.stop()
                    main.start()
        if 196 <= mousex <= 316 and 512 <= mousey <= 581:
            screen.blit(pygame.image.load('./image/startb.png'), [181, 503.5])
        else:
            screen.blit(pygame.image.load('./image/starts.png'), [196, 512])
        screen.blit(fontr, (10, 10))
        screen.blit(font1r, (240, 756))
        pygame.display.update()
        Resource.clock.tick(Resource.FPS)
        pygame.display.set_caption('飞机大战  FPS:' + str(int(Resource.clock.get_fps())))


threads1 = threading.Thread(target=check_new_version)

if __name__ == '__main__':
    background = background()
    main = main()
    myhero = myhero()
    threads1.start()
    prepare()
