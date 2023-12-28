import numpy as np

def part1():
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    allowed_directions = [
        [0, 2, 3],
        [1, 2, 3],
        [0, 1, 2],
        [0, 1, 3],
    ]

    
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        # print(lines)
        nrows = len(lines)
        ncols = len(lines[0].strip())

        heat_matrix = np.zeros((nrows, ncols), dtype = np.int8)

        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip()):
                heat_matrix[i, j] = int(c)

    ndirections = len(directions)
    nsteps_max = 3
    coolest_paths = -np.ones((ndirections, nsteps_max + 1, nrows, ncols), dtype = int)
    cummulative_visits = np.zeros((nrows, ncols), dtype = int)

    u_src = (0, 0, 0, 0)
    coolest_paths[:, :, 0, 0] = 0

    active_vertices = [u_src]
    already_added = np.zeros((ndirections, nsteps_max + 1, nrows, ncols), dtype = np.int8)
    while len(active_vertices) > 0:
        new_active_vertices = []
        already_added.fill(0)

        for u in active_vertices:
            u_val = coolest_paths[u]
            u_direction = u[0]
            u_steps = u[1]
            u_row = u[2]
            u_col = u[3]
            cummulative_visits[u_row, u_col] += 1

            for v_direction in allowed_directions[u_direction]:
                direction = directions[v_direction]
                v_row = direction[0] + u_row
                v_col = direction[1] + u_col
                v_steps = 1
                if u_direction == v_direction:
                    v_steps += u_steps

                if (v_row < 0 or v_row >= nrows) or (v_col < 0 or v_col >= ncols) or v_steps > nsteps_max:
                    continue

                heat_increment = heat_matrix[v_row, v_col]
                v_heat = coolest_paths[v_direction, v_steps, v_row, v_col]
                if v_heat < 0 or (v_heat >= heat_increment + u_val):
                    coolest_paths[v_direction, v_steps, v_row, v_col] = heat_increment + u_val

                    if already_added[v_direction, v_steps, v_row, v_col] == 0:
                        new_active_vertices.append((v_direction, v_steps, v_row, v_col))
                        already_added[v_direction, v_steps, v_row, v_col] = 1

        active_vertices = new_active_vertices
    # print(cummulative_visits)

    destination_heat = coolest_paths[:, :, -1, -1]
    min_temperature = np.max(destination_heat)
    for i in range(destination_heat.shape[0]):
        for j in range(destination_heat.shape[1]):
            if destination_heat[i, j] < min_temperature and destination_heat[i, j] > 0:
                min_temperature = destination_heat[i, j]
    print(min_temperature)


def part2():
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    allowed_directions = [
        [0, 2, 3],
        [1, 2, 3],
        [0, 1, 2],
        [0, 1, 3],
    ]

    
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        # print(lines)
        nrows = len(lines)
        ncols = len(lines[0].strip())

        heat_matrix = np.zeros((nrows, ncols), dtype = np.int8)

        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip()):
                heat_matrix[i, j] = int(c)

    ndirections = len(directions)
    nsteps_min = 4
    nsteps_max = 10
    coolest_paths = -np.ones((ndirections, nsteps_max + 1, nrows, ncols), dtype = int)
    cummulative_visits = np.zeros((nrows, ncols), dtype = int)

    v1 = (0, 1, 1, 0)
    v2 = (2, 1, 0, 1)
    coolest_paths[:, :, 0, 0] = 0
    coolest_paths[v1] = heat_matrix[1, 0]
    coolest_paths[v2] = heat_matrix[0, 1]

    active_vertices = [v1, v2]
    already_added = np.zeros((coolest_paths.shape[0], coolest_paths.shape[1], coolest_paths.shape[2], coolest_paths.shape[3]), dtype = np.int8)
    while len(active_vertices) > 0:
        new_active_vertices = []
        already_added.fill(0)

        for u in active_vertices:
            u_val = coolest_paths[u]
            u_direction = u[0]
            u_steps = u[1]
            u_row = u[2]
            u_col = u[3]
            cummulative_visits[u_row, u_col] += 1

            if u_steps < nsteps_min:
                v_direction = u_direction
                direction = directions[v_direction]
                v_row = direction[0] + u_row
                v_col = direction[1] + u_col
                v_steps = 1 + u_steps
                if (v_row < 0 or v_row >= nrows) or (v_col < 0 or v_col >= ncols):
                    continue

                heat_increment = heat_matrix[v_row, v_col]
                v_heat = coolest_paths[v_direction, v_steps, v_row, v_col]
                if v_heat < 0 or (v_heat >= heat_increment + u_val):
                    coolest_paths[v_direction, v_steps, v_row, v_col] = heat_increment + u_val

                    if already_added[v_direction, v_steps, v_row, v_col] == 0:
                        new_active_vertices.append((v_direction, v_steps, v_row, v_col))
                        already_added[v_direction, v_steps, v_row, v_col] = 1
            else:
                for v_direction in allowed_directions[u_direction]:
                    direction = directions[v_direction]
                    v_row = direction[0] + u_row
                    v_col = direction[1] + u_col
                    v_steps = 1
                    if u_direction == v_direction:
                        v_steps += u_steps

                    if (v_row < 0 or v_row >= nrows) or (v_col < 0 or v_col >= ncols) or v_steps > nsteps_max:
                        continue

                    heat_increment = heat_matrix[v_row, v_col]
                    v_heat = coolest_paths[v_direction, v_steps, v_row, v_col]
                    if v_heat < 0 or (v_heat >= heat_increment + u_val):
                        coolest_paths[v_direction, v_steps, v_row, v_col] = heat_increment + u_val

                        if already_added[v_direction, v_steps, v_row, v_col] == 0:
                            new_active_vertices.append((v_direction, v_steps, v_row, v_col))
                            already_added[v_direction, v_steps, v_row, v_col] = 1

        active_vertices = new_active_vertices
    # print(cummulative_visits)

    destination_heat = coolest_paths[:, :, -1, -1]
    min_temperature = np.max(destination_heat)
    for i in range(destination_heat.shape[0]):
        for j in range(destination_heat.shape[1]):
            if destination_heat[i, j] < min_temperature and destination_heat[i, j] > 0:
                min_temperature = destination_heat[i, j]
    print(min_temperature)

# part1()
part2()
# part1exp2()