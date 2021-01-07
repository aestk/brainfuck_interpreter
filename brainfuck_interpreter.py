# A simple brainfuck interpreter that works ... sort of
# Only one line can be read at once

# Try this, for example : ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++. (source: Wikipedia)

# Cells for storing the data
cells = []
# List for storing jump marks position
jump_marks = []

cell_pointer = 0
instruction_pointer = 0

# Adds 1 to the cell pointer (goes one cell up)
def increment_cell_pointer():
    global cell_pointer
    if cell_pointer < 29999:
        cell_pointer += 1

# Subtracts 1 from the cell pointer (goes one cell down)
def decrement_cell_pointer():
    global cell_pointer
    if cell_pointer > 0:
        cell_pointer -= 1

# Adds 1 to the current cell
def increment_byte():
    global cell_pointer
    if cells[cell_pointer] < 127:
        cells[cell_pointer] += 1

# Subtracts 1 from the current cell
def decrement_byte():
    global cell_pointer
    if cells[cell_pointer] > 0:
        cells[cell_pointer] -= 1

# Outputs the current cell value as ASCII character
def output_byte():
    global cell_pointer
    print(chr(cells[cell_pointer]), end="")

# Lets the user input a single ASCII character
def input_byte():
    global cell_pointer
    while True:
        inp = input()
        if len(inp) == 1:
            break
    
    cells[cell_pointer] = ord(inp)

# Sets the cell pointer to the next instruction after the loop end if the cell
# value is 0, if not, the next instruction is called
def check_jump_forward(i):
    global cell_pointer
    if cells[cell_pointer] == 0:
        for n in range(len(jump_marks)):
            if jump_marks[n][0] == i:
                return (jump_marks[n][1]+1)
    return i
  
# Sets the cell pointer to the next instruction after the loop start if the cell
# value is not 0, if not, the next instruction is called
def check_jump_backward(i):
    global cell_pointer
    if cells[cell_pointer] != 0:
        for n in range(len(jump_marks)):
            if jump_marks[n][1] == i:
                return jump_marks[n][0]
    return i

# Initializes the cells
for i in range(30000):
    cells.append(0)

program = input("Enter your program: ")

# Creates jump mark list
# Forward jumps
for i in range(len(program)):
    if program[i] == "[":
        jump_marks.append([i])
        
# Backward jumps
temp_forward_jumps = []
for i in range(len(program)):
    if program[i] == "]":
        for j in range(i, -1, -1):
            if program[j] == "[" and j not in temp_forward_jumps:
                temp_forward_jumps.append(j)
                for mark in jump_marks:
                    if mark[0] == j:
                        mark.append(i)
                break

# All characters which are not part of the instruction set are ignored
while instruction_pointer < len(program):
    if program[instruction_pointer] == ">":
        increment_cell_pointer()
    elif program[instruction_pointer] == "<":
        decrement_cell_pointer()
    elif program[instruction_pointer] == "+":
        increment_byte()
    elif program[instruction_pointer] == "-":
        decrement_byte()
    elif program[instruction_pointer] == ".":
        output_byte()
    elif program[instruction_pointer] == ",":
        input_byte()
    elif program[instruction_pointer] == "[":
        instruction_pointer = check_jump_forward(instruction_pointer)
    elif program[instruction_pointer] == "]":
        instruction_pointer = check_jump_backward(instruction_pointer)
    instruction_pointer += 1