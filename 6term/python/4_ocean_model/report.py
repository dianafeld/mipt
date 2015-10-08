# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os
from ocean import *


def make_report(ocean, num_iters):
    report_dir = "report"
    if not os.path.isdir(report_dir):
        os.makedirs(report_dir)

    predators = []
    preys = []

    iter_num = 0
    while not is_over(iter_num, num_iters):
        iter_num += 1
        do_iteration(ocean, iter_num)
        predators.append(Predator.number)
        preys.append(Prey.number)

    if iter_num < num_iters:
        with open(os.path.join(report_dir, "report.txt"), "w", encoding="utf-8") as f:
            print("В океане никто не выжил", file=f)
            if Predator.number:
                print("Хищникам нечего есть", file=f)
            elif Prey.number:
                print("Остались только жертвы", file=f)
    else:

        ocean_height = len(ocean) - 2
        ocean_width = len(ocean[0]) - 2
        ocean_size = ocean_height * ocean_width

        with open(os.path.join(report_dir, "report.txt"), "w", encoding="utf-8") as f:
            print("Средняя доля жертв в океане: {:.2f}".
                  format(np.mean(preys) / ocean_size), file=f)
            print("Средняя доля хищников в океане: {:.2f}".
                  format(np.mean(predators) / ocean_size), file=f)
            print("Минимальное/максимальное число жертв в океане: {}/{}".
                  format(np.min(preys), np.max(preys)), file=f)
            print("Минимальное/максимальное число хищников в океане: {}/{}".
                  format(np.min(preys), np.max(predators)), file=f)

    iterations = np.arange(iter_num)
    plt.plot(iterations, predators, 'r', label="predators")
    plt.plot(iterations, preys, 'g', label='preys')

    plt.legend()
    plt.xlabel("iter_num")
    plt.ylabel("population")

    plt.savefig(os.path.join(report_dir, "population.png"))
