# libraries
import pygame
import random


class Circle:

    """
    This is our simple Circle class
    """
    # color and radius globals
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    RADIUS = 50

    def __init__(self, circle_number, x, y):
        self.color = self.WHITE
        self.radius = self.RADIUS
        self.circle_number = circle_number
        self.x = x
        self.y = y
        self.previous_color = self.WHITE

    # randomly assigns a color to a circle
    def change_color(self, num_yellow):
        self.previous_color = self.color

        if num_yellow == 0 and self.previous_color != self.YELLOW:
            color_int = random.randint(1, 3)
        else:  # if there is already a yellow circle, then do not change to a yellow circle
            color_int = random.randint(1, 2)

        if color_int == 1:
            self.color = self.WHITE
        elif color_int == 2:
            self.color = self.RED
        else:
            self.color = self.YELLOW


class ClassicCornersTest:

    FPS = 30
    RECT_COLOR = (255, 255, 255)
    TOTAL_CIRCLES = 4
    PIXELS_BETWEEN_CIRCLES = 100
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH = SCREEN.get_width()
    HEIGHT = SCREEN.get_height()
    TIME_INTERVAL = 1  # seconds
    MAX_ITER = 60 * 15   # 15 minute test

    def __init__(self):
        pygame.init()

        # Set up screen
        self.screen = self.SCREEN
        self.central_line = pygame.Rect(self.WIDTH/2, 0, 1, self.HEIGHT)

        # Create list of circles
        self.circles = []

        self.total_iter = -1  # starts at -1 to account for all white circles for first iterations

        # Initialize scores
        self.total_yellows = 0
        self.yellows_correctly_clicked = 0
        self.incorrectly_clicked = 0
        self.click_in_interval = False

        # Creates 4 circles
        circle_num = 1
        while circle_num <= self.TOTAL_CIRCLES:
            if circle_num == 1:
                self.circles.append(Circle(circle_num, self.WIDTH / 4 - self.PIXELS_BETWEEN_CIRCLES,
                                           self.HEIGHT / 2 - self.PIXELS_BETWEEN_CIRCLES))
            elif circle_num == 2:
                self.circles.append(Circle(circle_num, self.WIDTH / 4 + self.PIXELS_BETWEEN_CIRCLES,
                                           self.HEIGHT / 2 - self.PIXELS_BETWEEN_CIRCLES))
            elif circle_num == 3:
                self.circles.append(Circle(circle_num, self.WIDTH / 4 - self.PIXELS_BETWEEN_CIRCLES,
                                           self.HEIGHT / 2 + self.PIXELS_BETWEEN_CIRCLES))
            else:
                self.circles.append(Circle(circle_num, self.WIDTH / 4 + self.PIXELS_BETWEEN_CIRCLES,
                                           self.HEIGHT / 2 + self.PIXELS_BETWEEN_CIRCLES))
            circle_num += 1

        self.clock = pygame.time.Clock()
        self.int_elapsed_time = 0  # ms

    def change_circle_colors(self):
        num_yellow_circles = 0
        random.shuffle(self.circles)  # shuffles the order in which the colors are changed
        for circle in self.circles:
            circle.change_color(num_yellow_circles)
            if circle.color == (255, 255, 0):
                num_yellow_circles += 1
                self.total_yellows += 1  # adds to the total yellow scores

    # Main loop
    def game_loop(self):
        while True:
            if self.total_iter == self.MAX_ITER and self.int_elapsed_time >= self.TIME_INTERVAL*1000:
                return

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and self.click_in_interval is False:
                    if self.screen.get_at(pygame.mouse.get_pos()) == (255, 255, 0):
                        self.yellows_correctly_clicked += 1
                    else:
                        self.incorrectly_clicked += 1
                    self.click_in_interval = True

            if self.int_elapsed_time >= self.TIME_INTERVAL*1000:
                self.total_iter += 1
                self.change_circle_colors()
                for circle in self.circles:
                    pygame.draw.circle(self.screen, circle.color, (circle.x, circle.y), circle.radius)
                self.int_elapsed_time = 0
                self.click_in_interval = False

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, self.RECT_COLOR, self.central_line)
            for circle in self.circles:
                pygame.draw.circle(self.screen, circle.color, (circle.x, circle.y), circle.radius)

            pygame.display.update()

            dt = self.clock.tick(self.FPS)
            self.int_elapsed_time += dt


cct = ClassicCornersTest()
cct.game_loop()
print("Total Iterations: %d " % cct.total_iter)
print("Total Yellow Circles: %d" % cct.total_yellows)
print("Total Correctly Clicked Circles: %d" % cct.yellows_correctly_clicked)
print("Total Incorrectly Clicked Circles: %d" % cct.incorrectly_clicked)
