import pygame, math
pygame.init()
screen = pygame.display.set_mode((800, 600))
mouse_x, mouse_y = pygame.mouse.get_pos()
clock = pygame.time.Clock()

class light_beam:
    def __init__(self, length, angle, x, y, color, deployment):
        self.length = length
        self.angle = angle
        self.x = x
        self.y = y
        self.color = color
        self.fade = max(color) / self.length
        self.deployment = deployment
        self.red_slider = pygame.Rect((500, 20), (255, 20))
        self.green_slider = pygame.Rect((500, 60), (255, 20))
        self.blue_slider = pygame.Rect((500, 100), (255, 20))
        self.red_slider_handle = pygame.Rect((500 + self.color[0], 20), (10, 20))
        self.green_slider_handle = pygame.Rect((500 + self.color[1], 60), (10, 20))
        self.blue_slider_handle = pygame.Rect((500 + self.color[2], 100), (10, 20))
        self.length_slider = pygame.Rect((656, 140), (99, 20))
        self.length_slider_handle = pygame.Rect((656 + self.length / 10, 140), (10, 20))

    def draw(self):
        for i in range(1, self.length):
            self.deployment_range = i * self.deployment * 2
            self.deployment_fade = max(self.color) / self.deployment_range
            self.xb = round(self.x + i * math.cos(self.angle))
            self.yb = round(self.y + i * math.sin(self.angle))
            if not (self.xb < 0 or self.xb > 800 or self.yb < 0 or self.yb > 600):
                self.red = self.color[0] - i * self.fade
                self.green = self.color[1] - i * self.fade
                self.blue = self.color[2] - i * self.fade
                screen.set_at(
                              (self.xb, self.yb),
                              (self.red if self.red > 0 else 0,
                              self.green if self.green > 0 else 0,
                              self.blue if self.blue > 0 else 0)
                              )
            for j in range(round(self.deployment_range)):
                self.red1 = self.color[0] - j * self.deployment_fade - i * self.fade
                self.green1 = self.color[1] - j * self.deployment_fade - i * self.fade
                self.blue1 = self.color[2] - j * self.deployment_fade - i * self.fade
                if self.red1 > 5 or self.green1 > 5 or self.blue1 > 5:
                    self.dangle = self.deployment / self.deployment_range * j
                    self.xb1 = round(self.x + i * math.cos(self.angle + self.dangle))
                    self.yb1 = round(self.y + i * math.sin(self.angle + self.dangle))
                    self.xb2 = round(self.x + i * math.cos(self.angle - self.dangle))
                    self.yb2 = round(self.y + i * math.sin(self.angle - self.dangle))
                    screen.set_at((self.xb1, self.yb1),
                                  (self.red1 if self.red1 > 0 else 0,
                                   self.green1 if self.green1 > 0 else 0,
                                   self.blue1 if self.blue1 > 0 else 0))
                    screen.set_at((self.xb2, self.yb2),
                                  (self.red1 if self.red1 > 0 else 0,
                                   self.green1 if self.green1 > 0 else 0,
                                   self.blue1 if self.blue1 > 0 else 0))
                    #pygame.display.update()

    def get(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (200, 150, 150), self.red_slider)
        pygame.draw.rect(screen, (150, 200, 150), self.green_slider)
        pygame.draw.rect(screen, (150, 150, 200), self.blue_slider)
        pygame.draw.rect(screen, (150, 150, 150), self.length_slider)
        pygame.draw.circle(screen, (150, 150, 150), (685, 250), 70, 70)
        if pygame.mouse.get_pressed()[0]:
            if self.red_slider.collidepoint((mouse_x, mouse_y)):
                self.red_slider_handle = pygame.Rect((mouse_x, 20), (10, 20))
                self.color[0] = round(self.red_slider_handle.centerx - 510)
            if self.green_slider.collidepoint((mouse_x, mouse_y)):
                self.green_slider_handle = pygame.Rect((mouse_x, 60), (10, 20))
                self.color[1] = round(self.green_slider_handle.centerx - 510)
            if self.blue_slider.collidepoint((mouse_x, mouse_y)):
                self.blue_slider_handle = pygame.Rect((mouse_x, 100), (10, 20))
                self.color[2] = round(self.blue_slider_handle.centerx - 510)
            if self.length_slider.collidepoint((mouse_x, mouse_y)):
                self.length_slider_handle = pygame.Rect((mouse_x, 140), (10, 20))
                self.length = (mouse_x - 655) * 10
                self.fade = max(self.color) / self.length
            if math.sqrt((mouse_y - 250) ** 2 + (mouse_x - 685) ** 2) < 50:
                self.angle = math.atan2(mouse_y - 250, mouse_x - 685)
            if 70 > math.sqrt((mouse_y - 250) ** 2 + (mouse_x - 685) ** 2) > 50:
                self.deployment = abs(math.atan2(mouse_y - 250, mouse_x - 685) - self.angle)
        if pygame.mouse.get_pressed()[2]:
            self.x, self.y = mouse_x, mouse_y
        pygame.draw.rect(screen, (255, 230, 230), self.red_slider_handle)
        pygame.draw.rect(screen, (230, 255, 230), self.green_slider_handle)
        pygame.draw.rect(screen, (230, 230, 255), self.blue_slider_handle)
        pygame.draw.rect(screen, (250, 250, 250), self.length_slider_handle)
        pygame.draw.line(screen, (255, 255, 255), (685, 250), (685 + 50 * math.cos(self.angle), 250 + 50 * math.sin(self.angle)))
        pygame.draw.line(screen, (255, 255, 255), (685 + 50 * math.cos(self.angle + self.deployment),
                                                   250 + 50 * math.sin(self.angle + self.deployment)), (
                         685 + 70 * math.cos(self.angle + self.deployment),
                         250 + 70 * math.sin(self.angle + self.deployment)))
        pygame.draw.line(screen, (255, 255, 255), (685 + 50 * math.cos(self.angle - self.deployment),
                                                   250 + 50 * math.sin(self.angle - self.deployment)), (
                         685 + 70 * math.cos(self.angle - self.deployment),
                         250 + 70 * math.sin(self.angle - self.deployment)))

screen.fill((0, 0, 0))
beam_list = [light_beam(300, 45 / 180 * math.pi, 200, 200, [200, 225, 255], 30 / 180 * math.pi)]

while True:
    clock.tick(30)
    pygame.display.set_caption(f'FPS: {clock.get_fps()}')
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for i in beam_list:
        i.draw()
        i.get()

    pygame.display.update()