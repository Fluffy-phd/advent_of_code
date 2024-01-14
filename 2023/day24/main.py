import numpy as np
import matplotlib.pyplot as plt


def intersects(u, v, x, y, z):

    upos = u[0]
    udir = u[1]

    vpos = v[0]
    vdir = v[1]
    print('comparing ', u, v, end = '')

    # upos + a*udir = vpos + b*vdir
    A = np.array([[udir[0], -vdir[0]], [udir[1], -vdir[1]]])
    b = np.array([vpos[0] - upos[0], vpos[1] - upos[1]])
    if np.linalg.matrix_rank(A) < 2:
        print('rovnobezne')
        return False

    # print(A)
    r = np.linalg.solve(A, b)

    if r[0] < 0 or r[1] < 0:
        print('mimo (v case zpet)')
        return False

    U = (upos[0] + udir[0] * r[0], upos[1] + udir[1] * r[0])
    V = (vpos[0] + vdir[0] * r[1], vpos[1] + vdir[1] * r[1])

    if U[0] < x[0] or U[0] > x[1] or U[1] < y[0] or U[1] > y[1]:
        print('mimo (oblast)')
        return False

    if V[0] < x[0] or V[0] > x[1] or V[1] < y[0] or V[1] > y[1]:
        print('mimo (oblast)')
        return False

    print()
    return True

def intersects_in_time(u, v, x, y, z):

    upos = u[0]
    udir = u[1]

    vpos = v[0]
    vdir = v[1]
    # print('comparing ', u, v, end = '')

    #x intersect
    # upos[x] = vpos[x] + t*vdir[x]
    # -> upos[x] - vpos[x] = t*(vdir[x] - udir[x])
    # -> t = (upos[x] - vpos[x]) / (vdir[x] - udir[x])
    tx = 0
    if (vdir[0] - udir[0]) != 0:
        tx = (upos[0] - vpos[0]) / (vdir[0] - udir[0])

    ty = 0
    if (vdir[1] - udir[1]) != 0:
        ty = (upos[1] - vpos[1]) / (vdir[1] - udir[1])

    tz = 0
    if (vdir[2] - udir[2]) != 0:
        tz = (upos[2] - vpos[2]) / (vdir[2] - udir[2])


    if abs(tx -tz) <= 1e-6 or abs(ty -tz) <= 1e-6 or abs(tx -ty) <= 1e-6:
        print(tx, ty, tz)

    

def part1():

    hailstone_paths = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            tmp = line.strip().split('@')
            pos = [int(v) for v in tmp[0].split(',')]
            vel = [int(v) for v in tmp[1].split(',')]
            hailstone_paths.append([pos, vel])


    nhailstones = len(hailstone_paths)
    answer = 0
    for i in range(nhailstones):
        for j in range(i + 1, nhailstones):
            if intersects(hailstone_paths[i], hailstone_paths[j], x = (200000000000000, 400000000000000), y = (200000000000000, 400000000000000), z = (-np.inf, np.inf)):
                answer += 1
    print(answer)

def print_analysis(positionas, pic_fn, min_max):
    pass

def part2():

    hailstone_paths_x = []
    hailstone_paths_y = []
    hailstone_paths_z = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            tmp = line.strip().split('@')
            pos = [int(v) for v in tmp[0].split(',')]
            vel = [int(v) for v in tmp[1].split(',')]
            hailstone_paths_x.append([pos[0], vel[0]])
            hailstone_paths_y.append([pos[1], vel[1]])
            hailstone_paths_z.append([pos[2], vel[2]])

    print_analysis(hailstone_paths_x, 'x.png', [7, 27])


    # nhailstones = len(hailstone_paths)
    # answer = 0
    # for i in range(nhailstones):
    #     for j in range(i + 1, nhailstones):
    #         intersects_in_time(hailstone_paths[i], hailstone_paths[j], x = (200000000000000, 400000000000000), y = (200000000000000, 400000000000000), z = (200000000000000, 400000000000000))
    # print(answer)

# part1()
part2()