import unittest

import day12


class TestShip2(unittest.TestCase):
    def test_N5(self):
        ship = day12.Ship2((10, 1))
        ship.react("N", 5)
        self.assertEquals(ship.waypoint, (10, 6))

    def test_S5(self):
        ship = day12.Ship2((10, 1))
        ship.react("S", 5)
        self.assertEquals(ship.waypoint, (10, -4))

    def test_E5(self):
        ship = day12.Ship2((10, 1))
        ship.react("E", 5)
        self.assertEquals(ship.waypoint, (15, 1))

    def test_W5(self):
        ship = day12.Ship2((10, 1))
        ship.react("W", 5)
        self.assertEquals(ship.waypoint, (5, 1))

    def test_sample_instructions(self):
        ship = day12.Ship2((10, 1))
        ship.react("F", 10)
        ship.react("N", 3)
        ship.react("F", 7)
        ship.react("R", 90)
        ship.react("F", 11)
        self.assertEquals(ship.waypoint, (4, -10))
        self.assertEquals(ship.position, (214, -72))

    def test_rotations(self):
        test_cases = [
            ((10, 1), "R", (1, -10)),
            ((10, 1), "L", (-1, 10)),
            ((-2, 20), "R", (20, 2)),
            ((-2, 20), "L", (-20, -2)),
            ((-30, -3), "R", (-3, 30)),
            ((-30, -3), "L", (3, -30)),
            ((4, -40), "R", (-40, -4)),
            ((4, -40), "L", (40, 4)),
            ((5, 0), "R", (0, -5)),
            ((5, 0), "L", (0, 5)),
            ((0, 6), "R", (6, 0)),
            ((0, 6), "L", (-6, 0)),
            ((-7, 0), "R", (0, 7)),
            ((-7, 0), "L", (0, -7)),
            ((0, -8), "R", (-8, 0)),
            ((0, -8), "L", (8, 0)),
        ]

        for start, instruction, expected in test_cases:
            ship = day12.Ship2(start)
            ship.react(instruction, 90)
            self.assertEquals(ship.waypoint, expected)
