import pygame
import numpy as np
from settings import *


class Paint:
    def __init__(self):

        # init constants
        self.width, self.height = WIDTH, HEIGHT
        self.paint_surface_color = BLACK_COLOR
        self.cursor_color = WHITE_COLOR
        self.ui_color = UI_COLOR
        self.ui_width = SIDE_PANEL_WIDTH
        self.ui_font = UI_FONT
        self.radius = LINE_WIDTH
        self.reset_button_color = RESET_BUTTON_COLOR
        self.collided_reset_button_color = COLLIDED_BUTTON_COLOR
        self.pressed_reset_button_color = PRESSED_RESET_BUTTON_COLOR

        self.prev_cursor_position = (0, 0)
        self.cursor_position = (0, 0)
        self.mouse_pressed = False
        self.reset_button_flag_collided = False
        self.reset_button_flag_pressed = False

        pygame.display.set_caption('Paint')

        self.screen = pygame.display.set_mode((self.width + self.ui_width, self.height))

        self.paint_surface = pygame.Surface((self.width, self.height))
        self.paint_surface.fill(self.paint_surface_color)

        self.info_surface = pygame.Surface((self.ui_width, self.height))
        self.info_surface.fill(self.ui_color)

        self.model_result = np.array([0.01779976,  0.14165316,  0.01029262,  0.168136,    0.03061161,
                                      0.09046587, 0.19987289,  0.13398581,  0.03119906,  0.17598322])

        self.numbers = {}
        self.number_labels = {}

        self.draw_ui_objects()

        self.reset_button = None
        self.text_reset = None
        self.result = None

    def draw_ui_objects(self):

        # init and draw right panel background
        ui_part = pygame.Rect(0, 0, self.ui_width, self.height)
        pygame.draw.rect(self.info_surface, self.ui_color, ui_part)

        # init reset_button rect
        self.reset_button = pygame.Rect(self.ui_width * 0.1, self.height - self.ui_width * 0.1 - 50,
                                        self.ui_width * 0.8, 50)
        # draw reset_button rect
        if not self.reset_button_flag_collided:
            pygame.draw.rect(self.info_surface, self.reset_button_color, self.reset_button)
        elif self.reset_button_flag_pressed:
            pygame.draw.rect(self.info_surface, self.pressed_reset_button_color, self.reset_button)
        else:
            pygame.draw.rect(self.info_surface, self.collided_reset_button_color, self.reset_button)

        # render reset_button text
        self.text_reset = self.ui_font.render("Clear", True, WHITE_COLOR)

        # render numbers at right panel
        for i in range(10):
            self.numbers[i] = self.ui_font.render(str(i), True, WHITE_COLOR)

        # init and render digit labels
        for i in range(10):
            label_rect = pygame.Rect(self.ui_width * 0.25, self.height * i / 12 + self.ui_width * 0.11,
                                     self.ui_width * 0.6 * self.model_result[i],  self.height * 0.01)
            if i == np.argmax(self.model_result):
                pygame.draw.rect(self.info_surface, GREEN_COLOR, label_rect)
            else:
                pygame.draw.rect(self.info_surface, BLACK_COLOR, label_rect)

    def draw_line(self):
        # create circle at click point
        pygame.draw.circle(self.paint_surface, self.cursor_color, self.cursor_position, self.radius)

        if self.mouse_pressed:

            # get different on 0X and 0Y axis
            dx = self.cursor_position[0] - self.prev_cursor_position[0]
            dy = self.cursor_position[1] - self.prev_cursor_position[1]

            distance = max(abs(dx), abs(dy))

            # draw rectangle from prev to next point
            for i in range(int(distance)):
                x = int(self.prev_cursor_position[0] + i / distance * dx)
                y = int(self.prev_cursor_position[1] + i / distance * dy)
                pygame.draw.circle(self.paint_surface, self.cursor_color, (x, y), self.radius)

    def update_screen(self):

        # blit paint surface
        self.screen.blit(self.paint_surface, (0, 0))

        # draw right side panel
        self.draw_ui_objects()

        # render reset button text
        w, h = self.text_reset.get_width(), self.text_reset.get_height()
        self.info_surface.blit(self.text_reset, (self.ui_width / 2 - w / 2,
                                                 self.height - self.ui_width * 0.11 - h))
        # render right panel digits
        for i in range(10):
            self.info_surface.blit(self.numbers[i], (self.ui_width * 0.1,
                                                     self.height * i / 12 + self.ui_width * 0.05))
        # blit right panel
        self.screen.blit(self.info_surface, (self.width, 0))

    def main(self):

        temp = 0

        while True:

            temp += 1
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # process RMB and LMB click
                if event.button == 1:
                    self.cursor_color = WHITE_COLOR
                elif event.button == 3:
                    self.cursor_color = BLACK_COLOR

                # draw line between prev and next cursor positions
                self.cursor_position = event.pos
                self.draw_line()
                self.mouse_pressed = True

                # reset paint surface if reset button clicked
                if self.reset_button.collidepoint((event.pos[0] - self.width, event.pos[1])):
                    self.reset_button_flag_pressed = True
                    self.paint_surface.fill(self.paint_surface_color)

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                self.reset_button_flag_pressed = False

            if event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    self.cursor_position = event.pos
                    self.draw_line()

                if self.reset_button.collidepoint((event.pos[0] - self.width, event.pos[1])):
                    self.reset_button_flag_collided = True
                else:
                    self.reset_button_flag_collided = False

            if event.type == pygame.QUIT:
                exit()

            self.prev_cursor_position = self.cursor_position

            # data = pygame.transform.scale(self.paint_surface, (28, 28))
            # data = pygame.surfarray.array2d(data) / 16777215
            # np.savetxt('data.csv', data, delimiter=',')

            self.update_screen()
            pygame.display.update()

            # temp part for testing
            if temp % 10 == 0:
                self.model_result = np.random.random(10)
                self.model_result = self.model_result / np.sum(self.model_result)


if __name__ == "__main__":
    Paint().main()
