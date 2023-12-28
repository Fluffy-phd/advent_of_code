import numpy as np

def find_max_flow_min_cut(s, t, N):
    nvertices = len(N)
    residual_capacity = np.zeros((nvertices, nvertices), dtype = int)
    residual_flow = np.zeros((nvertices, nvertices), dtype = int)
    for u in range(nvertices):
        for v in N[u]:
            residual_capacity[u, v] = 1
            residual_capacity[v, u] = 1


    continue_looking = True
    max_flow = 0

    while continue_looking:
        continue_looking = False

        active_vertices = [s]
        distances = -np.ones(nvertices, dtype = int)
        distances[s] = 0
        current_distance = 0
        while len(active_vertices) > 0:
            active_vertices_new = []
            current_distance += 1

            for u in active_vertices:
                if u == t:
                    break
                for v in N[u]:
                    if residual_capacity[u, v] - residual_flow[u, v] <= 0:
                        continue

                    if distances[v] > current_distance or distances[v] < 0:
                        distances[v] = current_distance
                        if v not in active_vertices_new:
                            active_vertices_new.append(v)
            active_vertices = active_vertices_new

        if distances[t] > 0:
            continue_looking = True
            max_flow += 1
        
        # alter residual graph edges
        av = t
        # print('found distance', distances[t])
        while distances[av] > 0:
            for u in N[av]:
                if distances[u] == distances[av] - 1:
                    residual_flow[u, av] += 1
                    residual_flow[av, u] -= 1
                    av = u
                    break
    
    if max_flow != 3:
        return 0
    
    S = [s]
    Sv = np.zeros(nvertices, dtype = int)
    Av = np.zeros(nvertices, dtype = int)
    active_vertices = [s]
    Sv[s] = 1
    while len(active_vertices) > 0:
        active_vertices_new = []

        for u in active_vertices:
            for v in N[u]:
                if residual_capacity[u, v] - residual_flow[u, v] <= 0:
                    continue

                if Av[v] == 0:
                    Av[v] = 1
                    active_vertices_new.append(v)
                if Sv[v] == 0:
                    Sv[v] = 1
                    S.append(v)

        active_vertices = active_vertices_new

    return len(S) * (nvertices - len(S))


def part1():

    with open('input2.txt', 'r') as f:
        lines = f.readlines()

        vertices_neighbors = {}
        vertex_map = {}

        for line in lines:
            tmp = line.strip().split(':')
            src = tmp[0].strip()
            targets = [u.strip() for u in tmp[1].split()]

            # print(src, targets)

            if src not in vertex_map:
                vertex_map[src] = len(vertex_map)
                vertices_neighbors[src] = []
            

            for tgt in targets:
                if tgt not in vertex_map:
                    vertex_map[tgt] = len(vertex_map)
                    vertices_neighbors[tgt] = []
                vertices_neighbors[src].append(tgt)
                vertices_neighbors[tgt].append(src)
        
        nvertices = len(vertex_map)
        neighbours = [[] for _ in range(nvertices)]
        for u in vertices_neighbors:
            U = vertex_map[u]
            Nu = vertices_neighbors[u]

            for v in Nu:
                V = vertex_map[v]
                if V not in neighbours[U]:
                    neighbours[U].append(V)
            neighbours[U].sort()

            # print(u, U, neighbours[U])

        # print(neighbours)
    
    answer = 0
    for s in range(nvertices - 1):
        for t in range(s + 1, nvertices):
            answer_tmp = find_max_flow_min_cut(s, t, neighbours)
            if answer_tmp > 0:
                print(answer_tmp)
                return
    #         if answer <= 0 or answer > answer_tmp:
    #             answer = answer_tmp
    # print(answer)


def part2():
    pass



part1()
part2()
