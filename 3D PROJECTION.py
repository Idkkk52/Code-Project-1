import pygame
import math
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

#def matrix_vector_multiplication(matrix_1, matrix_2):
 #   result_matrix = [matrix_1[0][0] * matrix_2[0], matrix_1[1][1] * matrix_2[1], matrix_1[]]

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.connection_list = []

    def draw(self, FOV, z_far, z_near, aspect_ratio):
        self.normal_x = self.x * aspect_ratio * (1 / math.tan(FOV / 2))
        self.normal_y = self.y * (1 / math.tan(FOV / 2))
        self.normal_z = (z_far / (z_far - z_near)) * self.z - (z_far / (z_far - z_near)) * z_near
        if self.z != 0:
            self.normal_x /= self.z
            self.normal_y /= self.z
        #print(self.normal_x * self.z, self.normal_y * self.z, self.normal_z * self.z)
        pygame.draw.circle(screen, (255, 0, 0), (round((width / 2) * (self.normal_x + 1)), round((height / 2) * (self.normal_y +1))), 5, 5)

    def connect(self):
        for i in self.connection_list:
            pygame.draw.line(screen, (255, 255, 255), (round((width / 2) * (self.normal_x +1)), round((height / 2) * (self.normal_y +1))), (round((width / 2) * (i.normal_x +1)), round((height / 2) * (i.normal_y +1))))


vertex_list = [Vertex(-1, -1, 2),
               Vertex(-1, 1, 3),
               Vertex(1, -1, 3),
               Vertex(1, 1, 3),
               Vertex(-1, -1, 5),
               Vertex(-1, 1, 5),
               Vertex(1, -1, 5),
               Vertex(1, 1, 5)]
vertex_list[0].connection_list = [vertex_list[1], vertex_list[2], vertex_list[4]]
vertex_list[3].connection_list = [vertex_list[1], vertex_list[2], vertex_list[7]]
vertex_list[6].connection_list = [vertex_list[2], vertex_list[4], vertex_list[7]]
vertex_list[5].connection_list = [vertex_list[1], vertex_list[4], vertex_list[7]]

while True:
    [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
    screen.fill((50, 50, 50))
    for i in vertex_list:
        i.draw(90 / 180 * math.pi, 1000, 0.1, 600 / 800)
        try:
            i.connect()
        except AttributeError:
            pass
    pygame.display.update()