import numpy as np

dir_changes = {}
dir_changes['.'] = {}
dir_changes['.'][(1, 0)] = [(1, 0)]
dir_changes['.'][(-1, 0)] = [(-1, 0)]
dir_changes['.'][(0, 1)] = [(0, 1)]
dir_changes['.'][(0, -1)] = [(0, -1)]

dir_changes['/'] = {}
dir_changes['/'][(1, 0)] = [(0, -1)]
dir_changes['/'][(-1, 0)] = [(0, 1)]
dir_changes['/'][(0, 1)] = [(-1, 0)]
dir_changes['/'][(0, -1)] = [(1, 0)]

dir_changes['\\'] = {}
dir_changes['\\'][(1, 0)] = [(0, 1)]
dir_changes['\\'][(-1, 0)] = [(0, -1)]
dir_changes['\\'][(0, 1)] = [(1, 0)]
dir_changes['\\'][(0, -1)] = [(-1, 0)]

dir_changes['|'] = {}
dir_changes['|'][(1, 0)] = [(1, 0)]
dir_changes['|'][(-1, 0)] = [(-1, 0)]
dir_changes['|'][(0, 1)] = [(1, 0), (-1, 0)]
dir_changes['|'][(0, -1)] = [(1, 0), (-1, 0)]

dir_changes['-'] = {}
dir_changes['-'][(1, 0)] = [(0, 1), (0, -1)]
dir_changes['-'][(-1, 0)] = [(0, 1), (0, -1)]
dir_changes['-'][(0, 1)] = [(0, 1)]
dir_changes['-'][(0, -1)] = [(0, -1)]

def get_n_energized(field_, starting_node, starting_direction):
    field = field_.copy()
    nrows = len(field)
    ncols = len(field[0])
    energized_fields = np.zeros((nrows, ncols), dtype = int)
    visited_states = np.zeros((nrows, ncols, 3, 3), dtype = int)

    active_set = [(starting_node, starting_direction)]
    while len(active_set) > 0:
        active_set_new = []

        for ucoords, udir in active_set:
            vcoords = (ucoords[0] + udir[0], ucoords[1] + udir[1])
            
            if vcoords[0] < 0 or vcoords[1] < 0 or vcoords[0] >= nrows or vcoords[1] >= ncols:
                continue
            energized_fields[vcoords] = 1

            for vdir in dir_changes[field[vcoords[0]][vcoords[1]]][udir]:
                if visited_states[vcoords[0], vcoords[1], vdir[0] + 1, vdir[1] + 1] == 1:
                    continue
                
                # print(vcoords, vdir, end = '')
                visited_states[vcoords[0], vcoords[1], vdir[0] + 1, vdir[1] + 1] = 1
                active_set_new.append((vcoords, vdir))
            # print()
        active_set = active_set_new

    # print(field)
    # print(energized_fields)
    return np.sum(energized_fields)

def part1():

    field = []
    nrows_max = 999999
    ncols_max = 999999
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        nrows = min(len(lines), nrows_max)
        ncols = min(len(lines[0].strip()), ncols_max)

        field = [line.strip()[:ncols] for line in lines[:nrows]]

    print(get_n_energized(field, (0, -1), (0, 1)))

def part2():

    field = []
    nrows_max = 999999
    ncols_max = 999999
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        nrows = min(len(lines), nrows_max)
        ncols = min(len(lines[0].strip()), ncols_max)

        field = [line.strip()[:ncols] for line in lines[:nrows]]


    answer = 0
    c = -1
    for r in range(nrows):
        tmp = get_n_energized(field, (r, c), (0, 1))
        if tmp > answer:
            answer = tmp

    c = ncols
    for r in range(nrows):
        tmp = get_n_energized(field, (r, c), (0, -1))
        if tmp > answer:
            answer = tmp
    r = -1
    for c in range(ncols):
        tmp = get_n_energized(field, (r, c), (1, 0))
        if tmp > answer:
            answer = tmp
            
    r = nrows
    for c in range(ncols):
        tmp = get_n_energized(field, (r, c), (-1, 0))
        if tmp > answer:
            answer = tmp
            
    print(answer)
        

# part1()
part2()



