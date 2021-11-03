# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2021/10/16 27:31
# @Author  : wangming
# @FileName: alien_invasion.py


import pygame

from game_instances import GameInstances
import game_functions as gf


def run_game():
    # 初始化游戏
    pygame.init()
    pygame.display.set_caption("Alien Invasion")

    # 初始化游戏实例
    objs = GameInstances()

    # 创建外星人群
    gf.create_fleet(objs)

    # 开始游戏的主循环
    while True:
        gf.check_events(objs)

        if objs.stats.game_active:
            objs.ship.update()
            gf.update_bullets(objs)
            gf.update_aliens(objs)

        gf.update_screen(objs)


if __name__ == "__main__":
    run_game()
