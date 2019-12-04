from copy import copy

with open("input.txt", "r") as f:
    # There's only one line for this input
    line = f.readline().strip('\n')
    initial_memory = [int(v) for v in line.split(',')]

# Applying problem modifications
target = 19690720
foundTarget = False
for noun in range(0, 100):
    for verb in range(0, 100):
        memory = copy(initial_memory)
        memory[1] = noun
        memory[2] = verb

        halt = False
        ptr = 0 # Start at the beginning, duh
        while not halt:
            opcode = memory[ptr]
            print(f"MEM[{ptr}]: [{opcode}]")
            if opcode == 99:
                halt = True
                continue
            elif opcode == 1: # Addition
                operators = memory[ptr+1:ptr+4]
                print(f"Addition with {operators}")
                memory[operators[2]] = memory[operators[0]] + memory[operators[1]]
            elif opcode == 2: # Addition
                operators = memory[ptr+1:ptr+4]
                print(f"Multiplication with {operators}")
                memory[operators[2]] = memory[operators[0]] * memory[operators[1]]

            ptr += 4

        if memory[0] == target:
            foundTarget = True
            break

    if foundTarget:
        break
print(noun, verb)
print(100 * noun + verb) # Answer
