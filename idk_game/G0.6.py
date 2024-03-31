import pygame
import math
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Consolas', 20)
myfont2 = pygame.font.SysFont('Coibri', 40)
screen = pygame.display.set_mode((800, 600))
state = 'menu'
background_image = pygame.image.load('BACKGROUND.png')
image = pygame.image.load('SHIP.png').convert_alpha()
dead_image = pygame.image.load('DEAD_SHIP.png').convert_alpha()
enemy_image = pygame.image.load('ENEMY_SHIP.png')
enemy_dead_image = pygame.image.load('DEAD_ENEMY_SHIP.png')
selected_image = pygame.image.load('SELECTED_SHIP.png')
speed_control_button_image_1 = pygame.image.load('SPEEDCONTR.png')
speed_control_button_image_2 = pygame.image.load('SPEEDCONTR2.png')
slider = pygame.Rect(10, 10, 100, 20)
key_down = False
ship_count = 0
ship_count_2 = 0
speed_control = True
camera_speed = 6
friendly_count = 0
enemy_count = 0

class ship:
    def __init__(self, image, dead_image, x, y, team, angle):
        self.image = image
        self.dead_image = dead_image
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = angle
        self.desired_angle = self.angle
        self.turn_rate = 0
        self.desired_turn_rate = 0
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.target = None
        self.cooldown = 0
        self.shell_x = self.x
        self.shell_y = self.y
        self.shell_in_flight = False
        self.hp = 100
        self.team = team
        self.slider_x = 10
        self.state = 'retreat'
        if self.team == 0:
            self.selected = False
            self.slider_handle = pygame.Rect(self.slider_x, 10, 10, 20)
            self.thrust_indicator = myfont.render("0%", True, (255, 255, 255))
            self.turn = False
        else:
            self.turn = True

    def decide(self):
        if enemy_count > 0 and self.team != 0 and self.state != 'dead':
            if enemy_count > friendly_count:
                self.state = 'retreat'
            else:
                self.state = 'atack'

        if enemy_count == 0:
            self.desired_angle = math.pi

    def point(self):
        if self.team == 0 and self.selected and pygame.mouse.get_pressed()[0] and not self.rect.collidepoint(pygame.mouse.get_pos()) and self.team == 0:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            self.turn = True

        if self.turn:
            self.desired_angle = math.atan2(self.mouse_y - self.y, self.mouse_x - self.x)

    def move(self):
        self.distance = math.sqrt((self.x - self.mouse_x) ** 2 + (self.y - self.mouse_y) ** 2)

        if self.team != 0 and enemy_count > 0:
            if self.state == 'atack':
                self.desired_angle = self.target_angle
                self.slider_x = 60
            if self.state == 'retreat':
                self.desired_angle = self.target_angle - math.pi if self.target_angle >= 0 else self.target_angle + math.pi
                self.slider_x = 110

        if self.speed < (self.slider_x - 10) / 200:
            self.speed += 0.0005
        if self.speed > (self.slider_x - 10) / 200:
            self.speed -= 0.0005

        if self.desired_angle != None:
            if self.desired_angle - self.angle >= math.pi:
                self.angle += 2 * math.pi
            if self.angle - self.desired_angle > math.pi:
                self.desired_angle += 2 * math.pi

        self.desired_turn_rate = (0.6 - self.speed / 4) * math.pi / 360

        if self.desired_angle < self.angle:
            self.desired_turn_rate *= -1

        if self.turn_rate - self.desired_turn_rate < -0.001:
            self.turn_rate += 0.00001
        elif self.turn_rate - self.desired_turn_rate > 0.001:
            self.turn_rate -= 0.00001

        if self.distance < 100:
            self.turn = False
            if not speed_control:
                self.slider_x = 10

        if self.turn and self.desired_angle != None:
            self.angle += self.turn_rate

            if not speed_control:
                if self.distance > 300:
                    self.slider_x = 110
                else:
                    self.slider_x = self.distance / 3 + 10

        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def shoot(self, enemy_ship_list):
        if self.target != None:
            if self.cooldown == 0:
                self.shell_x, self.shell_y = self.rect.center
                self.target_angle = math.atan2(enemy_ship_list[self.target].y - self.y, enemy_ship_list[self.target].x - self.x)
                self.shell_in_flight = True
                self.cooldown = 500

            if self.shell_in_flight:
                self.shell_x += 2 * math.cos(self.target_angle)
                self.shell_y += 2 * math.sin(self.target_angle)
                pygame.draw.circle(screen, (255, 255, 100), (self.shell_x, self.shell_y), 2, 2)
                if enemy_ship_list[self.target].rect.collidepoint(self.shell_x, self.shell_y):
                    self.shell_in_flight = False
                    enemy_ship_list[self.target].hp -= 20

            self.cooldown -= 1

            if enemy_ship_list[self.target].hp <= 0:
                self.target = None

    def scan(self, ship_list, return_value_1 = True, return_value_2 = True):
        self.min_distance = float('inf')
        self.min_distance_2 = float('inf')
        self.index = None
        self.scan_angle = None
        self.scan_angle_2 = None
        self.index_2 = None
        for i in ship_list:
            if self.hp > 0 and i.hp > 0:
                if return_value_1 and self.team != i.team:
                    self.dist = math.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2)
                    if self.dist < self.min_distance:
                        self.min_distance = self.dist
                        self.scan_angle = math.atan2(i.y - self.y, i.x - self.x)
                        self.index = ship_list.index(i)

                if return_value_2 and self.team == i.team and ship_list.index(i) != ship_list.index(self):
                    self.dist = math.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2)
                    if self.dist < self.min_distance_2:
                        self.min_distance_2 = self.dist
                        self.scan_angle_2 = math.atan2(i.y - self.y, i.x - self.x)
                        self.index_2 = ship_list.index(i)

        if return_value_1 and return_value_2:
            return self.min_distance, self.scan_angle, self.index, self.min_distance_2, self.scan_angle_2, self.index_2
        if return_value_1 and not return_value_2:
            return self.min_distance, self.scan_angle, self.index
        if not return_value_1 and return_value_2:
            return self.min_distance_2, self.scan_angle_2, self.index_2

    def draw(self):
        if self.hp <= 0:
            self.image = self.dead_image
            self.slider_x = 10
            self.desired_turn_rate = 0
            self.target = None
            if self.team == 0:
                self.selected = False
            else:
                self.state = 'dead'
            for i in ship_list:
                if i.target == ship_list.index(self):
                    i.target = None

        self.rotated_image = pygame.transform.rotate(self.image, -self.angle / math.pi * 180)
        self.rect = self.rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x,self.y)).center)
        screen.blit(self.rotated_image, self.rect)
        screen.blit(myfont.render(str(self.hp), True, (100, 100, 100)), self.rect.center)

    def get_speed(self):
        if pygame.mouse.get_pressed()[0] and slider.collidepoint(pygame.mouse.get_pos()) and self.selected:
            self.slider_x,temp = pygame.mouse.get_pos()

    def draw_controls(self):
        self.slider_handle = pygame.Rect(self.slider_x, 10, 10, 20)
        self.thrust_indicator = myfont.render(str(round(self.slider_x - 10)) + "%", True, (255,255,255))
        if self.selected:
            pygame.draw.rect(screen, (100, 100, 100), slider)
            pygame.draw.rect(screen, (200, 200, 200), self.slider_handle)
            screen.blit(self.thrust_indicator, (120, 10))

class button:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

    def press(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def create_ships(ship_number, enemy_ship_number, image, image_2, dead_image, dead_image_2):
    ship_list = []
    ship_y = 0
    ship_y_2 = 0

    for i in range(ship_number):
        if i % 2 == 1:
            ship_y += 150
        ship_list.append(ship(image, dead_image, 100, 250 + ship_y * ((-1) ** i), 0, 0))

    for i in range(enemy_ship_number):
        if i % 2 == 1:
            ship_y_2 += 150
        ship_list.append(ship(image_2, dead_image_2, 2000, 250 + ship_y_2 * ((-1) ** i), 1, math.pi))

    return ship_list

ship_list = []
group_list = []

start_button = button(pygame.image.load("start.png"), 50, 50)
start_button_2 = button(pygame.image.load("start.png"), 220, 300)
quit_button = button(pygame.image.load("quit.png"), 50, 200)
plus_button_1 = button(pygame.image.load("PLUS.png"), 100, 50)
minus_button_1 = button(pygame.image.load("MINUS.png"), 250, 50)
plus_button_2 = button(pygame.image.load("PLUS.png"), 500, 50)
minus_button_2 = button(pygame.image.load("MINUS.png"), 650, 50)
resume_button = button(pygame.image.load("resume.png"), 230, 150)
return_to_menu_button = button(pygame.image.load("returntomenu.png"), 5, 300)
back_button = button(pygame.image.load('BACK (1).png'), 300, 450)
speed_control_button = button(speed_control_button_image_1, 675, 25)

while True:
    keys = pygame.key.get_pressed()
    pygame.time.delay(6)
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if pygame.mouse.get_pressed()[0]:
        if state == 'game' and not key_down:
            for i in range(len(ship_list)):
                if ship_list[i].team == 0 and ship_list[i].rect.collidepoint(pygame.mouse.get_pos()):
                    ship_list[i].selected = not ship_list[i].selected
                    ship_list[i].image = selected_image if ship_list[i].selected else image
                    for j in range(len(ship_list)):
                        if j != i and ship_list[j].team == 0:
                            ship_list[j].selected = False
                            ship_list[j].image = image

                if ship_list[i].team == 0 and ship_list[i].selected:
                    for j in range(len(ship_list)):
                        if ship_list[j].team == 1 and ship_list[j].rect.collidepoint(pygame.mouse.get_pos()) and ship_list[j].hp > 0:
                            ship_list[i].target = j

            if speed_control_button.press():
                    speed_control = not speed_control

        if state == 'menu' and not key_down:
            if start_button.press():
                state = 'start'
            elif quit_button.press():
                pygame.quit()

        if state == 'pause' and not key_down:
            if resume_button.press():
                state = 'game'
            elif return_to_menu_button.press():
                state = 'menu'
                ship_list = []

        if state == 'start' and not key_down:
            if plus_button_1.press():
                ship_count += 1

            elif minus_button_1.press() and ship_count > 0:
                ship_count -= 1

            elif plus_button_2.press():
                ship_count_2 += 1

            elif minus_button_2.press() and ship_count_2 > 0:
                ship_count_2 -= 1

            elif start_button_2.press():
                state = 'game'

                ship_list = create_ships(ship_count, ship_count_2, image, enemy_image, dead_image, enemy_dead_image)

                ship_count = 0
                ship_count_2 = 0

            elif back_button.press():
                state = 'menu'

                ship_count = 0
                ship_y = 0
                ship_list = []

                ship_count_2 = 0
                ship_y_2 = 0
                enemy_ship_list = []

        key_down = True

    else:
        key_down = False

    if keys[pygame.K_ESCAPE]:
        if state == 'game':
            state = 'pause'
        escape_key_down = True

    if state == 'game':
        if keys[pygame.K_w]:
            for i in ship_list:
                i.y += camera_speed
                i.mouse_y += camera_speed
                i.shell_y += camera_speed
        if keys[pygame.K_s]:
            for i in ship_list:
                i.y -= camera_speed
                i.mouse_y -= camera_speed
                i.shell_y -= camera_speed
        if keys[pygame.K_a]:
            for i in ship_list:
                i.x += camera_speed
                i.mouse_x += camera_speed
                i.shell_x += camera_speed
        if keys[pygame.K_d]:
            for i in ship_list:
                i.x -= camera_speed
                i.mouse_x -= camera_speed
                i.shell_x -= camera_speed

        friendly_count = 0
        enemy_count = 0

        for i in ship_list:
            if i.team != 0:
                friendly_count += 1
            else:
                enemy_count +=1

        for i in ship_list:
            if i.team != 0 and i.hp > 0:
                temp, i.target_angle, i.target = i.scan(ship_list, True, False)

            if i.team == 0 and i.hp > 0:
                if speed_control:
                    i.get_speed()
                    i.draw_controls()

                if not slider.collidepoint(pygame.mouse.get_pos()) and not speed_control_button.press():
                    i.point()

            i.decide()

            if friendly_count == 0 or enemy_count == 0:
                state = 'menu'
                break

            i.move()
            i.draw()
            i.shoot(ship_list)

        if speed_control:
            speed_control_button = button(speed_control_button_image_1, 675, 25)

        else:
            speed_control_button = button(speed_control_button_image_2, 675, 25)

        speed_control_button.draw()

    if state == 'pause':
        resume_button.draw()
        return_to_menu_button.draw()

    if state == 'start':
        plus_button_1.draw()
        minus_button_1.draw()
        plus_button_2.draw()
        minus_button_2.draw()
        start_button_2.draw()
        back_button.draw()
        menu_ship_count_1 = myfont2.render("You:" + str(ship_count), True, (255, 255, 200))
        menu_ship_count_2 = myfont2.render("Enemy:" + str(ship_count_2), True, (255, 255, 200))
        screen.blit(menu_ship_count_1, (190, 200))
        screen.blit(menu_ship_count_2, (570, 200))

    if state =='menu':
        start_button.draw()
        quit_button.draw()

    pygame.display.update()