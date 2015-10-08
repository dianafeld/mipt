import random
import math


class Empty:
    """Class for representing empty cell in the ocean"""

    def __str__(self):
        return ' '


class Obstacle:
    """Class for representing obstacle in the ocean"""

    number = 0

    def __init__(self):
        Obstacle.number += 1

    def __str__(self):
        return 'X'


def get_free_neighbour_cells(ocean, h, w, types=[Empty]):
    """Return free cells within one move

    Specify `types` parameter if you want to change "free" definition

    """

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    cells = []

    for move in moves:
        if type(ocean[h + move[0]][w + move[1]]) in types:
            cells.append((h + move[0], w + move[1]))

    return cells


def add_variety(iters, percent):
    max_variety = math.floor(percent * iters)
    return iters + random.randint(-max_variety, +max_variety)


class Predator:
    """Class for representing predator strategy in the ocean"""

    number = 0

    def __init__(self, ocean, h, w, ocean_config, birth_iter=0):
        Predator.number += 1
        self.ocean = ocean
        self.h = h
        self.w = w
        self.ocean_config = ocean_config
        self.reproduction_iters = \
            add_variety(ocean_config.predator_repr_iters, ocean_config.variety)
        self.starvation_iters = \
            add_variety(ocean_config.predator_starve_iters, ocean_config.variety)
        self.birth_iter = birth_iter
        self.last_dinner_iter = birth_iter
        self.iters = birth_iter

    def __str__(self):
        if self.iters == self.birth_iter:
            return 'c'
        else:
            return 'C'

    def act(self):
        self.iters += 1
        if (self.iters - self.birth_iter) % self.reproduction_iters == 0:
            self.reproduce()
        else:
            self.move()

        if self.iters - self.last_dinner_iter > self.starvation_iters:
            self.die()

    def reproduce(self):
        free_cells = get_free_neighbour_cells(self.ocean, self.h, self.w)
        if not free_cells:
            return
        h, w = random.choice(free_cells)
        self.ocean[h][w] = Predator(self.ocean, h, w, self.ocean_config, self.iters)

    def move(self):
        free_cells = get_free_neighbour_cells(self.ocean, self.h, self.w, types=[Empty, Prey])
        if not free_cells:
            return
        h, w = random.choice(free_cells)

        if type(self.ocean[h][w]) is Prey:
            self.eat(h, w)

        self.ocean[h][w] = self
        self.ocean[self.h][self.w] = Empty()
        self.h = h
        self.w = w

    def eat(self, h, w):
        self.ocean[h][w].die()
        self.last_dinner_iter = self.iters

    def die(self):
        self.ocean[self.h][self.w] = Empty()
        Predator.number -= 1


class Prey:
    """Class for representing prey strategy in the ocean"""

    number = 0

    def __init__(self, ocean, h, w, ocean_config, birth_iter=0):
        Prey.number += 1
        self.ocean = ocean
        self.h = h
        self.w = w
        self.ocean_config = ocean_config
        self.reproduction_iters = add_variety(ocean_config.prey_repr_iters, ocean_config.variety)
        self.birth_iter = birth_iter
        self.iters = birth_iter

    def __str__(self):
        if self.iters == self.birth_iter:
            return '.'
        else:
            return 'o'

    def act(self):
        self.iters += 1
        if (self.iters - self.birth_iter) % self.reproduction_iters == 0:
            self.reproduce()
        else:
            self.move()

    def reproduce(self):
        free_cells = get_free_neighbour_cells(self.ocean, self.h, self.w)
        if not free_cells:
            return
        h, w = random.choice(free_cells)
        self.ocean[h][w] = Prey(self.ocean, h, w, self.ocean_config, self.iters)

    def move(self):
        free_cells = get_free_neighbour_cells(self.ocean, self.h, self.w)
        if not free_cells:
            return
        h, w = random.choice(free_cells)
        self.ocean[h][w] = self
        self.ocean[self.h][self.w] = Empty()
        self.h = h
        self.w = w

    def die(self):
        self.ocean[self.h][self.w] = Empty()
        Prey.number -= 1
