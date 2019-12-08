from copy import copy, deepcopy
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
#memory = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

class IntComputer:
    def __init__(self, memory):
        self.memory = memory
        self.halt = False
        self.ptr = 0
        self.consumed = False

    def step(self, input_cmd):
        self.consumed = False

        instruction = str(self.memory[self.ptr])
        opcode = int(instruction[-2:])
        mode = instruction[-3::-1]
        # Append leading 0s to mode
        mode += ("0" * (3 - len(mode)))
        output = None

        if opcode in [1, 2, 5, 6, 7, 8]:
            operators = []

            if mode[0] == '0':
                # Use value as address
                operators.append(self.memory[self.memory[self.ptr+1]])
            else:
                operators.append(self.memory[self.ptr+1])

            if mode[1] == '0':
                operators.append(self.memory[self.memory[self.ptr+2]])
            else:
                operators.append(self.memory[self.ptr+2])

            operators.append(self.memory[self.ptr+3])

            if opcode == 1:
                #print(f"[1]: {operators[0]} + {operators[1]} to MEM[{operators[2]}]")
                self.memory[operators[2]] = operators[0] + operators[1]
            elif opcode == 2:
                #print(f"[2]: {operators[0]} * {operators[1]} to MEM[{operators[2]}]")
                self.memory[operators[2]] = operators[0] * operators[1]

            # jump-if-true
            elif opcode == 5:
                #print(f"[5]: {operators[0]} != 0, jump to {operators[1]}")
                if operators[0] != 0:
                    self.ptr = operators[1]
                    return # Don't increment ptr

            # jump-if-false
            elif opcode == 6:
                #print(f"[6]: {operators[0]} == 0, jump to {operators[1]}")
                if operators[0] == 0:
                    self.ptr = operators[1]
                    return # Don't increment ptr

            # less than
            elif opcode == 7:
                #print(f"[7]: {operators[0]} < {operators[1]} to MEM[{operators[2]}]")
                if operators[0] < operators[1]:
                    self.memory[operators[2]] = 1
                else:
                    self.memory[operators[2]] = 0

            # equals
            elif opcode == 8:
                #print(f"[8]: {operators[0]} == {operators[1]} to MEM[{operators[2]}]")
                if operators[0] == operators[1]:
                    self.memory[operators[2]] = 1
                else:
                    self.memory[operators[2]] = 0

        elif opcode == 3: # Save it to address
            operator = self.memory[self.ptr+1]
            #print(f"[3]: Will save input at {operator}")

            # Flags main loop that input has been consumed
            self.consumed = True

            input_v = input_cmd

            self.memory[operator] = int(input_v)
        elif opcode == 4:
            operator = self.memory[self.ptr+1]
            output = self.memory[operator]
            print(f"[4]: Reading value from MEM[{operator}]: {output}")

        elif opcode == 99:
            print("Halt.")
            self.halt = True

        if opcode == 3 or opcode == 4:
            self.ptr += 2
        elif opcode == 5 or opcode == 6:
            self.ptr += 3
        elif opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
            self.ptr += 4

        return output

def runOnePerm(phases):
    amps = [IntComputer(copy(memory)) for _ in range(5)]
    c = 0
    for amp, phase in zip(amps, phases):
        while not amp.consumed:
            amp.step(phase)
        amp.consumed = False
        print(f"Set {phase} to amp {c}.")
        c += 1

    # Run loop until all halt
    all_halt = False
    running_output = 0
    while not all_halt:
        # Run amps in order, get output and feed to next
        halt_count = 0
        for i, amp in enumerate(amps):
            print(f"Running amp {i}. {running_output}")
            while not amp.consumed:
                amp_out = amp.step(running_output)
                if amp.halt:
                    break
            amp.consumed = False
            # At this point, it consumed the input, run until get output
            while amp_out == None:
                amp_out = amp.step(0)
                if amp.halt:
                    break

            if amp.halt:
                print("halted.")
                halt_count += 1
                continue
            else:
                running_output = amp_out

        if halt_count == len(amps):
            all_halt = True
            break

    return running_output


permuts = list(permutations([9, 8, 7, 6, 5]))
largest_signal = 0
for p in permuts:
    signal = runOnePerm(p) 
    if signal > largest_signal:
        largest_signal = signal

    #print(signal)

print(f"Largest signal was: {largest_signal}")
