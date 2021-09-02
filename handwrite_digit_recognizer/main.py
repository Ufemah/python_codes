import pygame
import numpy as np

from settings import *
from model_predicting import Model


class Paint:
    def __init__(self):

        # init CNN model
        self.model = Model()

        # init prediction results as zeros
        self.model_result = np.zeros(10)

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
        self.iter_count = ITERATION_STEPS_FOR_PREDICTING

        # init values
        self.prev_cursor_position = (0, 0)
        self.cursor_position = (0, 0)
        self.mouse_pressed = False
        self.reset_button_flag_collided = False
        self.reset_button_flag_pressed = False

        # init flags for stopping "I'm loading" animation
        self.init_passed_flag1 = False
        self.init_passed_flag2 = False

        # init screen
        pygame.display.set_caption('Paint')
        self.screen = pygame.display.set_mode((self.width + self.ui_width, self.height))

        # init surfaces
        self.paint_surface = pygame.Surface((self.width, self.height))
        self.paint_surface.fill(self.paint_surface_color)

        self.info_surface = pygame.Surface((self.ui_width, self.height))
        self.info_surface.fill(self.ui_color)

        # init dicts for numbers at right panel
        self.numbers = {}
        self.number_labels = {}

        # draw right panel gui elements
        self.draw_ui_objects()

        # init reset button vars
        self.reset_button = None
        self.text_reset = None

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

        # draw line between cursor points
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

        # fill screen with black color
        self.screen.fill(self.paint_surface_color)

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

    def loading_screensaver(self):
        # fill paint_surface
        pygame.draw.rect(self.paint_surface, self.paint_surface_color, (0, 0, self.width, self.height))

        # init and render "I'm loading" text
        loading_text = self.ui_font.render("I am loading", True, WHITE_COLOR)
        w, h = loading_text.get_width(), loading_text.get_height()
        self.paint_surface.blit(loading_text, (self.width / 2 - w / 2, self.height / 2 - h / 2))

    def main(self):

        steps = self.iter_count - 3  # var for making prediction every 25 iteration step

        running = True  # var for stopping iteration

        while running:
            if not self.init_passed_flag1:
                steps += 1

            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                steps += 1

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

            # watch mouse movement, when mouse button is pressed
            if event.type == pygame.MOUSEMOTION:

                # draw line between prev and current cursor positions
                if self.mouse_pressed:
                    steps += 1
                    self.cursor_position = event.pos
                    self.draw_line()

                # change button flag to change color if cursor collides with button
                if self.reset_button.collidepoint((event.pos[0] - self.width, event.pos[1])):
                    self.reset_button_flag_collided = True
                else:
                    self.reset_button_flag_collided = False

            # stop drawing line if mouse button is up
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                self.reset_button_flag_pressed = False

            # update prev cursor color
            self.prev_cursor_position = self.cursor_position

            # if screen is empty -> model_result = zeros
            if np.equal(pygame.surfarray.array2d(self.paint_surface), np.zeros((800, 800))).all():
                self.model_result = np.zeros(10) + 0.01

            # every N iteration steps make prediction with CNN model
            if steps % self.iter_count == 0:

                steps = 0

                matrix = pygame.transform.scale(self.paint_surface, (28, 28))  # scale paint surface: 800x800 -> 28x28
                matrix = pygame.surfarray.array2d(matrix)   # make matrix from surface

                matrix = np.where(matrix < -1, 0, np.abs(matrix / 16777215)).T  # process matrix

                # if screen is empty -> don't update model_result
                if not np.equal(matrix, np.zeros((28, 28))).all():
                    self.model_result = self.model.predict(matrix)  # make prediction and get result
                    self.model_result += 0.01  # +0.01 for info_panel
                self.init_passed_flag1 = True  # flag to stop "I'm loading" animation

            self.update_screen()

            # if model initialized
            if self.init_passed_flag1:
                if not self.init_passed_flag2:
                    # fill paint_surface if model has just been initialized
                    self.paint_surface.fill(self.paint_surface_color)
                    self.init_passed_flag2 = True
                pygame.display.update()

            # if model is not initialized -> show "I'm loading"
            else:
                self.loading_screensaver()
                pygame.display.update()


if __name__ == "__main__":
    Paint().main()
