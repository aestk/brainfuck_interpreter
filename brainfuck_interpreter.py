# Warning: Messy, buggy, unstructured code
# Must be rewritten

# A interactive brainfuck interpreter that works ... sort of

# A set of instructions (whether single- or multi-line) can only be executed if Enter is pressed twice!

instruction_set = [">", "<", "+", "-", ".", ",", "[", "]"]

data = []
current_instructions = []
jump_marks = []
temp_forward_jumps = []
output = []

data_pointer = 0
instruction_pointer = 0

forward_jump_count = 0
backward_jump_count = 0

input_line = ""

# Increments the data pointer (goes one cell to the right)
def increment_data_pointer():
    global data_pointer
    if data_pointer < 29999:
        data_pointer += 1

# Decrements the data pointer (goes one cell to the left)
def decrement_data_pointer():
    global data_pointer
    if data_pointer > 0:
        data_pointer -= 1

# Increments the value of the current cell
def increment_data():
    global data_pointer
    if data[data_pointer] < 127:
        data[data_pointer] += 1
        
# Decrements the value of the current cell
def decrement_data():
    global data_pointer
    if data[data_pointer] > 0:
        data[data_pointer] -= 1

# Adds value of the current cell as ASCII character to the output list
def add_output():
    global data_pointer
    output.append(chr(data[data_pointer]))

# Lets the user input a value for the current cell
def input_data():
    global data_pointer
    while True:
        inp = input("")
        if len(inp) == 1:
            data[data_pointer] = ord(inp)
            break

# Sets the data pointer to the next instruction after the loop end if
# the cell value is 0, if not, the next instruction is called
def jump_forward(inst):
    global data_pointer
    if data[data_pointer] == 0:
        for i in range(len(jump_marks)):
            if jump_marks[i][0] == inst:
                return (jump_marks[i][1]+1)
    return inst

# Sets the data pointer to the next instruction after the loop start
# if the cell value is not 0, if not, the next instruction is called
def jump_backward(inst):
    global data_pointer
    if data[data_pointer] != 0:
        for i in range(len(jump_marks)):
            if jump_marks[i][1] == inst:
                return jump_marks[i][0]
    return inst

while True:
    # Initialize data
    for i in range(30000):
        data.append(0)

    input_line = input("> " + (forward_jump_count-backward_jump_count) * "... ")
        
    for char in input_line:
        if char in instruction_set:
            current_instructions.append(char)
            
        if char == "[":
            forward_jump_count += 1
        elif char == "]":
            backward_jump_count += 1
    
    # Analyze/execute instructions when an empty line is entered
    if input_line == "":
        # Create jump mark list
        # Forward jump marks
        
        # Iterates through current_instructions, appends
        # a list with a single element to jump_marks if instruction = [
        for i in range(len(current_instructions)):
            if current_instructions[i] == "[":
                jump_marks.append([i])
        
        # Backward jump marks
        
        # Iterates through current_instructions, if a backward
        # jump mark is found, iterate back find to the next forward
        # jump mark with no corresponding backward jump mark
        # A temporary list is used to keep track of the forward jump marks
        for i in range(len(current_instructions)):
            if current_instructions[i] == "]":
                for j in range(i, -1, -1):
                    if current_instructions[j] == "[" and j not in temp_forward_jumps:
                        temp_forward_jumps.append(j)
                        for mark in jump_marks:
                            if mark[0] == j:
                                mark.append(i)
                                break
                        break
        
        #print(current_instructions)
        while instruction_pointer < len(current_instructions):
            if current_instructions[instruction_pointer] == ">":
                increment_data_pointer()
            elif current_instructions[instruction_pointer] == "<":
                decrement_data_pointer()
            elif current_instructions[instruction_pointer] == "+":
                increment_data()
            elif current_instructions[instruction_pointer] == "-":
                decrement_data()
            elif current_instructions[instruction_pointer] == ".":
                add_output()
            elif current_instructions[instruction_pointer] == ",":
                input_data()
            elif current_instructions[instruction_pointer] == "[":
                instruction_pointer = jump_forward(instruction_pointer)
            elif current_instructions[instruction_pointer] == "]":
                instruction_pointer = jump_backward(instruction_pointer)              
            instruction_pointer += 1
        
        # Outputs the contents of the output list
        if len(output) > 0:
            for char in output:
                print(char, end="")
            print()
            
        # Clear data
        data = []
        # Clear input
        current_instructions = []
        # Clear jump marks
        jump_marks = []
        temp_forward_jumps = []
        # Clear output
        output = []
        
        # Reset data pointer
        data_pointer = 0
        # Reset instruction pointer
        instruction_pointer = 0
        
        # Reset jump counters
        forward_jump_count = 0
        backward_jump_count = 0