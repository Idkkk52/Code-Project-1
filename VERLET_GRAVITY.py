import pygame, math
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('VERLET INTEGRATION (WITH GRAVITY)')
mouse_x, mouse_y = pygame.mouse.get_pos()
fill = True
image = pygame.Surface((3000, 3000))
x = -1000
y = -1000

class Ball:
    def __init__(self, mass, x, old_x, y, old_y, fixed, color):
        self.mass = mass
        self.x = x
        self.y = y
        self.old_x = old_x
        self.old_y = old_y
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.fixed = fixed
        self.color = color

    def move(self, delta_time):
        if not self.fixed:
            for i in ball_list:
                if ball_list.index(self) != ball_list.index(i):
                    self.speed_x = self.x - self.old_x
                    self.speed_y = self.y - self.old_y
                    self.old_x = self.x
                    self.old_y = self.y
                    self.angle = math.atan2(self.y - i.y, self.x - i.x)
                    self.distance = math.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2)
                    self.force = (self.mass * i.mass) * 15 / (self.distance ** 2)
                    self.acceleration = self.force / self.mass
                    self.acceleration_x = self.acceleration * math.cos(self.angle)
                    self.acceleration_y = self.acceleration * math.sin(self.angle)
                    self.x += self.speed_x - self.acceleration_x * delta_time * delta_time
                    self.y += self.speed_y - self.acceleration_y * delta_time * delta_time

    def draw(self, fill):
        if fill:
            pygame.draw.circle(screen, self.color, (self.x - 1000, self.y - 1000), 5, 5)
        else:
            image.set_at((round(self.x), round(self.y)), self.color)

ball_list = [Ball(1, 1150, 1150.01, 1200, 1199.96, False, (255, 0, 0)), Ball(10, 1300, 1300, 1300, 1300, False, (0, 255, 0)), Ball(1, 1550, 1550, 1550, 1550.02, False, (0, 0, 255))]

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if fill:
        screen.fill((150, 175, 200))
    else:
        screen.blit(image, (x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if keys[pygame.K_w]:
        for i in ball_list:
            if fill:
                i.y += 1
                i.old_y += 1
            y += 1
    if keys[pygame.K_s]:
        for i in ball_list:
            if fill:
                i.y -= 1
                i.old_y -= 1
            y -= 1
    if keys[pygame.K_a]:
        for i in ball_list:
            if fill:
                i.x += 1
                i.old_x += 1
            x += 1
    if keys[pygame.K_d]:
        for i in ball_list:
            if fill:
                i.x -= 1
                i.old_x -= 1
            x -= 1

    for i in ball_list:
        i.draw(fill)
        i.move(0.1)

    pygame.display.update()