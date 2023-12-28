import numpy as np

def flood_fill(field, value, starting_position):
    if field[starting_position] != 0:
        return field
    
    active_positions = [starting_position]
    field[starting_position] = value

    while len(active_positions) > 0:

        new_active_positions = []
        for current_position in active_positions:
            for shift in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                new_position = (shift[0] + current_position[0], shift[1] + current_position[1])
                if new_position[0] < 0 or new_position[0] >= field.shape[0]:
                    continue
                if new_position[1] < 0 or new_position[1] >= field.shape[1]:
                    continue
                if field[new_position] != 0:
                    continue
                # print(current_position, ' -> ', new_position)

                if field[new_position] == 0:
                    field[new_position] = value
                    new_active_positions.append(new_position)
            
            # print(field)
            # input()
        
        # print(new_active_positions)
        active_positions = new_active_positions

    return field

def part1():

    commands = []

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        row_idx_max = 0
        col_idx_max = 0
        row_idx_min = 0
        col_idx_min = 0
        
        current_position = (0, 0)
        for line in lines:
            tmp = line.split()
            direction = tmp[0]
            ammount = int(tmp[1])
            colorcode = tmp[2][1:-1]
            commands.append((direction, ammount, colorcode))

            # print(direction, ammount, colorcode)

            if direction == 'U':
                current_position = (current_position[0] + ammount, current_position[1])
            elif direction == 'D':
                current_position = (current_position[0] - ammount, current_position[1])
            elif direction == 'R':
                current_position = (current_position[0], current_position[1] + ammount)
            elif direction == 'L':
                current_position = (current_position[0], current_position[1] - ammount)

            row_idx_max = max(row_idx_max, current_position[0])
            col_idx_max = max(col_idx_max, current_position[1])
            row_idx_min = min(row_idx_min, current_position[0])
            col_idx_min = min(col_idx_min, current_position[1])
        
        nrows = row_idx_max - row_idx_min + 1
        ncols = col_idx_max - col_idx_min + 1

        field = np.zeros((nrows, ncols), dtype = int)
        starting_position = (-row_idx_min, -col_idx_min)

    field[starting_position] = 1
    current_position = starting_position
    for command in commands:
        if command[0] == 'U':
            field[current_position[0]:current_position[0] + command[1] + 1, current_position[1]] = 1
            current_position = (current_position[0] + command[1], current_position[1])
        elif command[0] == 'D':
            field[current_position[0] - command[1]:current_position[0], current_position[1]] = 1
            current_position = (current_position[0] - command[1], current_position[1])
        elif command[0] == 'R':
            field[current_position[0], current_position[1]:current_position[1] + command[1] + 1] = 1
            current_position = (current_position[0], current_position[1] + command[1])
        elif command[0] == 'L':
            field[current_position[0], current_position[1] - command[1]:current_position[1]] = 1
            current_position = (current_position[0], current_position[1] - command[1])
        


    for c in range(ncols):
        field = flood_fill(field, -1, (0, c))
        field = flood_fill(field, -1, (nrows - 1, c))
    for r in range(nrows):
        field = flood_fill(field, -1, (r, 0))
        field = flood_fill(field, -1, (r, ncols - 1))

    answer = 0
    for r in range(nrows):
        for c in range(ncols):
            if field[r, c] >= 0:
                answer += 1

    print(answer)

def part2():

    dirmap = {}
    dirmap['0'] = 'R'
    dirmap['1'] = 'D'
    dirmap['2'] = 'L'
    dirmap['3'] = 'U'

    commands = []

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        row_idx_max = 0
        col_idx_max = 0
        row_idx_min = 0
        col_idx_min = 0
        
        current_position = (0, 0)
        for line in lines:
            tmp = line.split()
            colorcode = tmp[2][1:-1]

            direction = dirmap[colorcode[-1]]
            amount = int(colorcode[1:-1], 16)

            # print(direction, amount, colorcode)
            commands.append((direction, amount))
        

    print(commands)

    horizontal_delimiters = [0]
    vertical_delimiters = [0]
    current_position_row = 0
    current_position_col = 0

    lines = []
    for cmd in commands:
        if cmd[0] == 'R':
            row1 = current_position_row
            row2 = current_position_row
            col1 = current_position_col
            col2 = current_position_col + cmd[1]

            current_position_col += cmd[1]
            if current_position_col not in horizontal_delimiters:
                horizontal_delimiters.append(current_position_col)
        elif cmd[0] == 'L':
            row1 = current_position_row
            row2 = current_position_row
            col1 = current_position_col - cmd[1]
            col2 = current_position_col

            current_position_col -= cmd[1]
            if current_position_col not in horizontal_delimiters:
                horizontal_delimiters.append(current_position_col)
        elif cmd[0] == 'U':
            row1 = current_position_row - cmd[1]
            row2 = current_position_row
            col1 = current_position_col
            col2 = current_position_col

            current_position_row -= cmd[1]
            if current_position_row not in vertical_delimiters:
                vertical_delimiters.append(current_position_row)
        elif cmd[0] == 'D':
            row1 = current_position_row 
            row2 = current_position_row + cmd[1]
            col1 = current_position_col
            col2 = current_position_col

            current_position_row += cmd[1]
            if current_position_row not in vertical_delimiters:
                vertical_delimiters.append(current_position_row)
        lines.append([(col1, col2), (row1, row2)])

    print(lines)
    horizontal_delimiters.sort()
    vertical_delimiters.sort()
    horizontal_invalid_lines = []
    vertical_invalid_lines = []
    for i in range(1, len(horizontal_delimiters)):
        for j in range(1, len(vertical_delimiters)):
            top_edge = (vertical_delimiters[j - 1], horizontal_delimiters[i - 1]), (vertical_delimiters[j - 1], horizontal_delimiters[i])
            bottom_edge = (vertical_delimiters[j], horizontal_delimiters[i - 1]), (vertical_delimiters[j], horizontal_delimiters[i])
            left_edge = (vertical_delimiters[j - 1], horizontal_delimiters[i - 1]), (vertical_delimiters[j - 1], horizontal_delimiters[i])
            right_edge = (vertical_delimiters[j], horizontal_delimiters[i - 1]), (vertical_delimiters[j], horizontal_delimiters[i])
            

    # print(horizontal_delimiters, vertical_delimiters)

    #construct rectangles
    rectangles = []
    for i in range(1, len(horizontal_delimiters)):
        for j in range(1, len(vertical_delimiters)):
            width = (vertical_delimiters[j - 1], vertical_delimiters[j])
            height = (horizontal_delimiters[i - 1], horizontal_delimiters[i])
            rectangles.append((width, height))

    # print(rectangles)

    for rectangle in rectangles:
        is_valid = False
        for line in lines:


# part1()
part2()
