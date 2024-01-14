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

def get_area(color, vertex_colors, vertex2coords_map, horizontal_delimiters, vertical_delimiters):
    area = 0
    for u in range(len(vertex_colors)):
        if vertex_colors[u] != color:
            continue

        u_coords = vertex2coords_map[u]
        # print(u_coords)
        area += (horizontal_delimiters[u_coords[1] + 1] - horizontal_delimiters[u_coords[1]]) * (vertical_delimiters[u_coords[0] + 1] - vertical_delimiters[u_coords[0]])

    return area

def flood_fill_part2(color, vertex_colors, neighbors, s):

    active_vertices = [s]
    vertex_colors[s] = color

    while len(active_vertices) > 0:
        active_vertices_new = []

        for u in active_vertices:
            for v in neighbors[u]:
                if vertex_colors[v] < 0:
                    vertex_colors[v] = color
                    active_vertices_new.append(v)
        active_vertices = active_vertices_new

def is_part_of_border(edge, lines):
    for l in lines:
        if edge[0][0] >= l[0][0] and edge[0][1] <= l[0][1] and edge[1][0] >= l[1][0] and edge[1][1] <= l[1][1]:
            # print(edge, l)
            return True

    return False

def print_colors(vertex_colors, coords2vertex_map, nrow_vertices, ncol_vertices, color, fn):
    
    with open(fn, 'w') as f:
        for r in range(nrow_vertices):
            for c in range(ncol_vertices):
                if vertex_colors[coords2vertex_map[r, c]] == color:
                    f.write('#')
                else:
                    f.write('.')
            f.write('\n')

def part2():

    dirmap = {}
    dirmap['0'] = 'R'
    dirmap['1'] = 'D'
    dirmap['2'] = 'L'
    dirmap['3'] = 'U'

    commands = []

    edge_len = 0
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
            edge_len += amount

            # print(direction, amount, colorcode)
            commands.append((direction, amount))
        

    # print(commands)

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

    # print()
    # for l in lines:
    #     print(l)
    # print()
    # print(lines)
    horizontal_delimiters.sort()
    vertical_delimiters.sort()
    # print(vertical_delimiters)
    # print(horizontal_delimiters)
    # horizontal_invalid_lines = []
    # vertical_invalid_lines = []
    # for i in range(1, len(horizontal_delimiters)):
    #     for j in range(1, len(vertical_delimiters)):
    #         top_edge = ((vertical_delimiters[j - 1], horizontal_delimiters[i - 1]), (vertical_delimiters[j - 1], horizontal_delimiters[i]))
    #         bottom_edge = ((vertical_delimiters[j], horizontal_delimiters[i - 1]), (vertical_delimiters[j], horizontal_delimiters[i]))
    #         left_edge = ((vertical_delimiters[j - 1], horizontal_delimiters[i - 1]), (vertical_delimiters[j - 1], horizontal_delimiters[i]))
    #         right_edge = ((vertical_delimiters[j], horizontal_delimiters[i - 1]), (vertical_delimiters[j], horizontal_delimiters[i]))

    #         rectangles.append(top_edge)
    nrow_vertices = (len(vertical_delimiters) - 1)
    ncol_vertices = (len(horizontal_delimiters) - 1)
    nvertices = nrow_vertices * ncol_vertices
    neighbors = [[] for _ in range(nvertices)]    

    coords2vertex_map = np.zeros((nrow_vertices, ncol_vertices), dtype = int)
    vertex2coords_map = []
    for row_idx in range(nrow_vertices):
        for col_idx in range(ncol_vertices):
            coords2vertex_map[row_idx, col_idx] = len(vertex2coords_map)
            vertex2coords_map.append((row_idx, col_idx))

    for row_idx in range(nrow_vertices):
        for col_idx in range(ncol_vertices):
            
            u = coords2vertex_map[row_idx, col_idx]

            if col_idx < ncol_vertices - 1:
                right_edge = [(horizontal_delimiters[col_idx + 1], horizontal_delimiters[col_idx + 1]), (vertical_delimiters[row_idx], vertical_delimiters[row_idx + 1])]
                if not is_part_of_border(right_edge, lines):
                    v = coords2vertex_map[row_idx, col_idx + 1]
                    neighbors[u].append(v)
                    neighbors[v].append(u)

            if row_idx < nrow_vertices - 1:
                bottom_edge = [(horizontal_delimiters[col_idx], horizontal_delimiters[col_idx + 1]), (vertical_delimiters[row_idx + 1], vertical_delimiters[row_idx + 1])]
                if not is_part_of_border(bottom_edge, lines):
                    v = coords2vertex_map[row_idx + 1, col_idx]
                    neighbors[u].append(v)
                    neighbors[v].append(u)
            
            # return

    # print()
    # # print(neighbors)
    # for u in range(nvertices):
    #     print(u, neighbors[u])
    # print()
    # flood fill
    vertex_colors = -np.ones(nvertices, dtype = int)
    color = 0
    while np.min(vertex_colors) < 0:
        for r in range(nrow_vertices):
            for c in range(ncol_vertices):
                if vertex_colors[coords2vertex_map[r, c]] < 0:
                    flood_fill_part2(color, vertex_colors, neighbors, coords2vertex_map[r, c])
                    # print(vertex_colors)
                    color += 1

    print_colors(vertex_colors, coords2vertex_map, nrow_vertices, ncol_vertices, 0, 'flood0.txt')
    print_colors(vertex_colors, coords2vertex_map, nrow_vertices, ncol_vertices, 1, 'flood1.txt')
    print_colors(vertex_colors, coords2vertex_map, nrow_vertices, ncol_vertices, 2, 'flood2.txt')
    print_colors(vertex_colors, coords2vertex_map, nrow_vertices, ncol_vertices, 3, 'flood3.txt')
    print_colors(vertex_colors, coords2vertex_map, nrow_vertices, ncol_vertices, 4, 'flood4.txt')

    area0 = get_area(0, vertex_colors, vertex2coords_map, horizontal_delimiters, vertical_delimiters)
    area1 = get_area(1, vertex_colors, vertex2coords_map, horizontal_delimiters, vertical_delimiters)
    area2 = get_area(2, vertex_colors, vertex2coords_map, horizontal_delimiters, vertical_delimiters)
    area3 = get_area(3, vertex_colors, vertex2coords_map, horizontal_delimiters, vertical_delimiters)
    area4 = get_area(4, vertex_colors, vertex2coords_map, horizontal_delimiters, vertical_delimiters)
    print(area0 + edge_len // 2 + 1)
    print(area1 + edge_len // 2 + 1)
    print(area2 + edge_len // 2 + 1)
    print(area3 + edge_len // 2 + 1)
    print(area4 + edge_len // 2 + 1)

    # area1: 102000662718092


# part1()
part2()
