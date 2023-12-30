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

# goes to the left
def go(arr):
    n = len(arr)
    nempty_spaces = 0
    nboulders = 0
    available_empty_space_idx = 0
    out = np.zeros(n, dtype = arr.dtype)
    for i in range(n):
        if arr[i] == 1:
            out[i] = 1

    idx = 0
    while idx < n:
        while arr[idx] == 1:
            idx += 1
            if idx >= n:
                break
        if idx >= n:
            break
        available_empty_space_idx = idx

        while arr[idx] == 0 or arr[idx] == 2:
            if arr[idx] == 2:
                nboulders += 1
            nempty_spaces += 1
            idx += 1
            if idx >= n:
                break

        if nboulders > 0:
            out[available_empty_space_idx:available_empty_space_idx + nboulders] = 2
            nboulders = 0
            nempty_spaces = 0
    return out

def go_north(platform):
    platform_tmp = platform.copy()
    ncols = platform.shape[1]

    for i in range(ncols):
        platform_tmp[:, i] = go(platform[:, i])

    return platform_tmp

def go_south(platform):
    platform_tmp = platform.copy()
    ncols = platform.shape[1]

    for i in range(ncols):
        platform_tmp[:, i] = np.flip(go(np.flip(platform[:, i])))

    return platform_tmp

def go_east(platform):
    platform_tmp = platform.copy()
    nrows = platform.shape[0]

    for i in range(nrows):
        platform_tmp[i, :] = np.flip(go(np.flip(platform[i, :])))

    return platform_tmp

def go_west(platform):
    platform_tmp = platform.copy()
    nrows = platform.shape[0]

    for i in range(nrows):
        platform_tmp[i, :] = go(platform[i, :])

    return platform_tmp

def printp(M):
    char_map = {}
    char_map[0] = '.'
    char_map[1] = '#'
    char_map[2] = 'O'

    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            print(char_map[M[i, j]], end = '')
        print()
    print()

def part2_column_score(M):

    out = [0 for _ in range(M.shape[1])]
    for c in range(M.shape[1]):
        for r in range(M.shape[0]):
            if M[r, c] == 2:
                out[c] += M.shape[0] - r
    return tuple(out)

def part2():

    nrows = 0
    ncols = 0
    with open('input.txt', 'r') as f:

        char_map = {}
        char_map['.'] = 0
        char_map['#'] = 1
        char_map['O'] = 2
        
        lines = f.readlines()
        # print(lines)
        nrows = len(lines)
        ncols = len(lines[0].strip())
        platform = np.zeros((nrows, ncols), dtype = int)
        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip()):
                platform[i, j] = char_map[c]

    history = {}

    idx = 0
    chain_length = 0
    chain_first_element = 0
    loads = []
    while True:
        platform = go_north(platform)
        platform = go_west(platform)
        platform = go_south(platform)
        platform = go_east(platform)

        tmp = part2_column_score(platform)
        if tmp not in history:
            history[tmp] = idx
            loads.append(tmp)
            # print(idx, tmp, np.sum(tmp))
        else:
            chain_first_element = history[tmp]
            chain_length = idx - chain_first_element
            break
        idx += 1
    print('tail length:', chain_first_element)
    print('chain length: ', chain_length)

    ncycles = 1000000000
    # ncycles = 10
    if ncycles <= chain_first_element:
        print(ncycles - 1, loads[ncycles - 1], np.sum(loads[ncycles - 1]))
    else:
        ncycles -= (chain_first_element + 1)
        ncycles = ncycles % chain_length + chain_first_element
        print(ncycles, loads[ncycles], np.sum(loads[ncycles]))

part1()

part2()