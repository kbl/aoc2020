import ioaoc
import collections

test_input = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

def parse(lines):
    deck1 = collections.deque()
    deck2 = collections.deque()

    decks = {"Player 1:": deck1, "Player 2:": deck2}
    for line in lines:
        if not line:
            continue
        if line.startswith("Player"):
            deck = decks[line]
            continue
        deck.append(int(line))

    return deck1, deck2


def combat(deck1, deck2):
    while deck1 and deck2:
        card1 = deck1.popleft()
        card2 = deck2.popleft()

        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

        if card2 == card1:
            raise ValueError(card2)

    return deck1, deck2


def subdeck(deck, count):
    subdeck = collections.deque()
    for card_number, card in enumerate(deck, 1):
        if card_number > count:
            break
        subdeck.append(card)
    return subdeck


def combat2(deck1, deck2):
    all_decks = set()
    while deck1 and deck2:
        decks = (tuple(deck1), tuple(deck2))

        if decks in all_decks:
            return deck1, deck2, 1

        all_decks.add(decks)

        card1 = deck1.popleft()
        card2 = deck2.popleft()

        winner = 1

        if card1 <= len(deck1) and card2 <= len(deck2):
            subdeck1 = subdeck(deck1, card1)
            subdeck2 = subdeck(deck2, card2)

            _, _, winner = combat2(subdeck1, subdeck2)
        elif card2 > card1:
            winner = 2

        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

    if deck1:
        return deck1, deck2, 1
    return deck1, deck2, 2


def deck_value(deck):
    deck_value = 0
    for number, card in enumerate(reversed(deck), 1):
        deck_value += number * card
    return deck_value


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day22_input.txt")

    deck1, deck2 = parse(lines)
    deck1, deck2 = combat(deck1, deck2)

    winning_deck = deck1
    if deck2:
        winning_deck = deck2

    print(">", deck_value(winning_deck))

    deck1, deck2 = parse(lines)
    deck1, deck2, _ = combat2(deck1, deck2)

    winning_deck = deck1
    if deck2:
        winning_deck = deck2

    print(">>", deck_value(winning_deck))
