import numpy as np

def get_distance(col_lens, row_lens, U, V):
    row_start = min(U[0], V[0])
    row_end = max(U[0], V[0]) + 1
    # print('rows:', row_start, row_end)

    col_start = min(U[1], V[1])
    col_end = max(U[1], V[1]) + 1
    # print('cols:', col_start, col_end)

    row_distance = 0
    
    for u in range(row_start + 1, row_end):
        row_distance += row_lens[u]

    col_distance = 0
    for u in range(col_start + 1, col_end):
        col_distance += col_lens[u]

    # print(row_distance, col_distance)

    return row_distance + col_distance

def part1():

    with open('input.txt', 'r') as f:
        lines = f.readlines()
        ncols = len(lines[0].strip())
        nrows = len(lines)
        map_ = np.zeros((nrows, ncols), dtype = int)
        col_lens_ = np.ones(ncols, dtype = int)
        row_lens_ = np.ones(nrows, dtype = int)

        for row_idx, line in enumerate(lines):
            for col_idx, c in enumerate(line):
                if c == '#':
                    map_[row_idx, col_idx] = 1

    for i in range(len(col_lens_)):
        if np.sum(map_[:, i]) == 0:
              col_lens_[i] = 2
    for i in range(len(row_lens_)):
        if np.sum(map_[i, :]) == 0:
              row_lens_[i] = 2
    

    # print(col_lens_, row_lens_, map_)
    stations = []
    for i in range(map_.shape[0]):
        for j in range(map_.shape[1]):
            if map_[i, j] > 0:
                stations.append((i, j))
    nstations = len(stations)
    # print(stations)
    
    # tmp_ = get_distance(col_lens_, row_lens_, stations[4], stations[8])

    answer = 0
    for i in range(nstations):
        for j in range(i + 1, nstations):
            tmp_ = get_distance(col_lens_, row_lens_, stations[i], stations[j])
            # print(stations[i], stations[j], tmp_)
            answer += tmp_
    print(answer)

    # map__ = np.zeros((1 + map_.shape[0], 1 + map_.shape[1]), dtype = int)
    # map__[1:, 0] = row_lens_
    # map__[0, 1:] = col_lens_
    # map__[1:, 1:] = map_

    # print(map__)

def part2():

    with open('input.txt', 'r') as f:
        lines = f.readlines()
        ncols = len(lines[0].strip())
        nrows = len(lines)
        map_ = np.zeros((nrows, ncols), dtype = int)
        col_lens_ = np.ones(ncols, dtype = int)
        row_lens_ = np.ones(nrows, dtype = int)

        for row_idx, line in enumerate(lines):
            for col_idx, c in enumerate(line):
                if c == '#':
                    map_[row_idx, col_idx] = 1

    for i in range(len(col_lens_)):
        if np.sum(map_[:, i]) == 0:
              col_lens_[i] = 1000000
    for i in range(len(row_lens_)):
        if np.sum(map_[i, :]) == 0:
              row_lens_[i] = 1000000
    

    # print(col_lens_, row_lens_, map_)
    stations = []
    for i in range(map_.shape[0]):
        for j in range(map_.shape[1]):
            if map_[i, j] > 0:
                stations.append((i, j))
    nstations = len(stations)
    # print(stations)
    
    # tmp_ = get_distance(col_lens_, row_lens_, stations[4], stations[8])

    answer = 0
    for i in range(nstations):
        for j in range(i + 1, nstations):
            tmp_ = get_distance(col_lens_, row_lens_, stations[i], stations[j])
            # print(stations[i], stations[j], tmp_)
            answer += tmp_
    print(answer)

    # map__ = np.zeros((1 + map_.shape[0], 1 + map_.shape[1]), dtype = int)
    # map__[1:, 0] = row_lens_
    # map__[0, 1:] = col_lens_
    # map__[1:, 1:] = map_

    # print(map__)






part1()
part2()