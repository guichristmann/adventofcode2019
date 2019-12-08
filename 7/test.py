from copy import copy

with open("input.txt", "r") as f:
    # There's only one line for this input
    line = f.readline().strip('\n')
    memory = [int(v) for v in line.split(',')]

#memory = [1002, 4, 3, 4, 33]
#memory = [3,9,8,9,10,9,4,9,99,-1,8]
#memory = [3,9,7,9,10,9,4,9,99,-1,8]
#memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
#memory = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
#memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]

memory = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

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

    if opcode in [1, 2, 5, 6, 7, 8]:
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

        # jump-if-true
        elif opcode == 5:
            print(f"[5]: {operators[0]} != 0, jump to {operators[1]}")
            if operators[0] != 0:
                ptr = operators[1]
                continue # Don't increment ptr

        # jump-if-false
        elif opcode == 6:
            print(f"[6]: {operators[0]} == 0, jump to {operators[1]}")
            if operators[0] == 0:
                ptr = operators[1]
                continue # Don't increment ptr

        # less than
        elif opcode == 7:
            print(f"[7]: {operators[0]} < {operators[1]} to MEM[{operators[2]}]")
            if operators[0] < operators[1]:
                memory[operators[2]] = 1
            else:
                memory[operators[2]] = 0

        # equals
        elif opcode == 8:
            print(f"[8]: {operators[0]} == {operators[1]} to MEM[{operators[2]}]")
            if operators[0] == operators[1]:
                memory[operators[2]] = 1
            else:
                memory[operators[2]] = 0

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
    elif opcode == 5 or opcode == 6:
        ptr += 3
    elif opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
        ptr += 4
