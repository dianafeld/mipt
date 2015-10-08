import configparser
import argparse

from ocean import *
from report import *


def set_argparser():
    """Add console mode parser"""

    parser = argparse.ArgumentParser(prog="Ocean simulation")
    parser.add_argument("config_path", help="path to ocean configuration file")
    parser.add_argument("num_iters", type=int, help="number of iterations to simulate")
    parser.add_argument("--report", action="store_true",
                        help="generate report (otherwise show simulation in terminal)")

    return parser


def parse_config(config_path):
    """Parse ocean configuration file specified by config_path"""

    config = configparser.ConfigParser()
    config.read(config_path)

    seed = int(config["random"]["seed"])
    variety = float(config["random"]["variety"])

    ocean_height, ocean_width = \
        map(int, [config["ocean"]["height"], config["ocean"]["width"]])

    prey_repr_iters, predator_repr_iters, predator_starve_iters =\
        map(int, [config["prey"]["reproduction time"],
                  config["predator"]["reproduction time"],
                  config["predator"]["starvation time"]])

    ocean_config = OceanConfig(ocean_height, ocean_width,
                               predator_repr_iters, predator_starve_iters,
                               prey_repr_iters,
                               seed, variety)

    if "probabilities" in config.sections():
        ocean_config.predator_prob, ocean_config.prey_prob, ocean_config.obstacle_prob = \
            map(float, [config["probabilities"]["predator"],
                        config["probabilities"]["prey"],
                        config["probabilities"]["obstacle"]])

    else:
        ocean_config.initial_ocean = config["ocean"]["initial ocean"]

    return ocean_config


def main():
    argparser = set_argparser()
    args = argparser.parse_args()
    ocean_config = parse_config(args.config_path)

    ocean = get_initial_ocean(ocean_config)
    num_iters = args.num_iters

    if args.report:
        make_report(ocean, num_iters)
    else:
        mainloop(ocean, num_iters)


if __name__ == '__main__':
    main()
