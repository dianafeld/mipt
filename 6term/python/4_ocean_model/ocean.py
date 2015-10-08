import random
import os
import time

from ocean_cells import *


class OceanConfig:
    """Class for storing all configuration values"""

    def __init__(self, height, width, predator_repr_iters, predator_starve_iters,
                 prey_repr_iters, seed, variety):
        self.height = height
        self.width = width

        self.predator_repr_iters = predator_repr_iters
        self.predator_starve_iters = predator_starve_iters
        self.prey_repr_iters = prey_repr_iters

        self.seed = seed
        self.variety = variety


def generate_cell(ocean, h, w, ocean_config):
    """Choose what to place to the given cell based on the generation probabilities"""

    r = random.random()
    if r < ocean_config.predator_prob:
        return Predator(ocean, h, w, ocean_config)
    elif r < ocean_config.predator_prob + ocean_config.prey_prob:
        return Prey(ocean, h, w, ocean_config)
    elif r < ocean_config.predator_prob + ocean_config.prey_prob + ocean_config.obstacle_prob:
        return Obstacle()
    else:
        return Empty()


def parse_ocean(ocean_config):
    """Parse initial ocean config string"""

    ocean_list = list(map(lambda x: x.strip()[::2], ocean_config.initial_ocean.split('\n')))
    ocean = [[None] * (len(ocean_list[0])) for _ in range(len(ocean_list))]
    for h, line in enumerate(ocean_list):
        for w, cell in enumerate(line):
            if cell == 'X':
                ocean[h][w] = Obstacle()
            elif cell in 'Cc':
                ocean[h][w] = Predator(ocean, h, w, ocean_config)
            elif cell in 'o.':
                ocean[h][w] = Prey(ocean, h, w, ocean_config)
            else:
                ocean[h][w] = Empty()

    return ocean


def generate_initial_ocean(ocean_config):
    """Generate ocean array based on the generation probabilities"""

    ocean = [[None] * (ocean_config.width + 2) for _ in range(ocean_config.height + 2)]
    for h in range(ocean_config.height + 2):
        for w in range(ocean_config.width + 2):
            if (h == 0 or h == ocean_config.height + 1 or
                    w == 0 or w == ocean_config.width + 1):
                ocean[h][w] = Obstacle()
            else:
                ocean[h][w] = generate_cell(ocean, h, w, ocean_config)

    return ocean


def get_initial_ocean(ocean_config):
    """Return initial ocean based on the ocean configuration"""

    random.seed(ocean_config.seed)

    if hasattr(ocean_config, "initial_ocean"):
        return parse_ocean(ocean_config)
    else:
        return generate_initial_ocean(ocean_config)


def is_over(iter_num, num_iters):
    """Check if ocean simulation should be stopped"""

    return iter_num >= num_iters or Predator.number == 0 or Prey.number == 0


def do_iteration(ocean, iter_num):
    """Do one iteration of ocean simulation"""

    for line in ocean:
        for cell in line:
            if type(cell) is Prey or type(cell) is Predator:
                if cell.iters < iter_num:
                    cell.act()


def print_ocean(ocean):
    """Visualize ocean"""

    os.system('cls' if os.name == 'nt' else 'clear')
    for line in ocean:
        print(' '.join(map(str, line)))
    time.sleep(0.5)


def mainloop(ocean, num_iters):
    iter_num = 0
    print_ocean(ocean)
    while not is_over(iter_num, num_iters):
        iter_num += 1
        do_iteration(ocean, iter_num)
        print_ocean(ocean)
