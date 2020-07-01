import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play和Help按钮
    play_button = Button(ai_settings, screen, "Play", 250)
    help_button = Button(ai_settings, screen, "Help", 650)
    ok_button = Button(ai_settings, screen, "Ok", 450)
    replay_button = Button(ai_settings, screen, "Replay", 250)
    
    # 创建存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 加载各页面图片
    help_image = pygame.image.load('images/help.bmp')
    cover_image = pygame.image.load('images/cover.bmp')
    end_image = pygame.image.load('images/end.bmp')
    
    # 开始游戏的主循环
    while True:    
        gf.check_events(ai_settings, screen, stats, sb, play_button,
            help_button, ok_button, ship, aliens, bullets)
        
        if stats.game_active and not stats.help_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
            bullets, play_button, help_button, ok_button, replay_button,
            cover_image, help_image, end_image)

run_game()
