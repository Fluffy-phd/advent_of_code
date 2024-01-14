import numpy as np
from time import time

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

# def get_n_available_points(field):
#     nrows = field.shape[0]
#     ncols = field.shape[1]
#     active_vertices = [(0, 0)]

#     visited_vertices = np.zeros((nrows, ncols), dtype = int)
#     visited_vertices[(0, 0)] = 1

#     while len(active_vertices):
#         active_vertices_new = []

#         for u in active_vertices:
#             for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
#                 r_ = u[0] + shift[0]
#                 c_ = u[1] + shift[1]

#                 if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
#                     continue
#                 if visited_vertices[r_, c_] > 0 or field[r_, c_] == 0:
#                     continue

#                 active_vertices_new.append((r_, c_))
#                 visited_vertices[r_, c_] = 1

#         active_vertices = active_vertices_new

#     answer = 0
#     for c in visited_vertices.reshape(-1):
#         if c == 1:
#             answer += 1
#     return answer

# def get_field_properties(field_, starting_vertex):
#     field = field_.copy()
#     nrows = field.shape[0]
#     ncols = field.shape[1]

#     distance_matrix = -np.ones((nrows, ncols), dtype = int)
#     color_matrix = np.zeros((2, nrows, ncols), dtype = int)

#     active_vertices = [starting_vertex]
#     distance_matrix[starting_vertex] = 0
#     color_matrix[0, starting_vertex[0], starting_vertex[1]] = 1
    
#     distance = 0
#     while len(active_vertices):
#         active_vertices_new = []
#         distance += 1
#         color = (distance % 2)
#         for u in active_vertices:
#             for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
#                 r_ = u[0] + shift[0]
#                 c_ = u[1] + shift[1]

#                 if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
#                     continue
                
#                 if field[r_, c_] == 0:
#                     continue

#                 color_matrix[color, r_, c_] = 1

#                 if distance_matrix[r_, c_] < 0 or distance_matrix[r_, c_] > distance:
#                     distance_matrix[r_, c_] = distance
#                     active_vertices_new.append((r_, c_))

#         active_vertices = active_vertices_new

#     max_distance = np.max(distance_matrix)
#     colored_vertices_cummulative = np.zeros((2, max_distance + 1), dtype = int)
#     for r in range(nrows):
#         for c in range(ncols):
#             d = distance_matrix[r, c]
#             if d >= 0:
#                 if color_matrix[0, r, c] == 1:
#                     color = 0
#                 else:
#                     color = 1
#                 colored_vertices_cummulative[color, d] += 1
#     for c in range(colored_vertices_cummulative.shape[0]):
#         for d in range(1, colored_vertices_cummulative.shape[1]):
#             colored_vertices_cummulative[c, d] += colored_vertices_cummulative[c, d - 1]

                



#     return colored_vertices_cummulative

# def get_n_fields(cummulative_colors, macro_field_coordinates, distance_limit, color_shift_):
#     if distance_limit < 0:
#         return 0
    
#     active_color_idx = (macro_field_coordinates[0] + macro_field_coordinates[1] + color_shift_) % 2
#     if distance_limit >= cummulative_colors.shape[1]:
#         return cummulative_colors[active_color_idx][-1]

#     return cummulative_colors[active_color_idx][distance_limit]

def get_distance_matrix(field_, starting_points, starting_point_distances):
    field = field_.copy()
    nrows = field.shape[0]
    ncols = field.shape[1]

    distance_matrix = -np.ones((nrows, ncols), dtype = int)

    for i in range(len(starting_points)):
        distance_matrix[starting_points[i]] = starting_point_distances[i]
    active_vertices = starting_points.copy()

    while len(active_vertices):
        active_vertices_new = []
        for u in active_vertices:
            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                r_ = u[0] + shift[0]
                c_ = u[1] + shift[1]

                if r_ < 0 or r_ >= nrows or c_ < 0 or c_ >= ncols:
                    continue
                
                if field[r_, c_] == 0:
                    continue

                if distance_matrix[r_, c_] < 0 or distance_matrix[r_, c_] > 1 + distance_matrix[u]:
                    distance_matrix[r_, c_] = 1 + distance_matrix[u]

                    if (r_, c_) not in active_vertices_new:
                        active_vertices_new.append((r_, c_))

        active_vertices = active_vertices_new


    return distance_matrix

def left_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    left_edge = [(r, 0) for r in range(nrows)]
    right_edge = [(r, ncols - 1) for r in range(nrows)]
    while True:
        distances = [D[-1][u] + 1 for u in left_edge]
        D_ = get_distance_matrix(field, right_edge, distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    return (D, np.max(Dd[-1]))

def right_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    left_edge = [(r, 0) for r in range(nrows)]
    right_edge = [(r, ncols - 1) for r in range(nrows)]

    while True:
        distances = [D[-1][u] + 1 for u in right_edge]
        D_ = get_distance_matrix(field, left_edge, distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    return (D, np.max(Dd[-1]))

def top_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    top_edge = [(0, c) for c in range(ncols)]
    bottom_edge = [(nrows - 1, c) for c in range(ncols)]
    while True:
        distances = [D[-1][u] + 1 for u in top_edge]
        D_ = get_distance_matrix(field, bottom_edge, distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    return (D, np.max(Dd[-1]))

def bottom_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    top_edge = [(0, c) for c in range(ncols)]
    bottom_edge = [(nrows - 1, c) for c in range(ncols)]
    while True:
        distances = [D[-1][u] + 1 for u in bottom_edge]
        D_ = get_distance_matrix(field, top_edge, distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    return (D, np.max(Dd[-1]))

def top_left_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    while True:
        distances = [D[-1][0, 0] + 2]
        D_ = get_distance_matrix(field, [(nrows - 1, ncols - 1)], distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    # for d in D:
    #     print(d)
    # for D_ in Dd:
    #     print(D_)

    return (D, np.max(Dd[-1]))

def top_right_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    while True:
        distances = [D[-1][0, ncols - 1] + 2]
        D_ = get_distance_matrix(field, [(nrows - 1, 0)], distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    # for d in D:
    #     print(d)
    # for D_ in Dd:
    #     print(D_)

    return (D, np.max(Dd[-1]))

def bottom_right_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    while True:
        distances = [D[-1][nrows - 1, ncols - 1] + 2]
        D_ = get_distance_matrix(field, [(0, 0)], distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    # for d in D:
    #     print(d)
    # for D_ in Dd:
    #     print(D_)

    return (D, np.max(Dd[-1]))

def bottom_left_expansion(D0, field):
    nrows = field.shape[0]
    ncols = field.shape[1]
    D = [D0]
    Dd = []

    while True:
        distances = [D[-1][nrows - 1, 0] + 2]
        D_ = get_distance_matrix(field, [(0, ncols - 1)], distances)

        Ddtmp = D_ - D[-1]

        if len(Dd) > 0:
            if np.sum(Dd[-1] - Ddtmp) == 0:
                break
        Dd.append(D_ - D[-1])
        D.append(D_)
        

    D.pop(-1)
    # for d in D:
    #     print(d)
    # for D_ in Dd:
    #     print(D_)

    return (D, np.max(Dd[-1]))

def get_active_fields(D):
    AF_ODD = []
    AF_EVEN = []

    for r in range(D.shape[0]):
        for c in range(D.shape[1]):
            if D[r, c] >= 0:
                if D[r, c] % 2 == 0:
                    AF_EVEN.append((r, c))
                else:
                    AF_ODD.append((r, c))
    return (AF_EVEN, AF_ODD)

def get_number_active_field_distance(AF, D, d):
    out = 0
    for c in AF:
        if D[c] <= d:
            out += 1
    return out

def analysis_straight(FF, AF, AF_modality, D_, shift, distance_limit, m):
    out = 0

    # print(distance_limit)
    # for D in D_[1:]:
    #     print(D)
    #left expansion analysis
    # out_sub = []
    if len(D_) >= m + 1:
        for i in range(1, m + 1):
            AF_modality = (AF_modality + 1) % 2
            D = D_[i]
            tmp = get_number_active_field_distance(AF[AF_modality], D, distance_limit)
            out += tmp
            # out_sub.insert(0, tmp)
            # print(FF[AF_modality] - tmp)
        return out


    for i in range(1, len(D_)):
        AF_modality = (AF_modality + 1) % 2
        D = D_[i]
        tmp = get_number_active_field_distance(AF[AF_modality], D, distance_limit)
        out += tmp
        # out_sub.insert(0, tmp)
        # print(FF[AF_modality] - tmp)
    
    D = D_[-1]

    distance_range = [D[0, 0], D[0, 0]]
    for e in D:
        for f in e:
            if f >= 0:
                # print(f)
                distance_range[0] = min(distance_range[0], f)
                distance_range[1] = max(distance_range[1], f)
                
    # # distance_range[1] + k * shift <= distance_limit
    # # print(distance_range)
    # # distance_range = (np.min(D[r for D[r] >= 0]), np.max(D))
    # # print(distance_range)

    # # print(k, distance_limit, distance_range)
    # k = len(D_)

    # i = 0
    # k <= (distance_limit - distance_range[0]) / shift
    k = max(0, (distance_limit - distance_range[1]) // shift)
    # print('k', k)
    kodd = k%2 + k//2
    keven = k - kodd
    if AF_modality == 0:
        nodd = kodd
        neven = keven
    else:
        nodd = keven
        neven = kodd
    out += nodd * FF[1] + neven * FF[0]
    AF_modality = (AF_modality + k) % 2
    
    distance_limit -= k * shift
    # print(distance_limit, distance_range)
    while distance_range[0] <= distance_limit:
        # distance_range += shift
        # i += 1
        distance_limit -= shift
        AF_modality = (AF_modality + 1) % 2
        # print('X', distance_range, distance_limit)
        tmp = get_number_active_field_distance(AF[AF_modality], D, distance_limit)
        out += tmp
        # print(FF[AF_modality] - tmp)

    return out

    

    
    return (out, out_sub) 
    max_distance = np.max(D_[-1])
    distance_remaining = np.max(distance_limit - max_distance, 0)
    number_of_repeats_neccessary = distance_remaining / shift
    number_of_full_fields = int(np.floor(number_of_repeats_neccessary))
    if AF_modality == 0:
        number_of_odd_full_fields = number_of_full_fields // 2 + number_of_full_fields % 2
        number_of_even_full_fields = number_of_full_fields // 2
    else:
        number_of_even_full_fields = number_of_full_fields // 2 + number_of_full_fields % 2
        number_of_odd_full_fields = number_of_full_fields // 2

    out += number_of_even_full_fields * FF[0]
    out += number_of_odd_full_fields * FF[1]
    AF_modality = (AF_modality + number_of_full_fields) % 2
    # print('max d:', max_distance, '# of full fields:', number_of_full_fields, '# of odd FF: ', number_of_odd_full_fields, '# of even FF:', number_of_even_full_fields)

    distance_limit -= shift * number_of_full_fields
    while True:
        Dtmp = D_[-1]
        for r in range(Dtmp.shape[0]):
            for c in range(Dtmp.shape[1]):
                if Dtmp[r, c] >= 0:
                    Dtmp[r, c] += shift

        AF_modality = (AF_modality + 1) % 2
        # print(Dtmp)
        # print('modality: ', AF_modality)
        tmp = get_number_active_field_distance(AF[AF_modality], Dtmp, distance_limit)
        # print(tmp, np.max(Dtmp), distance_limit)
        distance_limit -= shift
        if tmp == 0:
            break
        out += tmp
    
    return out
    
def analysis_diagonal(FF, AF, D_, shift, distance_limit, m):
    out = 0
    D = D_[-1]
    M = m - 1
    distance_limit -= M * shift
    k = m

    distance_range = [D[0, 0], D[0, 0]]
    for e in D:
        for f in e:
            if f >= 0:
                # print(f)
                distance_range[0] = min(distance_range[0], f)
                distance_range[1] = max(distance_range[1], f)

    # modality = np.zeros((m, m), dtype = int)
    # block_res = np.zeros((m, m), dtype = int)

    AF_modality = (m + 1) % 2
    for i in range(m):
        # print('square of size: %d x %d'%(m, m), distance_range, distance_limit)
        tmp = get_number_active_field_distance(AF[AF_modality], D, distance_limit)
        # modality[m - 1, i] = AF_modality
        # block_res[m - 1, i] = tmp

        # print('modality', AF_modality, 'distance', distance_limit, 'res', tmp, 'target', FF[AF_modality])
        out += k * tmp
        AF_modality = (AF_modality + 1) % 2
        k -= 1
        distance_limit += shift
        if FF[(AF_modality + 1) % 2] == tmp:
            break
    
    # print(out)
    nblocks_a = 0
    nblocks_b = 0


    if (k % 2) == 0:
        l = k // 2
        nblocks_a = l * (l + 1)
        nblocks_b = l * l
    else:
        l = (k + 1) // 2
        # print(l)
        nblocks_a = l * l
        nblocks_b = l * (l - 1)
    # print(k, l, nblocks_a, nblocks_b)

    if AF_modality == 0:
        out += FF[0] * nblocks_a + FF[1] * nblocks_b
    else:
        out += FF[1] * nblocks_a + FF[0] * nblocks_b


    # print(out)
    # print(modality[-1])
    # print(block_res[-1])
        

    


    return out
    # while tmp < FF[AF_modality]:

    #diagonal analysis, modality doesnt change
    for i in range(1, len(D_)):
        D = D_[i]
        tmp = get_number_active_field_distance(AF[AF_modality], D, distance_limit) * (2 * i - 1)
        tmp2 = get_number_active_field_distance(AF[(AF_modality + 1) % 2], D, distance_limit - shift_narrow) * (2 * i)
        if tmp > 0:
            out += tmp + tmp2
            print(D)
            print(tmp, tmp2)
        if tmp2 <= 0:
            return out
        
    diagonal_offset = (len(D_) - 1) * 2
    print('diagonal offset: ', diagonal_offset)
        
    max_distance = np.max(D_[-1]) + shift_narrow
    distance_remaining = np.max(distance_limit - max_distance, 0)
    number_of_repeats_neccessary = distance_remaining / shift_narrow
    number_of_full_fields = int(np.floor(number_of_repeats_neccessary))

    print('number of blocks of modality %d = %d' % ((AF_modality + 1) % 2, (number_of_full_fields - 1) // 2))
    # (diagonal_offset + 1) + (diagonal_offset + 3) + (diagonal_offset + 5) ... (number_of_full_fields) blocks of modality (AF_modality + 1) % 2
    if AF_modality == 0:
        number_of_odd_full_fields = number_of_full_fields // 2 + number_of_full_fields % 2
        number_of_even_full_fields = number_of_full_fields // 2
    else:
        number_of_even_full_fields = number_of_full_fields // 2 + number_of_full_fields % 2
        number_of_odd_full_fields = number_of_full_fields // 2

    out += number_of_even_full_fields * FF[0]
    out += number_of_odd_full_fields * FF[1]
    AF_modality = (AF_modality + number_of_full_fields) % 2
    # print('max d:', max_distance, '# of full fields:', number_of_full_fields, '# of odd FF: ', number_of_odd_full_fields, '# of even FF:', number_of_even_full_fields)

    distance_limit -= shift_narrow * number_of_full_fields
    while True:
        Dtmp = D_[-1]
        for r in range(Dtmp.shape[0]):
            for c in range(Dtmp.shape[1]):
                if Dtmp[r, c] >= 0:
                    Dtmp[r, c] += shift_narrow

        AF_modality = (AF_modality + 1) % 2
        # print(Dtmp)
        # print('modality: ', AF_modality)
        tmp = get_number_active_field_distance(AF[AF_modality], Dtmp, distance_limit) * mult
        # print(tmp, np.max(Dtmp), distance_limit)
        distance_limit -= shift_narrow
        if tmp == 0:
            break
        out += tmp
    
    return out
    
def part2(distance_limit, target):
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
    t0 = time()

    #properties of the central field
    D0 = get_distance_matrix(field, [starting_position], [0])
    # print(D0)
    D_l, shift_l = left_expansion(D0, field)
    D_r, shift_r = right_expansion(D0, field)
    D_t, shift_t = top_expansion(D0, field)
    D_b, shift_b = bottom_expansion(D0, field)
    D_tl, shift_tl = top_left_expansion(D0, field)
    D_tr, shift_tr = top_right_expansion(D0, field)
    D_br, shift_br = bottom_right_expansion(D0, field)
    D_bl, shift_bl = bottom_left_expansion(D0, field)

    AF_EVEN, AF_ODD = get_active_fields(D0)

    AF_modality = distance_limit % 2
    if AF_modality == 0:
        FF = [len(AF_EVEN), len(AF_ODD)]
        AF = (AF_EVEN, AF_ODD)
    else:
        FF = [len(AF_ODD), len(AF_EVEN)]
        AF = (AF_ODD, AF_EVEN)
    # print(FF)


    n = (D0.shape[0] - 1) // 2
        
    m = int(np.ceil((distance_limit - n) / D0.shape[0]))
    # number_of_squares = (2*m + 1)**2
    # number_of_even_squares = number_of_squares//2 + 1
    # number_of_odd_squares = number_of_squares - number_of_even_squares
    
    # upper limit on the answer
    # answer = number_of_even_squares * FF[0] + number_of_odd_squares * FF[1]
    answer = 0

    # macro_field = np.ones((2*m + 1, 2*m + 1), dtype = int)
    # subtract the fields that are clearly out of range
    # for corner in range(m):
    #     distance_from_center = D0.shape[0] * (1 + 2*(m - 1) - corner) + 1
    #     # print('corner %2d, distance: %d' % (corner, distance_from_center))

    #     #top-left corner
    #     if distance_from_center > distance_limit:
    #         answer -= FF[corner % 2] * (1 + corner) * 4

    #         # for i in range(corner + 1):
    #         #     macro_field[corner - i, i] = 0
    #         #     macro_field[i, 2*m - corner + i] = 0
    #         #     macro_field[2*m - corner + i, i] = 0
    #         #     macro_field[2*m - corner + i, 2*m - i] = 0
    #     else:
    #         break


    # macro_field[m, m] = get_number_active_field_distance(AF[0], D0, distance_limit)

    #subtract partial fields
    #central field
    answer = get_number_active_field_distance(AF[0], D0, distance_limit)

    answer += analysis_straight(FF, AF, 0, D_l, shift_l, distance_limit, m)
    answer += analysis_straight(FF, AF, 0, D_r, shift_r, distance_limit, m)
    answer += analysis_straight(FF, AF, 0, D_t, shift_t, distance_limit, m)
    answer += analysis_straight(FF, AF, 0, D_b, shift_b, distance_limit, m)

    answer += analysis_diagonal(FF, AF, D_tl, shift_t, distance_limit, m)
    answer += analysis_diagonal(FF, AF, D_tr, shift_t, distance_limit, m)
    answer += analysis_diagonal(FF, AF, D_bl, shift_t, distance_limit, m)
    answer += analysis_diagonal(FF, AF, D_br, shift_t, distance_limit, m)

    # print(macro_field)

    # print(D_tl)




    # # print('modality: ',  AF_modality)
    # answer = get_number_active_field_distance(AF[AF_modality], D0, distance_limit)

    # answer += analysis(FF, AF, AF_modality, D_l, shift_l, distance_limit)
    # answer += analysis(FF, AF, AF_modality, D_r, shift_r, distance_limit)
    # answer += analysis(FF, AF, AF_modality, D_t, shift_t, distance_limit)
    # answer += analysis(FF, AF, AF_modality, D_b, shift_b, distance_limit)
    
    # answer += analysis_tl(FF, AF, AF_modality, D_tl, shift_tl, shift_l, distance_limit)
    # # answer += analysis_diagonal(FF, AF, AF_modality, D_tr, shift_tr, distance_limit)
    # # answer += analysis_diagonal(FF, AF, AF_modality, D_bl, shift_bl, distance_limit)
    # # answer += analysis_diagonal(FF, AF, AF_modality, D_br, shift_br, distance_limit)
    
    # # print(D0)

    t = time() - t0
    print('%20d, %10.3f [s]' % (answer, t))
    error = abs(answer - target)
    # print(error, FF)

    # for i in range((error // FF[0]) + 1):
    #     a = i * FF[0]
    #     b = (error - a) % FF[1]

    #     print(i, b)
    #     if b == 0:
    #         break


# part1()
# part2(distance_limit = 6, target = 16)
# part2(distance_limit = 10, target = 50)
# part2(distance_limit = 50, target = 1594)
# part2(distance_limit = 100, target = 6536)
# part2(distance_limit = 500, target = 167004)
# part2(distance_limit = 1000, target = 668697)
# part2(distance_limit = 5000, target = 16733044)
    

part2(distance_limit = 26501365, target = 16733044)
