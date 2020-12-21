import ioaoc
import collections

test_data = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

TREE = "#"

def parse_map(lines):
    trees = set()
    for row_index, row in enumerate(lines):
        for column_index, cell in enumerate(row):
            if cell == TREE:
                trees.add((column_index, row_index))

    return trees, column_index, row_index

def traverse_map(trees, height, width, step_right, step_down):
    trees_positions = set()
    position = (0, 0)
    while position[1] <= height:
        if position in trees:
            trees_positions.add(position)
        column_index, row_index = position
        column_index = (column_index + step_right) % (width + 1)
        row_index += step_down
        position = (column_index, row_index)
    return trees_positions


if __name__ == "__main__":
    lines = ioaoc.read_file("day03_input.txt")
    trees, width, height = parse_map(lines)

    print(">", len(traverse_map(trees, height, width, 3, 1)))

    slope_product = 1
    for step_right, step_down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        slope_product *= len(traverse_map(trees, height, width, step_right, step_down))

    print(">>", slope_product)
