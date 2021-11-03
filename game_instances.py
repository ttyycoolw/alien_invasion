# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2021/11/15 02:45
# @Author  : wangming
# @FileName: game_instances.py


import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


class GameInstances:
    """整合管理游戏中的实例"""

    def __init__(self):
        # 导入游戏设置
        self.ai_settings = Settings()
        # 创建游戏屏幕
        self.screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
        # 创建Play按钮
        self.play_button = Button(self.ai_settings, self.screen, "Play")
        # 创建一个用于存储游戏统计信息的实例，并创建记分牌
        self.stats = GameStats(self.ai_settings)
        self.sb = Scoreboard(self.ai_settings, self.screen, self.stats)
        # 创建一艘飞船、一个子弹编组和一个外星人编组
        self.ship = Ship(self.ai_settings, self.screen)
        self.aliens = Group()
        self.bullets = Group()
