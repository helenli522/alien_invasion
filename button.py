import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg, button_x):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color_1 = (230, 230, 230)
        self.text_color_1 = (92, 167, 186)
        self.font = pygame.font.SysFont(None, 48)
                
        self.button_color_2 = (0, 255, 0)
        self.text_color_2 = (230, 230, 230)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = button_x
        self.rect.top = 400

        # 创建两种状态下的按钮标签
        self.prep_msg(msg)
        self.chan_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染为第一种图像，并使其在按钮上居中"""
        self.msg_image_1 = self.font.render(msg, True, self.text_color_1,
            self.button_color_1)
        self.msg_image_rect_1 = self.msg_image_1.get_rect()
        self.msg_image_rect_1.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color_1, self.rect)
        self.screen.blit(self.msg_image_1, self.msg_image_rect_1)

    def chan_msg(self, msg):
        """将msg渲染为第二种图像，并使其在按钮上居中"""
        self.msg_image_2 = self.font.render(msg, True, self.text_color_2,
            self.button_color_2)
        self.msg_image_rect_2 = self.msg_image_2.get_rect()
        self.msg_image_rect_2.center = self.rect.center

    def redraw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color_2, self.rect)
        self.screen.blit(self.msg_image_2, self.msg_image_rect_2)

