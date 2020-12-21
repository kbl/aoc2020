import ioaoc

test_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


class Board:
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"

    def __init__(self, representation):
        self.seats = [Board.get_seats(representation)]

    @staticmethod
    def get_seats(lines):
        return [list(row) for row in lines]

    def next_iteration(self, seat_discovery_callable, occupied_threshold):
        new_seats = []

        seats = self.seats[-1]

        for row_index, row in enumerate(seats):
            new_row = []
            for column_index, seat in enumerate(row):
                adjacent_stats = {Board.FLOOR: 0, Board.EMPTY: 0, Board.OCCUPIED: 0}
                for adjacent, _, _ in seat_discovery_callable(column_index, row_index, seats):
                    adjacent_stats[adjacent] += 1

                new_seat = seat
                if seat == Board.EMPTY and adjacent_stats[Board.OCCUPIED] == 0:
                    new_seat = Board.OCCUPIED
                if seat == Board.OCCUPIED and adjacent_stats[Board.OCCUPIED] >= occupied_threshold:
                    new_seat = Board.EMPTY

                new_row.append(new_seat)
            new_seats.append(new_row)

        self.seats.append(new_seats)

    @staticmethod
    def adjacent(seat_column_index, seat_row_index, seats):
        adjacent_seats = []
        for row_distance in (-1, 0, 1):

            row_index = seat_row_index + row_distance
            if row_index < 0 or row_index >= len(seats):
                continue
            row = seats[row_index]
            
            for column_distance in (-1, 0, 1):
                column_index = seat_column_index + column_distance

                if column_index < 0 or column_index >= len(row):
                    continue

                if row_distance == 0 and column_distance == 0:
                    continue

                adjacent_seats.append((row[column_index], column_index, row_index))

        return adjacent_seats

    @staticmethod
    def visible(seat_column_index, seat_row_index, seats):
        visible_seats = []
        for row_modifier in (-1, 0, 1):
            for column_modifier in (-1, 0, 1):
                if column_modifier == 0 and row_modifier == 0:
                    continue

                row_index = seat_row_index
                column_index = seat_column_index
                while True:
                    row_index += row_modifier
                    if row_index < 0 or row_index >= len(seats):
                        break
                    row = seats[row_index]

                    column_index += column_modifier
                    if column_index < 0 or column_index >= len(row):
                        break

                    if row[column_index] == Board.FLOOR:
                        continue

                    visible_seats.append((row[column_index], column_index, row_index))
                    break

        return visible_seats

    def __str__(self):
        return "\n".join(["".join(row) for row in self.seats[-1]])

    def count(self, seat_type):
        how_many = 0
        for row in self.seats[-1]:
            for seat in row:
                if seat == seat_type:
                    how_many += 1
        return how_many


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day11_input.txt")

    board = Board(lines)

    while True:
        board.next_iteration(Board.adjacent, occupied_threshold=4)
        if board.seats[-1] == board.seats[-2]:
            break

    print(">", board.count(Board.OCCUPIED))

    board = Board(lines)

    while True:
        board.next_iteration(Board.visible, occupied_threshold=5)
        if board.seats[-1] == board.seats[-2]:
            break

    print(">>", board.count(Board.OCCUPIED))
