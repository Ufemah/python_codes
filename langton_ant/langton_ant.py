import pygame
import numpy as np
import platform

folder_symbol = '/'

if platform.system() == "Windows":
    folder_symbol = '\\'

lst = []

time_delay = 2
size = 50


def matrix(_size, _lst):
    _matrix = np.eye(_size) * 0
    for i in _lst:
        _matrix[i[0]][i[1]] += 1
    return _matrix


class Ant(object):
    def __init__(self, _size):
        self.rect = ant_img.get_rect()
        self.rect = self.rect.move(int(_size * 0.6) * white_img.get_rect().w,
                                   int(_size * 0.6) * white_img.get_rect().h)    # start point

    def first_blit(self):
        screen.blit(ant_img, self.rect)

    def blit(self, _bg, surface):
        self.rect, dx, dy = _bg.ant_move()
        _ant_img = ant_img
        if dx == 1:
            _ant_img = ant_right_img
        elif dx == -1:
            _ant_img = ant_left_img
        elif dy == 1:
            _ant_img = ant_down_img
        elif dy == -1:
            _ant_img = ant_up_img

        surface.blit(_ant_img, self.rect)

    def ant_rect(self):
        ant_center = (int((self.rect.x + self.rect.w / 2) // white_img.get_rect().w),
                      int((self.rect.y + self.rect.h / 2) // white_img.get_rect().h))
        return self.rect, ant_center

    def position(self):
        ant_center = (int((self.rect.x + self.rect.w/2) // white_img.get_rect().h),
                      int((self.rect.y + self.rect.h/2) // white_img.get_rect().h))
        return ant_center


class BackGround:
    def __init__(self, _size):
        self.rect_white = white_img.get_rect()
        self.rect_grey = grey_img.get_rect()
        self.size = _size
        self.first = True

    def blit(self, surface):
        global lst, size
        ant_center = ant.position()

        if ant_center in lst:
            lst.remove(ant_center)
        else:
            lst.append(ant_center)

        mat = matrix(self.size, lst)

        for i1 in range(self.size):
            for i2 in range(self.size):
                if mat[i1][i2] == 0:
                    surface.blit(white_img, (white_img.get_rect().h*i1, white_img.get_rect().h*i2))
                else:
                    surface.blit(grey_img, (white_img.get_rect().h*i1, white_img.get_rect().h*i2))

    def ant_move(self):
        global last_pos, lst, previous_pos
        ant_position, center = ant.ant_rect()
        mat = matrix(self.size, lst)

        dx_move = 1
        dy_move = 0

        if not self.first:
            dx = previous_pos.x - last_pos.x
            dy = previous_pos.y - last_pos.y
            if dx == 0:
                dx_move = 0
            else:
                dx_move = dx/abs(dx)

            if dy == 0:
                dy_move = 0
            else:
                dy_move = dy/abs(dy)

            if mat[center[0]][center[1]] == 1:
                if ant_position.x > 0 and ant_position.y > 0:
                    ant_position = ant.ant_rect()[0].move(dy, -dx)
                else:
                    ant_position = ant.ant_rect()[0]
            else:
                if ant_position.x > 0 and ant_position.y > 0:
                    ant_position = ant.ant_rect()[0].move(-dy, dx)
                else:
                    ant_position = ant.ant_rect()[0]
            previous_pos = last_pos
            last_pos = ant_position
        else:
            ant_position = ant.ant_rect()[0].move(0, -white_img.get_rect().h)
            self.first = False
            lst = []

        return ant_position, dx_move, dy_move


class Strips:
    def __init__(self, _size):
        self.rect_vertical = vertical_strip_img.get_rect()
        self.rect_horizontal = horizontal_strip_img.get_rect()
        self.size = _size

    def blit(self, surface):
        for i in range(self.size + 1):
            surface.blit(vertical_strip_img, self.rect_vertical.move(white_img.get_rect().h * i, 0))
            surface.blit(horizontal_strip_img, self.rect_horizontal.move(0, white_img.get_rect().w * i))


ant_img = pygame.image.load('src' + folder_symbol + 'ant_20.png')
grey_img = pygame.image.load('src' + folder_symbol + 'bg_grey_20.jpg')
white_img = pygame.image.load('src' + folder_symbol + 'bg_white_20.jpg')

ant_up_img = pygame.image.load('src' + folder_symbol + 'ant_20_up.png')
ant_down_img = pygame.image.load('src' + folder_symbol + 'ant_20_down.png')
ant_right_img = pygame.image.load('src' + folder_symbol + 'ant_20_right.png')
ant_left_img = pygame.image.load('src' + folder_symbol + 'ant_20_left.png')

vertical_strip_img = pygame.image.load('src' + folder_symbol + 'vertical_strip.jpg')
horizontal_strip_img = pygame.image.load('src' + folder_symbol + 'horizontal_strip.jpg')

window = w, h = white_img.get_rect().w * size + 1, white_img.get_rect().h * size + 1
screen = pygame.display.set_mode(window)
pygame.display.set_caption('Ant')

pygame.init()

ant = Ant(size)
bg = BackGround(size)
strips = Strips(size)

ant.first_blit()

pygame.display.update()

last_pos = ant.ant_rect()[0]
previous_pos = last_pos

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    bg.blit(screen)
    strips.blit(screen)
    ant.blit(bg, screen)

    pygame.display.update()
    pygame.time.delay(time_delay)
