import pygame
import random
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('SNOW2')
bottom = 500

class snowflake:
    def __init__(self, size, color, fallen, x, y):
        self.size = size
        self.color = color
        self.fallen = fallen
        self.x = x
        self.y = y
        if not self.fallen:
            self.speed_x = 0#random.randint(-10, 10) / 100
            self.speed_y = random.randint(10,15) / 30 * self.size

    def move(self):
        if not self.fallen:
            self.x += self.speed_x
            self.y += self.speed_y
            if self.y > bottom:
                self.y = random.randint(-400, 0)
                snowflake_list.append(snowflake(self.size, self.color, True, self.x, bottom))
                self.x = random.randint(0, 500)
                return 0.01
        return 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.size)

snowflake_list = []

for i in range(50):
    snowflake_list.append(snowflake(3, (255, 255, 255), False, random.randint(0, 500), random.randint(-400, 0)))
    snowflake_list.append(snowflake(2, (225, 225, 225), False, random.randint(0, 500), random.randint(-400, 0)))
    snowflake_list.append(snowflake(2, (225, 225, 225), False, random.randint(0, 500), random.randint(-400, 0)))
    snowflake_list.append(snowflake(1, (200, 200, 200), False, random.randint(0, 500), random.randint(-400, 0)))
    snowflake_list.append(snowflake(1, (200, 200, 200), False, random.randint(0, 500), random.randint(-400, 0)))
    snowflake_list.append(snowflake(1, (200, 200, 200), False, random.randint(0, 500), random.randint(-400, 0)))

while True:
    screen.fill((80, 100, 150))
    #pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for i in snowflake_list:
        bottom -= i.move()
        i.draw()

    pygame.display.update()