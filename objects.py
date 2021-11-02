# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2021/11/15 02:45
# @Author  : wangming
# @FileName: objects.py


class Objects:
    """整合管理游戏中的实例"""

    def __init__(self, ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
        self.ai_settings = ai_settings
        self.screen = screen
        self.stats = stats
        self.sb = sb
        self.play_button = play_button
        self.ship = ship
        self.aliens = aliens
        self.bullets = bullets
