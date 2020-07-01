import sys
import pygame
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien
from button import Button

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens,
        bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        
        # 隐藏光标
        pygame.mouse.set_visible(False)
        
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, help_button,
        ok_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 按键
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship,
                aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship) 
        # 鼠标
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not stats.game_active:
                if stats.help_active and ok_button.rect.collidepoint(mouse_x, mouse_y):
                        stats.help_active = False
                elif not stats.help_active and help_button.rect.collidepoint(mouse_x, mouse_y):
                        stats.help_active = True
                elif not stats.help_active and play_button.rect.collidepoint(mouse_x, mouse_y):
                        # 重置游戏设置
                        ai_settings.initialize_dynamic_settings()
                        
                        # 隐藏光标
                        pygame.mouse.set_visible(False)
                        
                        # 重置游戏统计信息
                        stats.reset_stats()
                        stats.game_active = True
                        stats.game_over = False

                        # 重置记分牌图像
                        sb.prep_score()
                        sb.prep_high_score()
                        sb.prep_level()
                        sb.prep_ships()

                        # 清空外星人列表和子弹列表
                        aliens.empty()
                        bullets.empty()

                        # 创建一群新的外星人，并让飞船居中
                        create_fleet(ai_settings, screen, ship, aliens)
                        ship.center_ship()


"""
def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
        aliens, bullets, mouse_x, mouse_y):
    # 在玩家单击Play按钮时开始新游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        
        # 隐藏光标
        pygame.mouse.set_visible(False)
        
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
"""
        
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button, help_button, ok_button, replay_button,
        cover_image, help_image, end_image):
    """更新屏幕上的图像，并切换到新屏幕"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if stats.help_active:
        screen.blit(help_image, (0,0))
        ok_button.draw_button()
        
        # 判断鼠标是否在按钮上
        if ok_button.rect.collidepoint(mouse_x, mouse_y):
            ok_button.redraw_button()  
    elif stats.game_active:
        # 每次循环时都重绘屏幕
        screen.fill(ai_settings.bg_color)
        # 在飞船和外星人后面重绘所有子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        # 显示得分
        sb.show_score()
    elif stats.game_over:
        screen.blit(end_image, (0,0))
        replay_button.draw_button()
        help_button.draw_button()
        
        # 判断鼠标是否在按钮上
        if replay_button.rect.collidepoint(mouse_x, mouse_y):
            replay_button.redraw_button()
        if help_button.rect.collidepoint(mouse_x, mouse_y):
            help_button.redraw_button()
    else:
        screen.blit(cover_image, (0,0))
        play_button.draw_button()
        help_button.draw_button()

        # 判断鼠标是否在按钮上
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            play_button.redraw_button()
        if help_button.rect.collidepoint(mouse_x, mouse_y):
            help_button.redraw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
            
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    my_groupcollide(ai_settings, screen, stats, sb, ship, aliens, bullets)

def my_groupcollide(ai_settings, screen, stats, sb, ship, aliens, bullets):
    count = 0
    for bullet in bullets.copy():
        judge = False
        for alien in aliens.copy():
            if bullet.num > 0.5 and alien.num > 0.5 or bullet.num <= 0.5 and alien.num <= 0.5:
                    if abs(bullet.rect.x - alien.rect.x) < ai_settings.bullet_width/2 + alien.rect.width/2:
                        if abs(bullet.rect.y - alien.rect.y) < ai_settings.bullet_height/2 + alien.rect.height/2:
                            aliens.remove(alien)
                            count += 1
                            judge = True
        if judge:
            bullets.remove(bullet)
    stats.score += ai_settings.alien_points * count
    sb.prep_score()
    check_high_score(stats, sb)

    if len(aliens) == 0:
        # 如果整群外星人都被消灭， 就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level +=1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
        
"""
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
    # 响应子弹和外星人的碰撞
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
"""

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                             (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应飞船被外星人撞到"""
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        stats.game_over = True
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
        bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
        
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
