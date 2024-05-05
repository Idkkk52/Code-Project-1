import pygame, math
pygame.init()
pygame.font.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('VERLET INTEGRATION')

force_x = 0
force_y = 400

screen_color = (150, 175, 200)

mouse_x, mouse_y = pygame.mouse.get_pos()
space_flag = False
LMB_flag = False
flag_1 = False
space_down = False

class Ball:
    def __init__(self, x, y, fixed = False, col = (255, 0, 0), mass = 1):
        self.mass = mass
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.fixed = fixed
        self.grabbed = False
        self.selected = False
        self.radius = self.mass ** 0.33 * 4 if not self.fixed else 4
        self.col = col if not self.fixed else (100, 100, 100)

    def move(self, delta_time):
        if not self.grabbed:
            if not self.fixed:
                self.speed_x = self.x - self.old_x
                self.speed_y = self.y - self.old_y
                self.old_x = self.x
                self.old_y = self.y
                self.x += self.speed_x + force_x * delta_time * delta_time
                self.y += self.speed_y + force_y * delta_time * delta_time
        else:
            self.x, self.y = mouse_x, mouse_y
            self.old_x, self.old_y = mouse_x, mouse_y

        if math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) < 25 and pygame.mouse.get_pressed()[0]:
            c = 0
            for i in ball_list:
                c += 1 if not(i.grabbed) else 0
            if c == len(ball_list): self.grabbed = True

        if self.grabbed and (math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) > 25 or not pygame.mouse.get_pressed()[0]):
            self.grabbed = False

    def constraints(self):
        if not self.fixed:
            if self.x > WIDTH:
                self.x = WIDTH
                self.old_x = self.x + self.speed_x
            if self.y > HEIGHT:
                self.y = HEIGHT
                self.old_y = self.y + self.speed_y
            if self.x < 0:
                self.x = 0
                self.old_x = self.x + self.speed_x
            if self.y < 0:
                self.y = 0
                self.old_y = self.y + self.speed_y

    def draw(self, pause):
        if self.selected and pause: pygame.draw.circle(screen, (255, 255, 0),
                                                       (self.x, self.y),
                                                       round(self.radius) + 1 ,
                                                       round(self.radius) + 1)
        pygame.draw.circle(screen, self.col,
                           (self.x, self.y),
                           round(self.radius) ,
                           round(self.radius))

class Link:
    def __init__(self, ball1, ball2, length = 50):
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
        if not (self.ball1.fixed or self.ball1.grabbed) and not (self.ball2.fixed or self.ball2.grabbed):
            self.ball1.x -= self.offset_x / self.ball1.mass
            self.ball1.y -= self.offset_y / self.ball1.mass
            self.ball2.x += self.offset_x / self.ball2.mass
            self.ball2.y += self.offset_y / self.ball2.mass

        if (self.ball1.fixed or self.ball1.grabbed) and not (self.ball2.fixed or self.ball2.grabbed):
            self.ball2.x += self.offset_x * 2 / self.ball2.mass
            self.ball2.y += self.offset_y * 2 / self.ball2.mass

        if (self.ball2.fixed or self.ball2.grabbed) and not (self.ball1.fixed or self.ball1.grabbed):
            self.ball1.x -= self.offset_x * 2 / self.ball1.mass
            self.ball1.y -= self.offset_y * 2 / self.ball1.mass

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), (self.ball1.x, self.ball1.y), (self.ball2.x, self.ball2.y))

ball_list = []
             #Ball(1, 200, 300, False)]
link_list = []

while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    if keys[pygame.K_SPACE] and not space_flag:
        space_down = not space_down
        space_flag = True

        if space_down: screen_color = (125, 150, 175)
        else: screen_color = (150, 175, 200)

        pygame.time.delay(300)

    else:
        space_flag = False

    for i in link_list:
        if not space_down: i.spring(0.001)
        i.draw()

    for i in ball_list:
        i.draw(space_down)

        if not space_down:
            i.move(0.001)
            i.constraints()

        else:
            if pygame.mouse.get_pressed()[0]:
                for i in ball_list:
                    if -i.radius < i.x - mouse_x < i.radius and -i.radius < i.y - mouse_y < i.radius:
                        if not LMB_flag:
                            i.selected = not i.selected
                            LMB_flag = True
                            pygame.time.delay(300)

            else: LMB_flag = False

    if pygame.mouse.get_pressed()[2] and space_down:
        ball_list.append(Ball(mouse_x, mouse_y, keys[pygame.K_z]))

        for i in ball_list:
            if i.selected and i != ball_list[len(ball_list) - 1]:
                link_list.append(Link(i, ball_list[len(ball_list) - 1]))
                i.selected = False

        ball_list[len(ball_list) - 1].selected = True
        pygame.time.delay(300)

    if keys[pygame.K_1] and not flag_1:

        for i in range(10):
            for j in range(10):
                ball_list.append(Ball(50 + i * 25, 100 + j * 25))

        for i in range(len(ball_list)):
            if i % 10 != 9: link_list.append(Link(ball_list[i], ball_list[i + 1], 25))
            if i < 90: link_list.append(Link(ball_list[i], ball_list[i + 10], 25))

        ball_list.append(Ball(50, 50, True))
        ball_list.append(Ball(275, 50, True))
        link_list.append(Link(ball_list[100], ball_list[0], 25))
        link_list.append(Link(ball_list[101], ball_list[90], 25))

        flag_1 = True

        pygame.time.delay(500)

    else: flag_1 = False

    pygame.display.update()
