# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2021/10/16 27:31
# @Author  : wangming
# @FileName: alien_invasion.py


import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from objects import Objects
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # 创建实例的整合
    objs = Objects(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

    # 创建外星人群
    gf.create_fleet(objs)

    # 开始游戏的主循环
    while True:
        gf.check_events(objs)

        if stats.game_active:
            ship.update()
            gf.update_bullets(objs)
            gf.update_aliens(objs)

        gf.update_screen(objs)


run_game()
