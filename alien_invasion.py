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

    # 开始游戏的主循环
    while True:
        # 检测操作
        gf.check_events(objs)
        # 更新实例，并刷新屏幕
        objs.update()


if __name__ == "__main__":
    run_game()
