import ioaoc


test_input = """.#.
..#
###"""

class Space:
    def __init__(self, lines=None, space=None):
        if space is None:
            space = Space.parse(lines)
        self.space = space
        min_coordinate, max_coordinate = self.find_boundaries()

    def active_adjacent(self, coordinates):
        x, y, z = coordinates
        diffs = (-1, 0, 1)
        for diff_x in diffs:
            for diff_y in diffs:
                for diff_z in diffs:
                    if (diff_x, diff_y, diff_z) == (0, 0, 0):
                        continue

                    new_coordinates = (x + diff_x, y + diff_y, z + diff_z)

                    if new_coordinates in self.space:
                        yield new_coordinates

    @staticmethod
    def parse(lines):
        z = 0
        space = set()
        for y, row in enumerate(lines):
            for x, cell in enumerate(row):
                if cell == ACTIVE:
                    space.add((x, y, z))
        return space
    
    def find_boundaries(self):
        min_coordinate = None
        max_coordinate = None

        for coordinates in self.space:
            if min_coordinate is None:
                min_coordinate = min(coordinates)
                max_coordinate = max(coordinates)
                continue

            if min(coordinates) < min_coordinate:
                min_coordinate = min(coordinates)

            if max(coordinates) > max_coordinate:
                max_coordinate = max(coordinates)

        return min_coordinate, max_coordinate

    def __str__(self):
        min, max = self.find_boundaries()
        rows = []
        for z in range(min, max+1):
            rows.append(f"z={z}")
            for y in range(min, max+1):
                row = []
                for x in range(min, max+1):
                    state = INACTIVE
                    if (x, y, z) in self.space:
                        state = ACTIVE

                    row.append(state)
                rows.append("".join(row))
        return "\n".join(rows)

    def tick(self):
        new_space = {}

        min, max = self.find_boundaries()

        min -= 1
        max += 1

        for x in range(min, max+1):
            for y in range(min, max+1):
                for z in range(min, max+1):
                    coordinates = (x, y, z)
                    active_adjacent_count = len(list(self.active_adjacent(coordinates)))

                    if coordinates in self.space:
                        if active_adjacent_count in (2, 3):
                            new_space[coordinates] = ACTIVE
                    else:
                        if active_adjacent_count == 3:
                            new_space[coordinates] = ACTIVE
        return Space(space=new_space)


class Space2:
    def __init__(self, lines=None, space=None):
        if space is None:
            space = Space2.parse(lines)
        self.space = space
        min_coordinate, max_coordinate = self.find_boundaries()

    def active_adjacent(self, coordinates):
        x, y, z, w = coordinates
        diffs = (-1, 0, 1)
        for diff_x in diffs:
            for diff_y in diffs:
                for diff_z in diffs:
                    for diff_w in diffs:
                        if (diff_x, diff_y, diff_z, diff_w) == (0, 0, 0, 0):
                            continue

                        new_coordinates = (x + diff_x, y + diff_y, z + diff_z, w + diff_w)

                        if new_coordinates in self.space:
                            yield new_coordinates

    @staticmethod
    def parse(lines):
        z = 0
        w = 0
        space = set()
        for y, row in enumerate(lines):
            for x, cell in enumerate(row):
                if cell == ACTIVE:
                    space.add((x, y, z, w))
        return space
    
    def find_boundaries(self):
        min_coordinate = None
        max_coordinate = None

        for coordinates in self.space:
            if min_coordinate is None:
                min_coordinate = min(coordinates)
                max_coordinate = max(coordinates)
                continue

            if min(coordinates) < min_coordinate:
                min_coordinate = min(coordinates)

            if max(coordinates) > max_coordinate:
                max_coordinate = max(coordinates)

        return min_coordinate, max_coordinate

    def tick(self):
        new_space = {}

        min, max = self.find_boundaries()

        min -= 1
        max += 1

        for x in range(min, max+1):
            for y in range(min, max+1):
                for z in range(min, max+1):
                    for w in range(min, max+1):
                        coordinates = (x, y, z, w)
                        active_adjacent_count = len(list(self.active_adjacent(coordinates)))

                        if coordinates in self.space:
                            if active_adjacent_count in (2, 3):
                                new_space[coordinates] = ACTIVE
                        else:
                            if active_adjacent_count == 3:
                                new_space[coordinates] = ACTIVE
        return Space2(space=new_space)


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day17_input.txt")

    ACTIVE = "#"
    INACTIVE = "."

    space = Space(lines)
    for _ in range(6):
        space = space.tick()

    print(">", len(space.space))

    space = Space2(lines)
    for _ in range(6):
        space = space.tick()

    print(">>", len(space.space))
