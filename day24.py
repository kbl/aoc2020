import ioaoc

test_input = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

MOVES = {
        "1": (-0.5, 1),
        "2": (0.5, 1),
        "3": (1, 0),
        "4": (0.5, -1),
        "5": (-0.5, -1),
        "6": (-1, 0),
}


def parse_line(line):
    """
    >>> parse_line("nwwswee")
    [(-0.5, 1), (-1, 0), (-1, -1)]
    """
    #  nw ne                      
    # w      e
    #  sw se
    #   1 2                       
    # 6     3
    #   5 4 
    line = line.replace("nw", "1")
    line = line.replace("ne", "2")
    line = line.replace("sw", "5")
    line = line.replace("se", "4")
    line = line.replace("e", "3")
    line = line.replace("w", "6")
    return [MOVES[move] for move in line]


def adjacent(position):
    x, y = position
    return [(x + move_x, y + move_y) for move_x, move_y in MOVES.values()]


def parse(lines):
    return [parse_line(line) for line in lines]


def count_black(tiles):
    count = 0
    for tile in tiles.values():
        if tile == "b":
            count += 1
    return count


if __name__ == "__main__":
    lines = ioaoc.read_file("day24_input.txt")
    lines = test_input.split("\n")
    parsed_lines = parse(lines)
    tiles = {}

    for moves in parsed_lines:
        x = 0
        y = 0
        for (move_x, move_y) in moves:
            x += move_x
            y += move_y
        position = (x, y)
        tile = tiles.get(position, "w")
        if tile == "w":
            tile = "b"
        else:
            tile = "w"
        tiles[position] = tile

    print(">", count_black(tiles))

    generation = tiles
    for i in range(100):
        next_generation = {}

        to_check = set()
        for position in generation.keys():
            to_check.update(adjacent(position))

        for position in to_check:
            blacks = 0
            for p in adjacent(position):
                if generation.get(p, "w") == "b":
                    blacks += 1

            tile = generation.get(position, "w")
            if tile == "b" and (blacks == 0 or blacks > 2):
                next_generation[position] = "w"
            elif tile == "w" and blacks == 2:
                next_generation[position] = "b"
            else:
                next_generation[position] = tile

        generation = next_generation
    print(">>", count_black(generation))
