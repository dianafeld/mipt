import unittest
from ocean_cells import *
from ocean import parse_ocean, OceanConfig


class TestPrey(unittest.TestCase):
    def setUp(self):
        self.ocean_config = OceanConfig(2, 2, 4, 4, 2, 1234, 0)
        self.ocean_config.initial_ocean = '''X X X X
                                            X o   X
                                            X     X
                                            X X X X'''
        self.ocean = parse_ocean(self.ocean_config)

    def test_prey_act_move(self):
        prey = self.ocean[1][1]
        prey.act()
        self.assertTrue((type(self.ocean[1][1]) is Empty) and
                        (self.ocean[1][2] == prey or self.ocean[2][1] == prey))

    def test_prey_act_reproduce(self):
        prey = self.ocean[1][1]
        prey.iters += prey.reproduction_iters
        prey.act()
        self.assertTrue(self.ocean[1][2] == prey or self.ocean[2][1] == prey)

    def test_prey_die(self):
        prey = self.ocean[1][1]
        num = Prey.number
        prey.die()
        self.assertTrue((type(self.ocean[1][1]) is Empty) and (Prey.number == (num - 1)))


class TestPred(unittest.TestCase):
    def setUp(self):
        self.ocean_config = OceanConfig(2, 2, 4, 5, 2, 1234, 0)
        self.ocean_config.initial_ocean = '''X X X X
                                            X C   X
                                            X     X
                                            X X X X'''
        self.ocean = parse_ocean(self.ocean_config)

    def test_pred_act_move(self):
        pred = self.ocean[1][1]
        pred.act()
        self.assertTrue((type(self.ocean[1][1]) is Empty) and
                        (self.ocean[1][2] == pred or self.ocean[2][1] == pred))

    def test_pred_act_reproduce(self):
        pred = self.ocean[1][1]
        pred.iters += pred.reproduction_iters
        pred.act()
        self.assertTrue(self.ocean[1][2] == pred or self.ocean[2][1] == pred)

    def test_pred_act_starve(self):
        pred = self.ocean[1][1]
        pred.iters += pred.starvation_iters
        pred.act()
        self.assertTrue((type(self.ocean[1][1]) is Empty) and
                        not (self.ocean[1][2] == pred or self.ocean[2][1] == pred))

    def test_pred_act(self):
        pred = self.ocean[1][1]
        pred.act()
        self.assertTrue((type(self.ocean[1][1]) is Empty) and
                        (self.ocean[1][2] == pred or self.ocean[2][1] == pred))

    def test_pred_die(self):
        pred = self.ocean[1][1]
        num = Predator.number
        pred.die()
        self.assertTrue((type(self.ocean[1][1]) is Empty) and (Predator.number == (num - 1)))


class TestPredEat(unittest.TestCase):
    def setUp(self):
        self.ocean_config = OceanConfig(2, 2, 4, 5, 2, 1234, 0)
        self.ocean_config.initial_ocean = '''X X X X
                                            X C o X
                                            X o   X
                                            X X X X'''
        self.ocean = parse_ocean(self.ocean_config)

    def test_pred_act_eat(self):
        pred = self.ocean[1][1]
        num = Prey.number
        pred.act()
        self.assertTrue((type(self.ocean[1][1]) is Empty) and (Prey.number == (num - 1)) and
                        (pred.last_dinner_iter == pred.iters) and
                        (self.ocean[1][2] == pred or self.ocean[2][1] == pred))


if __name__ == '__main__':
    unittest.main()
