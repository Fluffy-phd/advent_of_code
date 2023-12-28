import numpy as np


paths_lengths = []
def run_dfs(neighbours_out, visited_vertices, us, ut, path_len):

    if us == ut:
        paths_lengths.append(path_len)
        return

    for v, l in neighbours_out[us]:
        if visited_vertices[v] == 1:
            continue

        visited_vertices[v] = 1

        run_dfs(neighbours_out, visited_vertices, v, ut, path_len + l)

        visited_vertices[v] = 0





def dfs(us, ut, neighbours_out):
    nvertices = len(neighbours_out)
    visited_vertices = np.zeros(nvertices, dtype = int)
    visited_vertices[us] = 1
    return run_dfs(neighbours_out, visited_vertices, us, ut, 0)
    


def part1():

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        nrows = len(lines)
        ncols = len(lines[0].strip())

        field = [line.strip() for line in lines]

    starting_tile = (0, 0)
    ending_tile = (nrows - 1, 0)
    for c in range(ncols):
        if field[0][c] == '.':
            starting_tile = (0, c)
        if field[nrows - 1][c] == '.':
            ending_tile = (nrows - 1, c)
    field[starting_tile[0]].replace('.', 'v')
    field[ending_tile[0]].replace('.', 'v')
    # print(starting_tile, ending_tile)

    # construct a directed graph
    coord2vertex_map = np.zeros((nrows, ncols), dtype = int)
    vertex2coords_map = []
    for r in range(nrows):
        for c in range(ncols):
            coord2vertex_map[r, c] = len(vertex2coords_map)
            vertex2coords_map.append((r, c))
    nvertices = len(vertex2coords_map)
    neighbours_out = [[] for _ in range(nvertices)]
    neighbours_in = [[] for _ in range(nvertices)]

    neighbours_out[coord2vertex_map[starting_tile]].append((coord2vertex_map[starting_tile[0] + 1, starting_tile[1]], 1))
    neighbours_in[coord2vertex_map[starting_tile[0] + 1, starting_tile[1]]].append((coord2vertex_map[starting_tile], 1))

    for r in range(1, nrows - 1):
        for c in range(1, ncols - 1):
            if field[r][c] == '#':
                continue

            u = coord2vertex_map[r, c]
            if field[r][c] == '.':
                for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    r_ = r + shift[0]
                    c_ = c + shift[1]
                    if field[r_][c_] != '#':
                        v = coord2vertex_map[r_, c_]
                        neighbours_out[u].append((v, 1))
                        neighbours_in[v].append((u, 1))
            elif field[r][c] == '>':
                if field[r][c + 1] != '#':
                    v = coord2vertex_map[r, c + 1]
                    neighbours_out[u].append((v, 1))
                    neighbours_in[v].append((u, 1))
            elif field[r][c] == '<':
                if field[r][c - 1] != '#':
                    v = coord2vertex_map[r, c - 1]
                    neighbours_out[u].append((v, 1))
                    neighbours_in[v].append((u, 1))
            elif field[r][c] == 'v':
                if field[r + 1][c] != '#':
                    v = coord2vertex_map[r + 1, c]
                    neighbours_out[u].append((v, 1))
                    neighbours_in[v].append((u, 1))

    # contract edges
    contract_edges = True
    ncontracted = 0
    while contract_edges:
        contract_edges = False

        for u in range(nvertices):
            r, c = vertex2coords_map[u]
            if field[r][c] != '.':
                continue
            if len(neighbours_out[u]) == 2:
                ncontracted += 1
                contract_edges = True

                #v - u - w
                v, vu = neighbours_out[u][0]
                w, uw = neighbours_out[u][1]

                neighbours_out[u] = []
                for j, u_ in enumerate(neighbours_out[v]):
                    if u_[0] == u:
                        neighbours_out[v][j] = (w, vu + uw)

                        for jj, uu_ in enumerate(neighbours_in[w]):
                            if uu_[0] == u:
                                neighbours_in[w][jj] = (v, vu + uw)
                                break
                        break

                for j, u_ in enumerate(neighbours_out[w]):
                    if u_[0] == u:
                        neighbours_out[w][j] = (v, vu + uw)

                        for jj, uu_ in enumerate(neighbours_in[v]):
                            if uu_[0] == u:
                                neighbours_in[v][jj] = (w, vu + uw)
                                break
                        break



                # print(v, u, w, neighbours_out[v], neighbours_in[w])
                # print(v, u, w, neighbours_out[v], neighbours_in[w])
                # print(v, u, w)
    print(ncontracted)

    # for u, nu in enumerate(neighbours_out):
    #     if len(nu) > 0:
    #         print(u, vertex2coords_map[u], nu)


    dfs(coord2vertex_map[starting_tile], coord2vertex_map[ending_tile], neighbours_out)
    # answer = dfs(field, starting_tile, ending_tile)
   

    # print(answer)

    answer = 0
    for pl in paths_lengths:
        answer = max(answer, pl)
    print(answer)
    

def part2():

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        nrows = len(lines)
        ncols = len(lines[0].strip())

        field = [line.strip() for line in lines]

    starting_tile = (0, 0)
    ending_tile = (nrows - 1, 0)
    for c in range(ncols):
        if field[0][c] == '.':
            starting_tile = (0, c)
        if field[nrows - 1][c] == '.':
            ending_tile = (nrows - 1, c)
    field[starting_tile[0]].replace('.', 'v')
    field[ending_tile[0]].replace('.', 'v')
    # print(starting_tile, ending_tile)

    # construct a directed graph
    coord2vertex_map = np.zeros((nrows, ncols), dtype = int)
    vertex2coords_map = []
    for r in range(nrows):
        for c in range(ncols):
            coord2vertex_map[r, c] = len(vertex2coords_map)
            vertex2coords_map.append((r, c))
    nvertices = len(vertex2coords_map)
    neighbours_out = [[] for _ in range(nvertices)]
    neighbours_in = [[] for _ in range(nvertices)]

    neighbours_out[coord2vertex_map[starting_tile]].append((coord2vertex_map[starting_tile[0] + 1, starting_tile[1]], 1))
    neighbours_in[coord2vertex_map[starting_tile[0] + 1, starting_tile[1]]].append((coord2vertex_map[starting_tile], 1))

    for r in range(1, nrows - 1):
        for c in range(1, ncols - 1):
            if field[r][c] == '#':
                continue

            u = coord2vertex_map[r, c]
            for shift in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                r_ = r + shift[0]
                c_ = c + shift[1]
                if field[r_][c_] != '#':
                    v = coord2vertex_map[r_, c_]
                    neighbours_out[u].append((v, 1))
                    neighbours_in[v].append((u, 1))

    # contract edges
    contract_edges = True
    ncontracted = 0
    while contract_edges:
        contract_edges = False

        for u in range(nvertices):
            r, c = vertex2coords_map[u]
            if field[r][c] == '#':
                continue
            if len(neighbours_out[u]) == 2:
                ncontracted += 1
                contract_edges = True

                #v - u - w
                v, vu = neighbours_out[u][0]
                w, uw = neighbours_out[u][1]

                neighbours_out[u] = []
                for j, u_ in enumerate(neighbours_out[v]):
                    if u_[0] == u:
                        neighbours_out[v][j] = (w, vu + uw)

                        for jj, uu_ in enumerate(neighbours_in[w]):
                            if uu_[0] == u:
                                neighbours_in[w][jj] = (v, vu + uw)
                                break
                        break

                for j, u_ in enumerate(neighbours_out[w]):
                    if u_[0] == u:
                        neighbours_out[w][j] = (v, vu + uw)

                        for jj, uu_ in enumerate(neighbours_in[v]):
                            if uu_[0] == u:
                                neighbours_in[v][jj] = (w, vu + uw)
                                break
                        break



                # print(v, u, w, neighbours_out[v], neighbours_in[w])
                # print(v, u, w, neighbours_out[v], neighbours_in[w])
                # print(v, u, w)
    print(ncontracted)

    # for u, nu in enumerate(neighbours_out):
    #     if len(nu) > 0:
    #         print(u, vertex2coords_map[u], nu)


    dfs(coord2vertex_map[starting_tile], coord2vertex_map[ending_tile], neighbours_out)
    # answer = dfs(field, starting_tile, ending_tile)
   

    # print(answer)

    answer = 0
    for pl in paths_lengths:
        answer = max(answer, pl)
    print(answer)
    
# part1()
part2()

