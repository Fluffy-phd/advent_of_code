import numpy as np
from functools import cmp_to_key

def cmp(a, b):
    # print(a[2], b[2], end = '')
    if a[2, 0] < b[2, 0]:
        # print(a[2], ' < ', b[2])
        return -1
    
    if a[2, 0] > b[2, 0]:
        # print(a[2], ' > ', b[2])
        return 1
    # print(a[2], ' = ', b[2])
    return 0

def part1():
    answer = 0

    segments = []
    xmax = 0
    ymax = 0
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            p = line.strip().split('~')
            u = [int(i.strip()) for i in p[0].split(',')]
            v = [int(i.strip()) for i in p[1].split(',')]
            # print(u, v)

            coords = np.zeros((3, 2), dtype = int)
            for i in range(3):
                coords[i, 0] = min(u[i], v[i])
                coords[i, 1] = max(u[i], v[i]) + 1

            
            xmax = max(xmax, coords[0, 1])
            ymax = max(ymax, coords[1, 1])
            segments.append(coords)

    
    # print(segments)
    xmax += 1
    ymax += 1

    segments = sorted(segments, key=cmp_to_key(cmp))
    height_map = np.zeros((xmax, ymax), dtype = int)
    top_brick = -np.ones((xmax, ymax), dtype = int)

    nsegments = len(segments)
    supporting_segments_in = [[] for _ in range(nsegments)]
    supporting_segments_out = [[] for _ in range(nsegments)]

    # print(height_map)
    for idx, segment in enumerate(segments):
        #highest point lying under this segment
        X = segment[0]
        Y = segment[1]
        Z = segment[2]
        HEIGHT = Z[1] - Z[0]
        
        supporting_map = height_map[X[0]:X[1], Y[0]:Y[1]].reshape(-1)
        supporting_bricks = top_brick[X[0]:X[1], Y[0]:Y[1]].reshape(-1)
        high_point = np.max(height_map[X[0]:X[1], Y[0]:Y[1]])

        if high_point > 0:
            for i_, h_ in enumerate(supporting_map):
                if h_ == high_point:
                    if supporting_bricks[i_] not in supporting_segments_in[idx]:
                        supporting_segments_in[idx].append(supporting_bricks[i_])

                        if idx not in supporting_segments_out[supporting_bricks[i_]]:
                            supporting_segments_out[supporting_bricks[i_]].append(idx)


        # print(segment, high_point)
        height_map[X[0]:X[1], Y[0]:Y[1]] = (HEIGHT + high_point)
        top_brick[X[0]:X[1], Y[0]:Y[1]] = idx
        # print(height_map, segment)
    # print(xmax, ymax)

    print(supporting_segments_in)
    print(supporting_segments_out)

    for u in range(nsegments):
        can_disintegrate = True
        for v in supporting_segments_out[u]:
            if len(supporting_segments_in[v]) == 1:
                can_disintegrate = False
                break
        if can_disintegrate:
            answer += 1



    print(answer)

def part2():
    answer = 0

    segments = []
    xmax = 0
    ymax = 0
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            p = line.strip().split('~')
            u = [int(i.strip()) for i in p[0].split(',')]
            v = [int(i.strip()) for i in p[1].split(',')]
            # print(u, v)

            coords = np.zeros((3, 2), dtype = int)
            for i in range(3):
                coords[i, 0] = min(u[i], v[i])
                coords[i, 1] = max(u[i], v[i]) + 1

            
            xmax = max(xmax, coords[0, 1])
            ymax = max(ymax, coords[1, 1])
            segments.append(coords)

    
    # print(segments)
    xmax += 1
    ymax += 1

    segments = sorted(segments, key=cmp_to_key(cmp))
    height_map = np.zeros((xmax, ymax), dtype = int)
    top_brick = -np.ones((xmax, ymax), dtype = int)

    nsegments = len(segments)
    supporting_segments_in = [[] for _ in range(nsegments)]
    supporting_segments_out = [[] for _ in range(nsegments)]

    # print(height_map)
    for idx, segment in enumerate(segments):
        #highest point lying under this segment
        X = segment[0]
        Y = segment[1]
        Z = segment[2]
        HEIGHT = Z[1] - Z[0]
        
        supporting_map = height_map[X[0]:X[1], Y[0]:Y[1]].reshape(-1)
        supporting_bricks = top_brick[X[0]:X[1], Y[0]:Y[1]].reshape(-1)
        high_point = np.max(height_map[X[0]:X[1], Y[0]:Y[1]])

        if high_point > 0:
            for i_, h_ in enumerate(supporting_map):
                if h_ == high_point:
                    if supporting_bricks[i_] not in supporting_segments_in[idx]:
                        supporting_segments_in[idx].append(supporting_bricks[i_])

                        if idx not in supporting_segments_out[supporting_bricks[i_]]:
                            supporting_segments_out[supporting_bricks[i_]].append(idx)


        # print(segment, high_point)
        height_map[X[0]:X[1], Y[0]:Y[1]] = (HEIGHT + high_point)
        top_brick[X[0]:X[1], Y[0]:Y[1]] = idx
        # print(height_map, segment)
    # print(xmax, ymax)

    # print(supporting_segments_in)
    # print(supporting_segments_out)


    how_many_bricks_would_fall = -np.ones(nsegments, dtype = int)
   
    for i in range(nsegments):

        active_set = [i]

        fallen_bricks = np.zeros(nsegments, dtype = int)
        fallen_bricks[i] = 1

        while len(active_set) > 0:
            active_set_new = []

            for u in active_set:
                for v in supporting_segments_out[u]:
                    vhasfallen = True
                    for w in supporting_segments_in[v]:
                        if fallen_bricks[w] == False:
                            vhasfallen = False
                            break
                    if vhasfallen and fallen_bricks[v] == 0:
                        fallen_bricks[v] = 1
                        active_set_new.append(v)


            active_set = active_set_new


        answer += np.sum(fallen_bricks) - 1
        



    print(answer)
# part1()

part2()