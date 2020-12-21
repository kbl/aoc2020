import ioaoc


test_input = """F10
N3
F7
R90
F11"""


def parse(lines):
    return [(line[0], int(line[1:])) for line in lines]


class Ship:
    MOVES = {
        "N": (0, 1),
        "S": (0, -1),
        "E": (1, 0),
        "W": (-1, 0),
    }
    ROTATIONS = {
        "N": {
            "L": "W",
            "R": "E",
        },
        "S": {
            "L": "E",
            "R": "W",
        },
        "E": {
            "L": "N",
            "R": "S",
        },
        "W": {
            "L": "S",
            "R": "N",
        },
    }

    def __init__(self):
        self.orientation = "E"
        self.position = (0, 0)

    def react(self, instruction, operand):
        if instruction in ("L", "R"):
            for _ in range(operand // 90):
                self.orientation = Ship.ROTATIONS[self.orientation][instruction]
            return

        direction = instruction
        if instruction == "F":
            direction = self.orientation

        move_x, move_y = Ship.MOVES[direction]
        for _ in range(operand):
            x, y = self.position
            self.position = (x + move_x, y + move_y)


class Ship2:
    WAYPOINT_MOVES = {
        "N": (0, 1),
        "S": (0, -1),
        "E": (1, 0),
        "W": (-1, 0),
    }

    ROTATION_MULTIPLIERS = {
        "L": (-1, 1),
        "R": (1, -1),
    }

    def __init__(self, waypoint):
        self.position = (0, 0)
        self.waypoint = waypoint

    def react(self, instruction, operand):
        if instruction in Ship2.WAYPOINT_MOVES:
            move_x, move_y = Ship2.WAYPOINT_MOVES[instruction]
            x, y = self.waypoint
            self.waypoint = (x + move_x * operand, y + move_y * operand)
            return

        if instruction == "F":
            position_x, position_y = self.position
            waypoint_x, waypoint_y = self.waypoint
            self.position = (position_x + waypoint_x * operand, position_y + waypoint_y * operand)
            return

        multiplier_x, multiplier_y = Ship2.ROTATION_MULTIPLIERS[instruction]
        for _ in range(operand // 90):
            waypoint_x, waypoint_y = self.waypoint
            self.waypoint = (waypoint_y * multiplier_x, waypoint_x * multiplier_y)


def manhattan_distance(position):
    x, y = position
    return abs(x) + abs(y)
            

if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day12_input.txt")
    instructions = parse(lines)

    ship = Ship()
    for instruction, operand in instructions:
        ship.react(instruction, operand)

    print(">", manhattan_distance(ship.position))

    ship = Ship2((10, 1))
    for instruction, operand in instructions:
        ship.react(instruction, operand)

    print(">>", manhattan_distance(ship.position))
