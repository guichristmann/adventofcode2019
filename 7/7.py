from copy import copy
from itertools import permutations

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
#memory = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]

# Assuming the program is expecting 2 inputs
def run2In1Out(program, phase_cmds):
    last_output = 0
    total = 0
    for phase_cmd in phase_cmds:
        # Applying problem modifications
        halt = False
        ptr = 0 # Start at the beginning, duh
        read_count = 0
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
                if read_count == 0:
                    input_v = phase_cmd #input("Input: ")
                    read_count += 1
                elif read_count == 1:
                    input_v = last_output
                    read_count += 1
                else:
                    print("Should not be here.")
                memory[operator] = int(input_v)
            elif opcode == 4:
                operator = memory[ptr+1]
                last_output = memory[operator]
                print(f"[4]: Reading value from MEM[{operator}]: {last_output}")

            elif opcode == 99:
                halt = True
            if opcode == 3 or opcode == 4:
                ptr += 2
            elif opcode == 5 or opcode == 6:
                ptr += 3
            elif opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
                ptr += 4

        total += last_output

    return last_output 

permuts = list(permutations([0, 1, 2, 3, 4]))
largest_signal = 0
for p in permuts:
    signal = run2In1Out(copy(memory), p)
    if signal > largest_signal:
        largest_signal = signal

print(largest_signal)
#print(run2In1Out(copy(memory), [4, 3, 2, 1, 0]))
