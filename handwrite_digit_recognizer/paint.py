import pygame
import numpy as np
from settings import *


class Paint:
    def __init__(self):

        self.width, self.height = WIDTH, HEIGHT
        self.paint_surface_color = BLACK_COLOR
        self.cursor_color = WHITE_COLOR
        self.ui_color = UI_COLOR
        self.ui_width = SIDE_PANEL_WIDTH
        self.ui_font = UI_FONT
        self.radius = LINE_RADIUS
        self.clear_button_color = CLEAR_BUTTON_COLOR
        self.pressed_clear_button_color = PRESSED_CLEAR_BUTTON_COLOR

        self.prev_cursor_position = (0, 0)
        self.cursor_position = (0, 0)
        self.mouse_pressed = False
        self.clear_button_flag = False

        pygame.display.set_caption('Paint')

        self.screen = pygame.display.set_mode((self.width + self.ui_width, self.height))

        self.paint_surface = pygame.Surface((self.width, self.height))
        self.paint_surface.fill(self.paint_surface_color)

        self.info_surface = pygame.Surface((self.ui_width, self.height))
        self.info_surface.fill(self.ui_color)

        self.draw_ui_objects()

        self.clear_button = None
        self.text_clear = None

    def draw_ui_objects(self):

        self.clear_button = pygame.Rect(self.ui_width * 0.1, self.height - self.ui_width * 0.1 - 50,
                                        self.ui_width * 0.8, 50)
        if self.clear_button_flag:
            pygame.draw.rect(self.info_surface, self.clear_button_color, self.clear_button)
        else:
            pygame.draw.rect(self.info_surface, self.pressed_clear_button_color, self.clear_button)

        self.text_clear = self.ui_font.render("Clear", True, self.cursor_color)

    def draw_line(self):
        pygame.draw.circle(self.paint_surface, self.cursor_color, self.cursor_position, self.radius)

        if self.mouse_pressed:

            dx = self.cursor_position[0] - self.prev_cursor_position[0]
            dy = self.cursor_position[1] - self.prev_cursor_position[1]

            distance = max(abs(dx), abs(dy))

            for i in range(int(distance)):
                x = int(self.prev_cursor_position[0] + i / distance * dx)
                y = int(self.prev_cursor_position[1] + i / distance * dy)
                pygame.draw.circle(self.paint_surface, self.cursor_color, (x, y), self.radius)

    def update_screen(self):
        self.draw_ui_objects()

        self.screen.blit(self.paint_surface, (0, 0))

        w, h = self.text_clear.get_width(), self.text_clear.get_height()
        self.info_surface.blit(self.text_clear, (self.ui_width / 2 - w / 2,
                                                 self.height - self.ui_width * 0.11 - h))

        self.screen.blit(self.info_surface, (self.width, 0))

    def main(self):
        while True:

            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.cursor_position = event.pos
                self.draw_line()
                self.mouse_pressed = True

                if self.clear_button.collidepoint((event.pos[0] - self.width, event.pos[1])):
                    self.paint_surface.fill(self.paint_surface_color)

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False

            if event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    self.cursor_position = event.pos
                    self.draw_line()

                if self.clear_button.collidepoint((event.pos[0] - self.width, event.pos[1])):
                    self.clear_button_flag = True
                else:
                    self.clear_button_flag = False

            if event.type == pygame.QUIT:
                exit()

            self.prev_cursor_position = self.cursor_position

            #data = pygame.transform.scale(self.paint_surface, (28, 28))
            #data = pygame.surfarray.array2d(data)
            #np.savetxt('data.csv', data, delimiter=',')

            self.update_screen()
            pygame.display.flip()


if __name__ == "__main__":
    Paint().main()
