import numpy as np

def get_distance_matrix_from_edges(field_):
    field = field_.copy()
    nrows = field.shape[0]
    ncols = field.shape[1]

    distance_matrix = -np.ones((nrows, ncols), dtype = int)

    active_vertices = []
    for c in range(ncols):
        c1 = (0, c)
        if field[c1] < 0 and distance_matrix[c1] < 0:
            active_vertices.append(c1)
            distance_matrix[c1] = 0

        c2 = (nrows - 1, c)
        if field[c2] < 0 and distance_matrix[c2] < 0:
            active_vertices.append(c2)
            distance_matrix[c2] = 0

    for r in range(nrows):
        r1 = (r, 0)
        if field[r1] < 0 and distance_matrix[r1] < 0:
            active_vertices.append(r1)
            distance_matrix[r1] = 0

        r2 = (r, ncols - 1)
        if field[r2] < 0 and distance_matrix[r2] < 0:
            active_vertices.append(r2)
            distance_matrix[r2] = 0
    
    distance = 0
    while len(active_vertices):
        active_vertices_new = []
        distance += 1
        for u in active_vertices:
            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                r_ = u[0] + shift[0]
                c_ = u[1] + shift[1]

                if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
                    continue
                
                if field[r_, c_] == 0:
                    continue

                if distance_matrix[r_, c_] < 0 or distance_matrix[r_, c_] > distance:
                    distance_matrix[r_, c_] = distance
                    active_vertices_new.append((r_, c_))

        active_vertices = active_vertices_new


    return distance_matrix

def get_distance_matrix_from_center(field_):
    field = field_.copy()
    nrows = field.shape[0]
    ncols = field.shape[1]

    distance_matrix = -np.ones((nrows, ncols), dtype = int)

    active_vertices = [((nrows - 1)//2, (ncols - 1)//2)]
    distance_matrix[active_vertices[-1]] = 0
    
    distance = 0
    while len(active_vertices):
        active_vertices_new = []
        distance += 1
        for u in active_vertices:
            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                r_ = u[0] + shift[0]
                c_ = u[1] + shift[1]

                if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
                    continue
                
                if field[r_, c_] == 0:
                    continue

                if distance_matrix[r_, c_] < 0 or distance_matrix[r_, c_] > distance:
                    distance_matrix[r_, c_] = distance
                    active_vertices_new.append((r_, c_))

        active_vertices = active_vertices_new


    return distance_matrix

def get_n_available_points(field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    active_vertices = [(0, 0)]

    visited_vertices = np.zeros((nrows, ncols), dtype = int)
    visited_vertices[(0, 0)] = 1

    while len(active_vertices):
        active_vertices_new = []

        for u in active_vertices:
            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                r_ = u[0] + shift[0]
                c_ = u[1] + shift[1]

                if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
                    continue
                if visited_vertices[r_, c_] > 0 or field[r_, c_] == 0:
                    continue

                active_vertices_new.append((r_, c_))
                visited_vertices[r_, c_] = 1

        active_vertices = active_vertices_new

    answer = 0
    for c in visited_vertices.reshape(-1):
        if c == 1:
            answer += 1
    return answer


def get_n_valid_endpoints(field_, starting_position, nsteps_limit):
    field = field_.copy()
    nrows = field.shape[0]
    ncols = field.shape[1]
    active_vertices = [starting_position]
    visited_vertices = np.zeros((nrows, ncols), dtype = int)
    visited_vertices[starting_position] = 1

    nsteps = 0
    while len(active_vertices) and nsteps <= nsteps_limit:
        active_vertices_new = []

        for u in active_vertices:
            if nsteps % 2 == 0:
                field[u] = 1

            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                r_ = u[0] + shift[0]
                c_ = u[1] + shift[1]

                if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
                    continue
                if visited_vertices[r_, c_] > 0 or field[r_, c_] == 0:
                    continue

                active_vertices_new.append((r_, c_))
                visited_vertices[r_, c_] = 1
        nsteps += 1

        active_vertices = active_vertices_new


    answer = 0
    for c in field.reshape(-1):
        if c == 1:
            answer += 1
    return answer

def part1():
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        nrows = len(lines)
        ncols = len(lines[0].strip())
        field = -np.ones((nrows, ncols), dtype = int)

        for r, line in enumerate(lines):
            for c, cc in enumerate(line):
                if cc == '#':
                    field[r, c] = 0
                if cc == 'S':
                    starting_position = (r, c)
        
    print(get_n_valid_endpoints(field, starting_position, 64))
    

def get_field_properties(field_, starting_vertex):
    field = field_.copy()
    nrows = field.shape[0]
    ncols = field.shape[1]

    distance_matrix = -np.ones((nrows, ncols), dtype = int)
    color_matrix = np.zeros((2, nrows, ncols), dtype = int)

    active_vertices = [starting_vertex]
    distance_matrix[starting_vertex] = 0
    color_matrix[0, starting_vertex[0], starting_vertex[1]] = 1
    
    distance = 0
    while len(active_vertices):
        active_vertices_new = []
        distance += 1
        color = (distance % 2)
        for u in active_vertices:
            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                r_ = u[0] + shift[0]
                c_ = u[1] + shift[1]

                if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
                    continue
                
                if field[r_, c_] == 0:
                    continue

                color_matrix[color, r_, c_] = 1

                if distance_matrix[r_, c_] < 0 or distance_matrix[r_, c_] > distance:
                    distance_matrix[r_, c_] = distance
                    active_vertices_new.append((r_, c_))

        active_vertices = active_vertices_new

    max_distance = np.max(distance_matrix)
    colored_vertices_cummulative = np.zeros((2, max_distance + 1), dtype = int)
    for r in range(nrows):
        for c in range(ncols):
            d = distance_matrix[r, c]
            if d >= 0:
                if color_matrix[0, r, c] == 1:
                    color = 0
                else:
                    color = 1
                colored_vertices_cummulative[color, d] += 1
    for c in range(colored_vertices_cummulative.shape[0]):
        for d in range(1, colored_vertices_cummulative.shape[1]):
            colored_vertices_cummulative[c, d] += colored_vertices_cummulative[c, d - 1]

                



    return colored_vertices_cummulative

def get_n_fields(cummulative_colors, macro_field_coordinates, distance_limit, color_shift_):
    if distance_limit < 0:
        return 0
    
    active_color_idx = (macro_field_coordinates[0] + macro_field_coordinates[1] + color_shift_) % 2
    if distance_limit >= cummulative_colors.shape[1]:
        return cummulative_colors[active_color_idx][-1]

    return cummulative_colors[active_color_idx][distance_limit]


def part2():
    with open('input2.txt', 'r') as f:
        lines = f.readlines()

        nrows = len(lines)
        ncols = len(lines[0].strip())
        field = -np.ones((nrows, ncols), dtype = int)

        for r, line in enumerate(lines):
            for c, cc in enumerate(line):
                if cc == '#':
                    field[r, c] = 0
                if cc == 'S':
                    starting_position = (r, c)

    nsteps_limit = 5
    nsteps_center2edge = (nrows - 1)//2 + 1
    nsteps_center2corner = nrows + 1
    nsteps_across = nrows
    
    # distances from center of edges towards the rest of the field
    # right_edge_distances, right_edge_colors, right_edge_cummulative = get_field_properties(field, ((nrows - 1) // 2, 0))
    # top_edge_distances, top_edge_colors, top_edge_cummulative = get_field_properties(field, (nrows - 1, (ncols - 1) // 2))
    # bottom_edge_distances, bottom_edge_colors, bottom_edge_cummulative = get_field_properties(field, (0, (ncols - 1) // 2))
    central_cummulative = get_field_properties(field, starting_position)

    # distances from the corners towards the rest of the field
    # bottomleft_corner_distances, bottomleft_corner_colors, bottomleft_corner_cummulative = get_field_properties(field, (nrows - 1, 0))
    # bottomright_corner_distances, bottomright_corner_colors, bottomright_corner_cummulative = get_field_properties(field, (nrows - 1, ncols - 1))

    # field_n_0 = get_n_valid_endpoints(field, (0, 0), nrows * ncols * 2)
    # field_n_1 = get_n_valid_endpoints(field, (0, 1), nrows * ncols * 2)

    # print('fields with global coords (i, j) such that (i + j) % 2 = 0', field_n_1)
    # print('fields with global coords (i, j) such that (i + j) % 2 = 1', field_n_0)
    answer = get_n_fields(central_cummulative, (0, 0), nsteps_limit, 1)
    #(nsteps_limit - nsteps_center2edge + nsteps_across) / nsteps_across > c
    straight_max = int(np.ceil((nsteps_limit - nsteps_center2edge + nsteps_across) / nsteps_across) + 1)
    left_edge_cummulative = get_field_properties(field, ((nrows - 1) // 2, ncols - 1))
    for c in range(1, straight_max):
        nsteps_limit_ = nsteps_limit - nsteps_center2edge - (c - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = left_edge_cummulative, macro_field_coordinates = (0, -c), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp

    right_edge_cummulative = get_field_properties(field, ((nrows - 1) // 2, 0))
    for c in range(1, straight_max):
        nsteps_limit_ = nsteps_limit - nsteps_center2edge - (c - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = right_edge_cummulative, macro_field_coordinates = (0, c), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp

    top_edge_cummulative = get_field_properties(field, (nrows - 1, (ncols - 1) // 2))
    for c in range(1, straight_max):
        nsteps_limit_ = nsteps_limit - nsteps_center2edge - (c - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = top_edge_cummulative, macro_field_coordinates = (-c, 0), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp

    bottom_edge_cummulative = get_field_properties(field, (0, (ncols - 1) // 2))
    for c in range(1, straight_max):
        nsteps_limit_ = nsteps_limit - nsteps_center2edge - (c - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = bottom_edge_cummulative, macro_field_coordinates = (c, 0), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp

    topleft_corner_cummulative = get_field_properties(field, (nrows - 1, ncols - 1))
    for distance in range(1, 202301):
        nsteps_limit_ = nsteps_limit - nsteps_center2corner - (distance - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = topleft_corner_cummulative, macro_field_coordinates = (-distance, -1), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp * distance

    topright_corner_cummulative = get_field_properties(field, (nrows - 1, 0))
    for distance in range(1, 202301):
        nsteps_limit_ = nsteps_limit - nsteps_center2corner - (distance - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = topright_corner_cummulative, macro_field_coordinates = (-distance, 1), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp * distance

    bottomright_corner_cummulative = get_field_properties(field, (0, 0))
    for distance in range(1, 202301):
        nsteps_limit_ = nsteps_limit - nsteps_center2corner - (distance - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = bottomright_corner_cummulative, macro_field_coordinates = (distance, 1), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp * distance

    bottomleft_corner_cummulative = get_field_properties(field, (0, ncols - 1))
    for distance in range(1, 202301):
        nsteps_limit_ = nsteps_limit - nsteps_center2corner - (distance - 1) * nsteps_across
        tmp = get_n_fields(cummulative_colors = bottomleft_corner_cummulative, macro_field_coordinates = (distance, -1), distance_limit = nsteps_limit_, color_shift_ = 0)
        answer += tmp * distance

    # distance_limit = nsteps_limit - nrows + 1
    # #top-left quadrant edge
    # topleft_corner_distances, topleft_corner_colors, topleft_corner_cummulative = get_field_properties(field, (nrows - 1, ncols - 1))
    # for distance in range(1, nleft + 10):
    #     coordinates_top_left = (-distance, -1)
    #     tmp_ = get_n_fields(nrows, topleft_corner_cummulative, coordinates_top_left, distance_limit)
    #     answer += distance * tmp_

    # topright_corner_distances, topright_corner_colors, topright_corner_cummulative = get_field_properties(field, (nrows - 1, 0))
    # for distance in range(1, nright + 10):
    #     coordinates_top_right = (-distance, 1)
    #     tmp_ = get_n_fields(nrows, topright_corner_cummulative, coordinates_top_right, distance_limit)
    #     answer += distance * tmp_

    # bottomright_corner_distances, bottomright_corner_colors, bottomright_corner_cummulative = get_field_properties(field, (0, 0))
    # for distance in range(1, nright + 10):
    #     coordinates_bottom_right = (distance, 1)
    #     tmp_ = get_n_fields(nrows, bottomright_corner_cummulative, coordinates_bottom_right, distance_limit)
    #     answer += distance * tmp_

    # bottomright_corner_distances, bottomright_corner_colors, bottomleft_corner_cummulative = get_field_properties(field, (0, ncols - 1))
    # for distance in range(1, nleft + 10):
    #     coordinates_bottom_left = (distance, 1)
    #     tmp_ = get_n_fields(nrows, bottomleft_corner_cummulative, coordinates_bottom_left, distance_limit)
    #     answer += distance * tmp_

    # print(answer)
    # # print(tmp_, tmp2_)
    # # for r in range(1, nleft):
    # #     answer += get_n_fields(nrows, topleft_corner_cummulative, (-r, -(nleft - r - 1)), distance_limit)
    # # print(answer)

    # # #top-right quadrant edge
    # # for r in range(1, nright):
    # #     answer += get_n_fields(nrows, topleft_corner_cummulative, (-r, (nright - r - 1)), distance_limit)
    print(answer)


    
    # # nsteps_limit = 26501365
    # # # nsteps_limit = 6
    
    # # #precompute number of terminating fields depending on the initial 

    # # # nfields
    # # nfield_distance = (nsteps_limit - ((nrows - 1) / 2))// nrows
    # # print(nfield_distance)

    # # print(get_distance_matrix_from_edges(field))
    # # print(get_distance_matrix_from_center(field))
    
    # # if nsteps_limit % 2 == 0:




    # # # distances from the starting vertex to the edges
    # # start_to_top
    # # start_to_bot
    # # start_to_left
    # # start_to_right

# part1()
part2()