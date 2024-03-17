import pygame
import random
pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption('PING-PONG GAME')
screen_color = (75, 75, 75)
pygame.font.init()
myfont = pygame.font.SysFont('Consolas', 20)

class tile:
    def __init__(self, x, y, speed, width, height, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect((self.x, self.y), (width, height))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x < 350:
            self.x += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

tile = tile(175, 570, 4, 150, 5, (255, 255, 0))

class ball:
    def __init__(self, x, y, speed_x, speed_y, mass, force, delta_time, color):
        self.hit_bottom = False
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.acceleration = force / mass
        self.delta_time = delta_time
        self.score = 0
        self.fail_score = 0

    def move(self):
        self.x += self.speed_x * self.delta_time
        self.y += self.speed_y * self.delta_time
        self.speed_y += self.acceleration * self.delta_time + 0.05
        if self.x < 0:
            self.x = 0
            self.speed_x *= -1
        if self.x > 500:
            self.x = 500
            self.speed_x *= -1
        if self.y < 0:
            self.y = 0
            self.speed_y *= -1
        if tile.x < self.x < tile.x + 150 and self.y > 570:
            self.y = 570
            self.speed_y *= -1
            self.score += 1
        if self.y > 600:
            self.hit_bottom = True
            self.fail_score += 1

    def hit(self):
        if self.hit_bottom:
            self.speed_x, self.speed_y = 0, 0
            self.color_save = self.color
            for i in range(8):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                self.color = (75, 75, 75) if i % 2 == 0 else self.color_save
                pygame.draw.circle(screen, self.color, (self.x, self.y), 10, 10)
                pygame.time.delay(333)
                pygame.display.update()
            self.hit_bottom = False
            self.x = random.randint(200, 300)
            self.y = random.randint(250, 350)
            self.speed_x = random.choice([-300, -200, 200, 300])
            self.speed_y = random.randint(0, 100)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10, 10)

ball = ball(random.randint(200, 300), random.randint(250, 350), random.choice([-300, 300]), random.randint(0, 100), 1, 400, 0.01, (255, 100, 0))

def print_stats(score, fail_score):
    score_indicator = myfont.render(f'score: {score}', True, (200, 200, 200))
    fail_score_indicator = myfont.render(f'fails: {fail_score}', True, (200, 200, 200))
    screen.blit(score_indicator, (0, 0))
    screen.blit(fail_score_indicator, (0, 20))

while True:
    pygame.time.delay(7)
    screen.fill(screen_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    tile.move()
    tile.draw()
    ball.move()
    ball.hit()
    ball.draw()
    print_stats(ball.score, ball.fail_score)
    pygame.display.update()