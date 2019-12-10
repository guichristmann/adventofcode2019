from copy import copy

DEBUG = False

def debugPrint(s):
    if DEBUG:
        print(s)

with open("input.txt", "r") as f:
    # There's only one line for this input
    line = f.readline().strip('\n')
    vals = [int(v) for v in line.split(',')]

#memory = [1002, 4, 3, 4, 33]
#memory = [3,9,8,9,10,9,4,9,99,-1,8]
#memory = [3,9,7,9,10,9,4,9,99,-1,8]
#memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
#memory = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
#memory = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]

#memory = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] 
#vals = [1102,34915192,34915192,7,4,7,99,0]
#vals = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
#vals = [104,1125899906842624,99]

memory = {i: v for i, v in enumerate(vals)}

def readMemory(pos):
    try:
        return memory[pos]
    except KeyError:
        debugPrint(f"{pos} not in memory, initializing with 0.")
        memory[pos] = 0
        return 0
 
# Applying problem modifications
halt = False
ptr = 0 # Start at the beginning, duh
relative_base = 0
while not halt:
    instruction = str(readMemory(ptr))
    opcode = int(instruction[-2:])
    mode = instruction[-3::-1]
    # Append leading 0s to mode
    debugPrint(mode)
    mode += ("0" * (3 - len(mode)))
    debugPrint(f"MEM[{ptr}]: [{opcode}] / [{mode}]")

    if opcode in [1, 2, 5, 6, 7, 8]:
        operators = []
        debugPrint(mode)
        if mode[0] == '0': # Position
            # Use value as address
            operators.append(readMemory(readMemory(ptr+1)))
        elif mode[0] == '1': # Immediate mode
            operators.append(readMemory(ptr+1))
        elif mode[0] == '2': # Relative mode
            operators.append(readMemory(readMemory(ptr+1) + relative_base))
        else:
            debugPrint("Unrecognized mode for first operand.")


        if mode[1] == '0':
            operators.append(readMemory(readMemory(ptr+2)))
        elif mode[1] == '1':
            operators.append(readMemory(ptr+2))
        elif mode[1] == '2':
            operators.append(readMemory(readMemory(ptr+2) + relative_base))
        else:
            debugPrint("Unrecognized mode for second operand.")

        if mode[2] == '0':
            operators.append(readMemory(ptr+3))
        elif mode[2] == '2':
            operators.append(readMemory(ptr+3) + relative_base)

        if opcode == 1:
            debugPrint(f"[1]: {operators[0]} + {operators[1]} to MEM[{operators[2]}]")
            memory[operators[2]] = operators[0] + operators[1]
        elif opcode == 2:
            debugPrint(f"[2]: {operators[0]} * {operators[1]} to MEM[{operators[2]}]")
            memory[operators[2]] = operators[0] * operators[1]

        # jump-if-true
        elif opcode == 5:
            debugPrint(f"[5]: {operators[0]} != 0, jump to {operators[1]}")
            if operators[0] != 0:
                ptr = operators[1]
                continue # Don't increment ptr

        # jump-if-false
        elif opcode == 6:
            debugPrint(f"[6]: {operators[0]} == 0, jump to {operators[1]}")
            if operators[0] == 0:
                ptr = operators[1]
                continue # Don't increment ptr

        # less than
        elif opcode == 7:
            debugPrint(f"[7]: {operators[0]} < {operators[1]} to MEM[{operators[2]}]")
            if operators[0] < operators[1]:
                memory[operators[2]] = 1
            else:
                memory[operators[2]] = 0

        # equals
        elif opcode == 8:
            debugPrint(f"[8]: {operators[0]} == {operators[1]} to MEM[{operators[2]}]")
            if operators[0] == operators[1]:
                memory[operators[2]] = 1
            else:
                memory[operators[2]] = 0

    elif opcode == 3: # Save it to address
        if mode[0] == '0': # Position
            # Use value as address
            operator = readMemory(readMemory(ptr+1))
        elif mode[0] == '1': # Immediate mode
            operator = readMemory(ptr+1)
        elif mode[0] == '2': # Relative mode
            operator = readMemory(ptr+1) + relative_base
        else:
            debugPrint("Unrecognized mode for first operand.")

        debugPrint(f"[3]: Will save input at {operator}")
        input_v = input("Input: ")
        memory[operator] = int(input_v)
    elif opcode == 4:
        if mode[0] == '0': # Position
            # Use value as address
            debugPrint("[4] Position mode")
            output = readMemory(readMemory(ptr+1))
        elif mode[0] == '1': # Immediate mode
            debugPrint("[4] Immediate mode")
            output = readMemory(ptr+1)
        elif mode[0] == '2': # Relative mode
            debugPrint("[4] Relative mode")
            output = readMemory(readMemory(ptr+1) + relative_base)
        else:
            debugPrint("Unrecognized mode for first operand.")

        print(f"###: {output}")
    elif opcode == 9:
        if mode[0] == '0': # Position
            # Use value as address
            debugPrint("[9] Position mode")
            operator = readMemory(readMemory(ptr+1))
        elif mode[0] == '1': # Immediate mode
            debugPrint("[9] Immediate mode")
            operator = readMemory(ptr+1)
        elif mode[0] == '2': # Relative mode
            debugPrint("[9] Relative mode")
            operator = readMemory(readMemory(ptr+1) + relative_base)
        else:
            debugPrint("Unrecognized mode for first operand.")

        debugPrint(f"[9]: Setting relative base to {operator}.")
        relative_base += operator

    elif opcode == 99:
        halt = True
    if opcode == 3 or opcode == 4 or opcode == 9:
        ptr += 2
    elif opcode == 5 or opcode == 6:
        ptr += 3
    elif opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
        ptr += 4
