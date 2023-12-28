import numpy as np

def part1():

    char_map = {}
    char_map['|'] = [(-1, 0), (1, 0)]
    char_map['-'] = [(0, -1), (0, 1)]
    char_map['L'] = [(-1, 0), (0, 1)]
    char_map['J'] = [(-1, 0), (0, -1)]
    char_map['7'] = [(0, -1), (1, 0)]
    char_map['F'] = [(0, 1), (1, 0)]
    char_map['.'] = [(0, 0)]
    char_map['S'] = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        nrows = len(lines)
        ncols = len(lines[0].strip())
        nnodes = nrows * ncols
        coord2node = np.zeros((nrows, ncols), dtype = int)
        node2coord = []
        neighbors = [[] for u in range(nnodes)]

        for i in range(nrows):
            for j in range(ncols):
                coord2node[i, j] = j + i * ncols
                node2coord.append((i, j))


        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip()):
                dirs = char_map[c]

                u = coord2node[i, j]
                if c == 'S':
                    starting_node = u

                for d in dirs:
                    new_pos = (i + d[0], j + d[1])
                    if new_pos[0] < 0 or new_pos[0] >= nrows:
                        continue
                    if new_pos[1] < 0 or new_pos[1] >= ncols:
                        continue
                    v = coord2node[new_pos[0], new_pos[1]]

                    neighbors[u].append((v, 1))
    
    # cleanup the relations
    cleanup = True
    npruning_cycles = 0
    while cleanup:
        cleanup = False
        npruning_cycles += 1
        # ignore vertices with less then two neighbors
        neighbors_ = []
        for u in neighbors:
            if len(u) > 1:
                neighbors_.append(u)
            else:
                neighbors_.append([])
                if len(u) > 0:
                    cleanup = True

        # remove neighbors which do not point back towards particular vertices
        neighbors = []
        for u in range(nnodes):
            Nu = []
            # print(u)
            for V in neighbors_[u]:
                v = V[0]

                issymmetric = False
                for U in neighbors_[v]:
                    if U[0] == u:
                        issymmetric = True
                        break
                
                if issymmetric:
                    Nu.append(V)
                else:
                    cleanup = True
            neighbors.append(Nu)

    print('number of pruning cycles:', npruning_cycles)
    print(starting_node)
    # print(neighbors)
    #now contract edges
    contractedges = True
    while contractedges:
        contractedges = False

        for u in range(nnodes):
            if u == starting_node or len(neighbors[u]) == 0:
                continue
            
            # print(u, neighbors[u])

            V1 = neighbors[u].pop()
            v1 = V1[0]
            duv1 = V1[1]

            V2 = neighbors[u].pop()
            v2 = V2[0]
            duv2 = V2[1]

            # print(u, neighbors[u], neighbors[v1], neighbors[v2])

            if len(neighbors[v1]) > 0:
                idx2remove1 = -1
                for i, U in enumerate(neighbors[v1]):
                    if U[0] == u:
                        idx2remove1 = i
                        break
                neighbors[v1].pop(idx2remove1)

            if len(neighbors[v2]) > 0:
                idx2remove2 = -1
                for i, U in enumerate(neighbors[v2]):
                    if U[0] == u:
                        idx2remove2 = i
                        break
                neighbors[v2].pop(idx2remove2)

            neighbors[v1].append((v2, duv1 + duv2))
            neighbors[v2].append((v1, duv1 + duv2))




            
        


    #contract edges
    print('cycle length', neighbors[starting_node][0][1])
    print('answer', neighbors[starting_node][0][1] /2 )




def flood_fill(A, s, v):
    nrows = A.shape[0]
    ncols = A.shape[1]

    active_nodes = [s]
    A[s] = 1

    while len(active_nodes) > 0:
        active_nodes_new = []

        for u in active_nodes:
            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                v = (u[0] + shift[0], u[1] + shift[1])

                if v[0] < 0 or v[1] < 0 or v[0] >= nrows or v[1] >= ncols:
                    continue

                if A[v] == 0:
                    A[v] = 1
                    active_nodes_new.append(v)

        active_nodes = active_nodes_new

def part2():

    char_map = {}
    char_map['|'] = [(-1, 0), (1, 0)]
    char_map['-'] = [(0, -1), (0, 1)]
    char_map['L'] = [(-1, 0), (0, 1)]
    char_map['J'] = [(-1, 0), (0, -1)]
    char_map['7'] = [(0, -1), (1, 0)]
    char_map['F'] = [(0, 1), (1, 0)]
    char_map['.'] = []
    char_map['S'] = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        nrows = len(lines) * 2
        ncols = len(lines[0].strip()) * 2
        nnodes = nrows * ncols
        coord2node = np.zeros((nrows, ncols), dtype = int)
        node2coord = []
        neighbors = [[] for u in range(nnodes)]

        for i in range(nrows):
            for j in range(ncols):
                coord2node[i, j] = len(node2coord)
                node2coord.append((i, j))


        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip()):
                dirs = char_map[c]

                ii = 2*i
                jj = 2*j
                u = coord2node[ii, jj]
                if c == 'S':
                    starting_node = u

                for d in dirs:
                    new_pos = (ii + d[0], jj + d[1])
                    if new_pos[0] < 0 or new_pos[0] >= nrows or new_pos[1] < 0 or new_pos[1] >= ncols:
                        continue
                    v = coord2node[new_pos[0], new_pos[1]]

                    neighbors[u].append(v)
        for c in range(ncols//2):
            j = 2*c + 1
            for r in range(nrows):
                
                u = coord2node[r, j]
                for d in char_map['-']:
                    new_pos = (r + d[0], j + d[1])
                    if new_pos[0] < 0 or new_pos[0] >= nrows or new_pos[1] < 0 or new_pos[1] >= ncols:
                        continue
                    v = coord2node[new_pos[0], new_pos[1]]

                    neighbors[u].append(v)
    
        for c in range(ncols//2):
            j = 2*c
            for rr in range(nrows//2):
                r = 2*rr + 1
                
                u = coord2node[r, j]
                for d in char_map['|']:
                    new_pos = (r + d[0], j + d[1])
                    if new_pos[0] < 0 or new_pos[0] >= nrows or new_pos[1] < 0 or new_pos[1] >= ncols:
                        continue
                    v = coord2node[new_pos[0], new_pos[1]]

                    neighbors[u].append(v)
    

    # cleanup the relations
    cleanup = True
    npruning_cycles = 0
    while cleanup:
        cleanup = False
        npruning_cycles += 1
        # ignore vertices with less then two neighbors
        neighbors_ = []
        for u in neighbors:
            if len(u) > 1:
                neighbors_.append(u)
            else:
                neighbors_.append([])
                if len(u) > 0:
                    cleanup = True

        # remove neighbors which do not point back towards particular vertices
        neighbors = []
        for u in range(nnodes):
            Nu = []
            # print(u)
            for v in neighbors_[u]:
                issymmetric = False
                for w in neighbors_[v]:
                    if w == u:
                        issymmetric = True
                        break
                
                if issymmetric:
                    Nu.append(v)
                else:
                    cleanup = True
            neighbors.append(Nu)

    # print(neighbors[starting_node])
    active_nodes = [neighbors[starting_node][0]]
    visited_nodes = np.zeros(nnodes, dtype = int)
    visited_nodes[starting_node] = 1
    field_map = np.zeros((nrows, ncols), dtype = int)
    field_map[node2coord[starting_node]] = 1

    while len(active_nodes) > 0:
        active_nodes_new = []

        for u in active_nodes:
            for v in neighbors[u]:
                if visited_nodes[v] == 0:
                    visited_nodes[v] = 1
                    active_nodes_new.append(v)
                    field_map[node2coord[v]] = 1

        active_nodes = active_nodes_new

    for c in range(ncols):
        flood_fill(field_map, (0, c), 1)
        flood_fill(field_map, (nrows - 1, c), 1)
    for r in range(nrows):
        flood_fill(field_map, (r, 0), 1)
        flood_fill(field_map, (r, ncols - 1), 1)
    
    #contract the map
    field_map = field_map[:, ::2]
    field_map = field_map[::2, :]
    # print(field_map)

    answer = 0
    for c in field_map.reshape(-1):
        if c == 0:
            answer += 1
    print(answer)
# part1()
part2()