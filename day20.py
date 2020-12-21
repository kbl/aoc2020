import ioaoc
import collections
import math

test_input = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""


def parse(lines):
    new_tile = True
    tile = []
    tiles = {}
    for line in lines:
        if not line:
            tile = []
            new_tile = True
            continue

        if new_tile:
            new_tile = False
            tile_id = int(line.split(" ")[1][:-1])
            continue

        tile.append(line)
        if len(tile) == 10:
            tiles[tile_id] = tile

    return tiles


def tile_borders(tile):
    """
    >>> tile_borders(["###..", "#....", "....#", "....#", "....."])
    ('###..', '..##.', '.....', '##...')
    """
    top = list(tile[0])
    bottom = list(tile[-1])

    left = []
    right = []
    for row in tile:
        left.append(row[0])
        right.append(row[-1])

    return "".join(top), "".join(right), "".join(bottom), "".join(left)


def flip_horizontally(tile_borders):
    """
    >>> flip_horizontally(('###..', '..##.', '.....', '##...'))
    ('.....', '.##..', '###..', '...##')
    """
    top, right, bottom, left = tile_borders
    return bottom, "".join(reversed(right)), top, "".join(reversed(left))


def rotate_right(tile_borders):
    """
    >>> rotate_right(('###..', '..##.', '...#.', '##...'))
    ('...##', '###..', '.##..', '...#.')
    """
    top, right, bottom, left = tile_borders
    return "".join(reversed(left)), top, "".join(reversed(right)), bottom


def all_borders(tile_borders):
    """
    >>> all_borders(('###..', '..##.', '...#.', '##...'))
    {(0, False): ('###..', '..##.', '...#.', '##...'), (0, True): ('...#.', '.##..', '###..', '...##'), (1, False): ('...##', '###..', '.##..', '...#.'), (1, True): ('.##..', '..###', '...##', '.#...'), (2, False): ('.#...', '...##', '..###', '.##..'), (2, True): ('..###', '##...', '.#...', '..##.'), (3, False): ('..##.', '.#...', '##...', '..###'), (3, True): ('##...', '...#.', '..##.', '###..')}
    """
    rotations = {}

    tile_borders = tuple(tile_borders)

    rotation_count = 0
    flipped = False
    rotations[(rotation_count, flipped)] = tile_borders
    flipped = True
    rotations[(rotation_count, flipped)] = flip_horizontally(tile_borders)

    for rotation_count in range(1, 4):
        flipped = False
        tile_borders = rotate_right(tile_borders)
        rotations[(rotation_count, flipped)] = tile_borders
        flipped = True
        rotations[(rotation_count, flipped)] = flip_horizontally(tile_borders)

    return rotations


def but_id(tile_id, borders):
    return [element for element in borders if element[0] != tile_id]


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = read_file("day20_input.txt")

    tiles = ioaoc.parse(lines)
    side = int(math.sqrt(len(tiles)))
    all_tile_borders = {}

    for tile_id, tile in tiles.items():
        all_tile_borders[tile_id] = all_borders(tile_borders(tile))

    left_border = collections.defaultdict(list)
    right_border = collections.defaultdict(list)
    top_border = collections.defaultdict(list)
    bottom_border = collections.defaultdict(list)

    for tile_id, tile_borders in all_tile_borders.items():
        for (orientation, (top, right, bottom, left)) in tile_borders.items():
            left_border[left].append((tile_id, *orientation))
            right_border[right].append((tile_id, *orientation))
            top_border[top].append((tile_id, *orientation))
            bottom_border[bottom].append((tile_id, *orientation))

    corner_candidates = []
    border_candidates = []
    center_candidates = []

    for tile_id, all_borders in all_tile_borders.items():
        can_be_in_the_center = False

        s_top, s_right, s_bottom, s_left = all_borders[(0, False)]

        borders_taken = len(but_id(tile_id, bottom_border[s_top]) +
        but_id(tile_id, left_border[s_right]) +
        but_id(tile_id, top_border[s_bottom]) +
        but_id(tile_id, right_border[s_left]))

        if borders_taken == 2:
            corner_candidates.append(tile_id)
        elif borders_taken == 3:
            border_candidates.append(tile_id)
        elif borders_taken == 4:
            center_candidates.append(tile_id)
        else:
            raise ValueError(tile_id)

    product = 1
    for tile_id in corner_candidates:
        product *= tile_id
    print(">", product)
