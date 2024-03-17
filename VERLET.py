import pygame, math
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('VERLET INTEGRATION')
force_x = 0
force_y = 400
mouse_x, mouse_y = pygame.mouse.get_pos()
class Ball:
    def __init__(self, mass, x, y, fixed):
        self.mass = mass
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.acceleration_x = force_x / self.mass
        self.acceleration_y = force_y / self.mass
        self.fixed = fixed
        self.grabbed = False

    def move(self, delta_time):
        if math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) > 25 or not pygame.mouse.get_pressed()[0]:
            if not self.fixed:
                self.speed_x = self.x - self.old_x
                self.speed_y = self.y - self.old_y
                self.old_x = self.x
                self.old_y = self.y
                self.x += self.speed_x + self.acceleration_x * delta_time * delta_time
                self.y += self.speed_y + self.acceleration_y * delta_time * delta_time
            self.grabbed = False
        else:
            c = 0
            for i in ball_list:
                c += 1 if not(i.grabbed) else 0
            if c == len(ball_list): self.grabbed = True
        if self.grabbed:
            self.x, self.y = mouse_x, mouse_y
            self.old_x, self.old_y = mouse_x, mouse_y

    def constraints(self):
        if self.x > 600:
            self.x = 600
            self.old_x = self.x + self.speed_x
        if self.y > 600:
            self.y = 600
            self.old_y = self.y + self.speed_y
        if self.x < 0:
            self.x = 0
            self.old_x = self.x + self.speed_x
        if self.y < 0:
            self.y = 0
            self.old_y = self.y + self.speed_y

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5 , 5)

class Link:
    def __init__(self, ball1, ball2, length):
        self.ball1 = ball1
        self.ball2 = ball2
        self.length = length if length > 0 else math.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)

    def spring(self, springness):
        self.distance_x = self.ball2.x - self.ball1.x
        self.distance_y = self.ball2.y - self.ball1.y
        self.distance = math.sqrt(self.distance_x ** 2 + self.distance_y ** 2)
        self.difference = self.length - self.distance
        self.percent = (self.difference / self.distance) / 2
        self.offset_x = self.distance_x * self.percent * springness
        self.offset_y = self.distance_y * self.percent * springness
        if not self.ball1.fixed and not self.ball1.grabbed:
            self.ball1.x -= self.offset_x
            self.ball1.y -= self.offset_y
        else:
            self.ball2.x += self.offset_x * 2
            self.ball2.y += self.offset_y * 2
        if not self.ball2.fixed and not self.ball2.grabbed:
            self.ball2.x += self.offset_x
            self.ball2.y += self.offset_y
        else:
            self.ball1.x -= self.offset_x * 2
            self.ball1.y -= self.offset_y * 2

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), (self.ball1.x, self.ball1.y), (self.ball2.x, self.ball2.y))

ball_list = [Ball(1, 200, 200, True),
             Ball(1, 300, 200, False),
             Ball(1, 300, 300, False),]
             #Ball(1, 200, 300, False)]
link_list = [Link(ball_list[0], ball_list[1], 100),
             Link(ball_list[1], ball_list[2], 100),]
             #Link(ball_list[2], ball_list[0], 90),]
             #Link(ball_list[2], ball_list[3], 100),
             #Link(ball_list[0], ball_list[2], 0)]

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill((150, 175, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for i in link_list:
        i.spring(0.01)
        i.draw()

    for i in ball_list:
        i.draw()
        i.move(0.001)
        i.constraints()

    pygame.display.update()