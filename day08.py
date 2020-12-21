import ioaoc
test_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

        

def parse(lines):
    instructions = []
    for line in lines:
        operator, operand = line.split(" ")
        operand = int(operand)
        instructions.append((operator, operand))
    return instructions


class Interpreter:
    def __init__(self, instructions, registers=None):
        if registers is None:
            registers = [0]
        self.registers = registers
        self.instructions = instructions
        self.instruction_pointer = 0

    def execute(self):
        visited = set([self.instruction_pointer])
        while True:
            instruction, operand = self.instructions[self.instruction_pointer]
            getattr(self, instruction)(operand)
            if self.instruction_pointer in visited:
                return False
            visited.add(self.instruction_pointer)
        return True

    def acc(self, operand):
        self.registers[0] += operand
        self.instruction_pointer += 1

    def nop(self, _):
        self.instruction_pointer += 1

    def jmp(self, operand):
        self.instruction_pointer += operand

if __name__ == "__main__":
    lines = ioaoc.read_file("day08_input.txt")
    instructions = parse(lines)
    
    interpreter = Interpreter(instructions)
    interpreter.execute()
    [register] = interpreter.registers
    print(">", register)

    modified_instructions = list(instructions)
    was_last_execution_successfull = False
    last_changed_instruction = -1
    while True:
        interpreter = Interpreter(modified_instructions)
        try:
            was_last_execution_successfull = interpreter.execute()
        except IndexError:
            [register] = interpreter.registers
            print(">>", register)
            break

        if was_last_execution_successfull:
            break

        for instruction_index, instruction in enumerate(modified_instructions):
            if instruction_index <= last_changed_instruction:
                continue

            instruction, operand = instruction

            if instruction == "nop":
                new_instruction = "jmp"
            elif instruction == "jmp":
                new_instruction = "nop"
            else:
                continue

            modified_instructions = list(instructions)
            modified_instructions[instruction_index] = (new_instruction, operand)
            last_changed_instruction = instruction_index
            break
