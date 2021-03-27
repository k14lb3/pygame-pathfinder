import pygame
import math

# Initialize
pygame.init()

# Global Variables
win_width = 500
win_height = 600
rows = 20

# Mouse
mouse_position_x = 0
mouse_position_y = 0

# Title and Icon
pygame.display.set_caption("Pathfinder")

# Create screen
win = pygame.display.set_mode((win_width, win_height))
win_tab_img = pygame.image.load('src/images/window.png')
win_tab_x = 0
win_tab_y = win_height - win_tab_img.get_height()
background_img = pygame.image.load('src/images/background.png')


class Actor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_loc(self):
        return [self.x, self.y]


class Button(Actor):
    def __init__(self, x, y, img, processing_img, reset_img, state, function):
        super().__init__(x, y)
        self.img = img
        self.width = img[0].get_width()
        self.height = img[0].get_height()
        self.processing_img = processing_img
        self.reset_img = reset_img
        self.state = state
        self.state_timer = 0
        self.function = function

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def show(self):
        if not self.state:
            win.blit(self.img[0], (self.x, self.y))
        elif not self.function.get_state():
            self.state_timer = 0
            win.blit(self.reset_img[0], (self.x, self.y))
        elif self.function.get_state():
            if self.state_timer % 2 == 0:
                win.blit(self.processing_img[1], (self.x, self.y))
            else:
                win.blit(self.processing_img[0], (self.x, self.y))
            self.state_timer += 1

    def interact(self, point_start):

        mouse_click = pygame.mouse.get_pressed()

        if self.x <= mouse_position_x <= self.x + self.width and \
                self.y <= mouse_position_y <= self.y + self.height:

            if not self.state:
                win.blit(self.img[1], (self.x, self.y))
                if mouse_click[0]:
                    self.state = True
                    self.function.set_state(True)
                    self.function.set_path_start([point_start.get_x(), point_start.get_y()])
                    for n in range(4):
                        self.function.append(n, self.function.get_path_start())
                    self.function.add_loc_count(1)
                    for n in range(1000):
                        for m in range(1000):
                            pass
            elif not self.function.get_state():
                win.blit(self.reset_img[1], (self.x, self.y))
                if mouse_click[0]:
                    self.state = False
                    self.function.reset()
                    for n in range(2000):
                        for m in range(2000):
                            pass

    def action(self, point_end):
        self.function.display(point_end)

    def display(self, point_start):
        self.show()
        self.interact(point_start)


class Point(Actor):
    point_size = 25

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.color = color
        self.click_x = None
        self.click_y = None
        self.drag = False

    @classmethod
    def get_size(cls):
        return cls.point_size

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_drag(self):
        return self.drag

    def show(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, Point.get_size(), Point.get_size()))

    def interact(self, point, button_start):

        if not button_start.state:
            mouse_click = pygame.mouse.get_pressed()

            if self.x <= mouse_position_x <= self.x + Point.get_size() and \
                    self.y <= mouse_position_y <= self.y + Point.get_size():
                if not point.get_drag():
                    if mouse_click[0]:
                        self.drag = True
                    if not mouse_click[0]:
                        self.drag = False

    def move(self, point):
        if mouse_position_y < win_height - win_tab_img.get_height():
            if self.drag:
                if mouse_position_x > self.x + Point.get_size():
                    if (self.x + Point.get_size() != point.get_x() and self.y == point.get_y()) or \
                            self.y < point.get_y() or self.y > point.get_y():
                        self.x += Point.get_size()
                if mouse_position_x < self.x:
                    if (self.x - Point.get_size() != point.get_x() and self.y == point.get_y()) or \
                            self.y < point.get_y() or self.y > point.get_y():
                        self.x += -Point.get_size()
                if mouse_position_y > self.y + Point.get_size():
                    if (self.x < point.get_x() or self.x > point.get_x()) or \
                            (self.y + Point.get_size() != point.get_y() and self.x == point.get_x()):
                        self.y += Point.get_size()
                if mouse_position_y < self.y:
                    if (self.x < point.get_x() or self.x > point.get_x()) or \
                            (self.y - Point.get_size() != point.get_y() and self.x == point.get_x()):
                        self.y += -Point.get_size()

    def display(self, point, button_start):
        self.show()
        self.interact(point, button_start)
        self.move(point)


class Pencil(Actor):
    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.color = color
        self.loc = []

    def show(self):

        for n in range(len(self.loc)):
            pygame.draw.rect(win, self.color, (self.loc[n][0], self.loc[n][1],
                                               Point.get_size(), Point.get_size()))

    def draw(self):

        mouse = pygame.mouse.get_pressed()

        if mouse[2]:
            x = mouse_position_x
            y = mouse_position_y

            while x % Point.get_size() != 0:
                x -= 1
            while y % Point.get_size() != 0:
                y -= 1

            self.loc.append([x, y])

    def display(self):
        self.draw()
        self.show()


class Pathfinder:
    def __init__(self):
        self.search_state = False
        self.search_visible = True
        self.loc = [[], [], [], [],
                    [], [], [], []]
        self.loc_count = -1
        self.rep = 1
        self.path = []
        self.path_state = False
        self.path_start = None
        self.path_end = None

    def get_state(self):
        return self.search_state

    def get_path_start(self):
        return self.path_start

    def get_path_state(self):
        return self.path_state

    def set_state(self, state):
        self.search_state = state

    def set_path_start(self, path_start):
        self.path_start = path_start

    def add_loc_count(self, x):
        self.loc_count += x

    def reset(self):
        for n in range(len(self.loc)):
            self.loc[n].clear()
        self.path.clear()
        self.rep = 1
        self.loc_count = -1

    def append(self, n, x):
        self.loc[n].append(x)

    def search_sides(self):

        x = 0
        y = 0

        for n in range(4):

            # Top - x = stay, y = decrement
            if n == 0:
                x = 0
                y = - Point.get_size()
            # Right - x = increment, y = stay
            if n == 1:
                x = Point.get_size()
                y = 0
            # Bottom - x = stay y = increment
            if n == 2:
                x = 0
                y = + Point.get_size()
            # Left - x = decrement, y = stay
            if n == 3:
                x = - Point.get_size()
                y = 0

            self.loc[n].append([self.loc[n][self.loc_count][0] + x,
                                self.loc[n][self.loc_count][1] + y])

    def search_edges(self):

        for n in range(4):

            x = 0
            y = 0

            if n == 0:
                x = Point.get_size()
                y = 0
            if n == 1:
                x = 0
                y = Point.get_size()
            if n == 2:
                x = -Point.get_size()
                y = 0
            if n == 3:
                x = 0
                y = -Point.get_size()

            for m in range(self.rep):
                self.loc[n + 4].append([self.loc[n][self.loc_count][0] + x,
                                        self.loc[n][self.loc_count][1] + y])

                if n == 0:
                    x += Point.get_size()
                    y += Point.get_size()
                if n == 1:
                    x += -Point.get_size()
                    y += Point.get_size()
                if n == 2:
                    x += -Point.get_size()
                    y += -Point.get_size()
                if n == 3:
                    x += Point.get_size()
                    y += -Point.get_size()

        self.rep += 1

    def search(self):

        if self.search_state:

            self.search_sides()

            self.search_edges()

            self.loc_count += 1

            if self.search_visible:
                for a in range(1000):
                    for b in range(5000):
                        pass

    def check(self, point_end):

        for n in range(len(self.loc)):
            for m in range(len(self.loc[n])):

                if m == len(self.loc[n]) - 1 or \
                        m > (len(self.loc[n]) - self.rep):

                    if self.loc[n][m] == point_end.get_loc():
                        self.path_end = self.loc[n][m]
                        if self.search_state:
                            self.path_state = True
                        self.search_state = False

                    color = (177, 32, 41)

                else:
                    color = (1, 132, 64)
                if self.search_visible:
                    pygame.draw.rect(win, color,
                                     (self.loc[n][m][0], self.loc[n][m][1],
                                      Point.get_size(), Point.get_size()))

    def create_path(self):
        if self.path_state:

            a = (self.path_start[0] - self.path_end[0])/25
            b = (self.path_start[1] - self.path_end[1])/25

            x = 0
            y = 0
            count = -1

            for n in range(abs(int(a))):
                if a < 0:
                    x += Point.get_size()
                else:
                    x += -Point.get_size()
                self.path.append([self.path_start[0] + x, self.path_start[1]])
                count += 1

            for n in range(abs(int(b))):
                if b < 0:
                    y += Point.get_size()
                else:
                    y += -Point.get_size()
                self.path.append([self.path[count][0], self.path_start[1] + y])

            self.path_state = False

    def show_path(self):

        for n in range(len(self.path)):
            pygame.draw.rect(win, (205, 127, 158),
                             (self.path[n][0], self.path[n][1],
                              Point.get_size(), Point.get_size()))

    def process(self, point_end):
        self.search()
        self.create_path()
        self.check(point_end)
        self.show_path()

    def display(self, point_end):
        self.process(point_end)


def draw_grid():
    # Top
    pygame.draw.line(win, (0, 0, 0), (0, 0), (win_width, 0))
    # Left
    pygame.draw.line(win, (0, 0, 0), (0, 0), (0, win_height - win_tab_img.get_height()))
    # Right
    pygame.draw.line(win, (0, 0, 0), (win_width - 1, 0), (win_width - 1, win_height - win_tab_img.get_height()))
    grid_size = win_width // rows
    x = 0
    y = 0

    for l in range(rows):
        x = x + grid_size
        y = y + grid_size

        pygame.draw.line(win, (0, 0, 0), (x, 0), (x, win_width))
        pygame.draw.line(win, (0, 0, 0), (0, y), (win_width, y))


def display_tools(button_start, point_start, point_end):
    button_start.action(point_end)
    win.blit(win_tab_img, (win_tab_x, win_tab_y))
    button_start.display(point_start)


def redraw_window(pencil, button_start, point_start, point_end):
    win.blit(background_img, (0, 0))
    pencil.display()
    display_tools(button_start, point_start, point_end)
    point_start.display(point_end, button_start)
    point_end.display(point_start, button_start)
    draw_grid()
    pygame.display.update()


def main():
    global mouse_position_x, mouse_position_y

    running = True
    clock = pygame.time.Clock()

    path_find = Pathfinder()
    pencil = Pencil(None, None, (33, 33, 33))
    button_start = Button(200, win_tab_y + 25,
                          [pygame.image.load('src/images/button/start/button_start.png'),
                           pygame.image.load('src/images/button/start/button_start_highlighted.png')],
                          [pygame.image.load('src/images/button/start/button_start_processing_0.png'),
                           pygame.image.load('src/images/button/start/button_start_processing_1.png')],
                          [pygame.image.load('src/images/button/start/button_start_reset.png'),
                           pygame.image.load('src/images/button/start/button_start_reset_highlight.png')],
                          False, path_find)

    point_start = Point(150, 150, (177, 32, 41))
    point_end = Point(win_width - 200 - Point.get_size(),
                      win_height - win_tab_img.get_height() - 200 - Point.get_size(),
                      (41, 32, 177))

    while running:

        clock.tick(60)

        mouse_position = pygame.mouse.get_pos()
        mouse_position_x = mouse_position[0]
        mouse_position_y = mouse_position[1]

        redraw_window(pencil, button_start, point_start, point_end)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


main()
