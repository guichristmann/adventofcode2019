with open("input.txt", "r") as f:
    # There's only one line for this input
    line = f.readline().strip('\n')
    memory = [int(v) for v in line.split(',')]

# Applying problem modifications
#memory[1] = 12
#memory[2] = 2

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

print(memory[0])
