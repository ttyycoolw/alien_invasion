# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2021/10/11 28:38
# @Author  : wangming
# @FileName: game_functions.py


import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, objs):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        objs.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        objs.ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(objs)


def check_keyup_events(event, objs):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        objs.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        objs.ship.moving_left = False


def check_events(objs):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, objs)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, objs)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(objs, mouse_x, mouse_y)


def check_play_button(objs, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = objs.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not objs.stats.game_active:
        start_game(objs)


def start_game(objs):
    """开始新游戏，重置设置"""
    # 重置游戏设置
    objs.ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    objs.stats.reset_stats()
    objs.stats.game_active = True

    # 重置记分牌图像
    objs.sb.prep_images()

    # 清空外星人列表和子弹列表
    objs.aliens.empty()
    objs.bullets.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(objs)
    objs.ship.center_ship()


def update_screen(objs):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    objs.screen.fill(objs.ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in objs.bullets.sprites():
        bullet.draw_bullet()
    objs.ship.blitme()
    objs.aliens.draw(objs.screen)

    # 显示得分
    objs.sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not objs.stats.game_active:
        objs.play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(objs):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    objs.bullets.update()

    # 删除已消失的子弹
    for bullet in objs.bullets.copy():
        if bullet.rect.bottom <= 0:
            objs.bullets.remove(bullet)

    # 检查碰撞
    check_bullet_alien_collisions(objs)


def check_bullet_alien_collisions(objs):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(objs.bullets, objs.aliens, objs.ai_settings.common_bullet, True)

    if collisions:
        for alien in collisions.values():
            objs.stats.score += objs.ai_settings.alien_points * len(alien)
            objs.sb.prep_score()
        check_high_score(objs)

    if len(objs.aliens) == 0:
        start_new_level(objs)


def start_new_level(objs):
    """进入新等级，删除现有的子弹，加快游戏节奏，并新建一群外星人"""
    objs.bullets.empty()
    objs.ai_settings.increase_speed()

    objs.stats.level += 1
    objs.sb.prep_level()

    create_fleet(objs)


def fire_bullet(objs):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(objs.bullets) < objs.ai_settings.bullets_allowed:
        new_bullet = Bullet(objs.ai_settings, objs.screen, objs.ship)
        objs.bullets.add(new_bullet)


def get_number_aliens_x(objs, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = objs.ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(objs, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (objs.ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(objs, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(objs.ai_settings, objs.screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    objs.aliens.add(alien)


def create_fleet(objs):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(objs.ai_settings, objs.screen)
    number_aliens_x = get_number_aliens_x(objs, alien.rect.width)
    number_rows = get_number_rows(objs, objs.ship.rect.height, alien.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(objs, alien_number, row_number)


def check_fleet_edges(objs):
    """有外星人到达边缘时采取相应的措施"""
    for alien in objs.aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(objs)
            break


def change_fleet_direction(objs):
    """将整群外星人下移，并改变它们的方向"""
    for alien in objs.aliens.sprites():
        alien.rect.y += objs.ai_settings.fleet_drop_speed
    objs.ai_settings.fleet_direction *= -1


def ship_hit(objs):
    """响应被外星人撞到的飞船"""
    if objs.stats.ships_left > 0:
        # 将ships_left减1
        objs.stats.ships_left -= 1

        # 更新记分牌
        objs.sb.prep_ships()

        # 清空外星人列表和子弹列表
        objs.aliens.empty()
        objs.bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(objs)
        objs.ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        objs.stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(objs):
    """检查是否有外星人到达了了屏幕底端"""
    screen_rect = objs.screen.get_rect()
    for alien in objs.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(objs)
            break


def update_aliens(objs):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(objs)
    objs.aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(objs.ship, objs.aliens):
        ship_hit(objs)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(objs)


def check_high_score(objs):
    """检查是否诞生了新的最高得分"""
    if objs.stats.score > objs.stats.high_score:
        objs.stats.high_score = objs.stats.score
        objs.sb.prep_high_score()
