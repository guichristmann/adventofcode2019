from copy import copy

with open("input.txt", "r") as f:
    # There's only one line for this input
    line = f.readline().strip('\n')
    memory = [int(v) for v in line.split(',')]

#memory = [1002, 4, 3, 4, 33]

# Applying problem modifications
halt = False
ptr = 0 # Start at the beginning, duh
while not halt:
    instruction = str(memory[ptr])
    opcode = int(instruction[-2:])
    mode = instruction[-3::-1]
    # Append leading 0s to mode
    print(mode)
    mode += ("0" * (3 - len(mode)))
    print(f"MEM[{ptr}]: [{opcode}] / [{mode}]")

    if opcode == 1 or opcode == 2:
        operators = []
        print(mode)
        if mode[0] == '0':
            # Use value as address
            operators.append(memory[memory[ptr+1]])
        else:
            operators.append(memory[ptr+1])

        if mode[1] == '0':
            operators.append(memory[memory[ptr+2]])
        else:
            operators.append(memory[ptr+2])

        operators.append(memory[ptr+3])

        if opcode == 1:
            print(f"[1]: {operators[0]} + {operators[1]} to MEM[{operators[2]}]")
            memory[operators[2]] = operators[0] + operators[1]
        elif opcode == 2:
            print(f"[2]: {operators[0]} * {operators[1]} to MEM[{operators[2]}]")
            memory[operators[2]] = operators[0] * operators[1]

    elif opcode == 3: # Save it to address
        operator = memory[ptr+1]
        print(f"[3]: Will save input at {operator}")
        input_v = input("Input: ")
        memory[operator] = int(input_v)
    elif opcode == 4:
        operator = memory[ptr+1]
        output = memory[operator]
        print(f"[4]: Reading value from MEM[{operator}]: {output}")

    elif opcode == 99:
        halt = True

    if opcode == 3 or opcode == 4:
        ptr += 2
    else:
        ptr += 4
