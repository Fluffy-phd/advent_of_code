import numpy as np

def get_column_score(col):
    rolling_sets = []
    nstones = 0
    n = len(col)
    shift = n
    for i, c in enumerate(col):
        if c == '#':
            if nstones > 0:
                rolling_sets.append((shift, nstones))
            shift = n - i - 1
            nstones = 0
        elif c == 'O':
            nstones += 1
    if nstones > 0:
        rolling_sets.append((shift, nstones))

    out = 0
    for s in rolling_sets:
        nstones = s[1]
        max_reward = s[0]

        for i in range(nstones):
            out += max_reward - i

    # print(col, rolling_sets, out)
    return out
    
def part1():

    platform_rows = []
    nrows = 0
    ncols = 0
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        # print(lines)
        nrows = len(lines)
        ncols = len(lines[0].strip())
        for line in lines:
            platform_rows.append(line.strip())

    platform_cols = []
    # print(platform_rows)

    for c in range(ncols):
        col = ''
        for r in range(nrows):
            col += platform_rows[r][c]
        platform_cols.append(col)

    answer = 0
    for col in platform_cols:
        answer += get_column_score(col)
    print(answer)

def go_north_column(column):
    for i in range(ncols):
        platform_tmp[:, i] = go_north_column(platform[:, i])

    return platform_tmp


def go_north(platform):
    platform_tmp = platform.copy()
    nrows = platform.shape[0]
    ncols = platform.shape[1]

    for i in range(ncols):
        platform_tmp[:, i] = go_north_column(platform[:, i])

    return platform_tmp

def part2():

    nrows = 0
    ncols = 0
    with open('input2.txt', 'r') as f:
        lines = f.readlines()
        # print(lines)
        nrows = len(lines)
        ncols = len(lines[0].strip())
        platform = np.zeros((nrows, ncols), dtype = str)
        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip()):
                platform[i, j] = c


    print(platform)

    platform = go_north(platform)

part1()

part2()