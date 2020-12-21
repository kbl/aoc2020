import collections 

input = "0,3,6"
input = "20,0,1,11,6,3"

if __name__ == "__main__":
    numbers = [int(number) for number in input.split(",")]
    occurences = collections.defaultdict(list)

    for turn, number in enumerate(numbers, 1):
        occurences[number].append(turn)

    turn = len(numbers) + 1
    previous_number = numbers[-1]

    while turn <= 2020:
        if len(occurences[previous_number]) == 1:
            number_to_say = 0
        else:
            second_to_last_turn, last_turn = occurences[previous_number][-2:]
            number_to_say = last_turn - second_to_last_turn

        occurences[number_to_say].append(turn)
        previous_number = number_to_say
        numbers.append(number_to_say)
        turn += 1

    print(">", numbers[-1])

    occurences = {number: [turn] for turn, number in enumerate(numbers, 1)}
    turn = len(numbers) + 1
    previous_number = numbers[-1]

    while turn <= 30000000:
        if len(occurences[previous_number]) == 1:
            number_to_say = 0
        else:
            second_to_last_turn, last_turn = occurences[previous_number]
            number_to_say = last_turn - second_to_last_turn

        if number_to_say in occurences:
            occurences[number_to_say] = [occurences[number_to_say][-1], turn]
        else:
            occurences[number_to_say] = [turn]

        previous_number = number_to_say
        turn += 1

    print(">>", number_to_say)
