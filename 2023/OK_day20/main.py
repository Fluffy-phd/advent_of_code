import numpy as np


def part1():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        nvertices = len(lines) + 1
        neighbors_out = [[] for _ in range(nvertices)]
        neighbors_in = [[] for _ in range(nvertices)]
        pulse_out = np.ones(nvertices, dtype = int)
        flip_flop_state = [0 for _ in range(nvertices)]
        vertex_type = ['' for _ in range(nvertices)]
        vertex_name = ['' for _ in range(nvertices)]
        name2int_map = {}
        active_idx = 0
        for line in lines:
            tmp_ = line.strip().split('->')
            src_name = tmp_[0].strip()
            destinations = tmp_[1].split(',')

            src_type = '*'
            if src_name != 'broadcaster':
                src_type = src_name[0]
                src_name = src_name[1:]
            
            if src_name not in name2int_map:
                name2int_map[src_name] = active_idx
                active_idx += 1

            vertex_type[name2int_map[src_name]] = src_type
            vertex_name[name2int_map[src_name]] = src_name

            for dst in destinations:
                if dst.strip() not in name2int_map:
                    name2int_map[dst.strip()] = active_idx
                    active_idx += 1
                neighbors_in[name2int_map[dst.strip()]].append(name2int_map[src_name])
                
            neighbors_out[name2int_map[src_name]] = [name2int_map[dst.strip()] for dst in destinations] 
            # if line[0] == '%':
                # flip module
        starting_vertex = name2int_map['broadcaster']

    print(starting_vertex, neighbors_out, neighbors_in, vertex_type, vertex_name)
    # modules
    # % flip flop, initially off, ignores high pulse, low pulse flips it between on and off, if it turns on, it sends a high pulse, if it turns off, it sends a low pulse
    # & concujnction, remember recent pulse type,

    n_pulses = [0, 0]
    def push_button():
        # print([(-1, 1)])
        # print([(starting_vertex, 1)])
        print('%s -> %s : %d' % ('button', vertex_name[starting_vertex], 1))
        active_vertices = []
        n_pulses[0] += 1
        for v in neighbors_out[starting_vertex]:
            active_vertices.append((v, 1))
            pulse_out[starting_vertex] = 1
            print('%s -> %s : %d' % (vertex_name[starting_vertex], vertex_name[v], 1))

        while len(active_vertices) > 0:
            active_vertices_new = []
            # print(active_vertices)
            

            for u, pulse in active_vertices:
                n_pulses[pulse - 1] += 1
                if u == starting_vertex:
                    pulse_out[u] = pulse
                    for v in neighbors_out[u]:
                        active_vertices_new.append((v, pulse))
                        print('%s -> %s : %d' % (vertex_name[u], vertex_name[v], pulse_out[u]))
                        

                elif vertex_type[u] == '%' and pulse == 1:
                    # low pulse
                    if flip_flop_state[u] == 0:
                        pulse_out[u] = 2
                        flip_flop_state[u] = 1
                        for v in neighbors_out[u]:
                            active_vertices_new.append((v, 2))
                            print('%s -> %s : %d' % (vertex_name[u], vertex_name[v], pulse_out[u]))
                    else:
                        pulse_out[u] = 1
                        flip_flop_state[u] = 0
                        for v in neighbors_out[u]:
                            active_vertices_new.append((v, 1))
                            print('%s -> %s : %d' % (vertex_name[u], vertex_name[v], pulse_out[u]))

                elif vertex_type[u] == '&':
                    pulse_out[u] = 1
                    for w in neighbors_in[u]:
                        if pulse_out[w] == 1:
                            pulse_out[u] = 2
                            break
                    
                    for v in neighbors_out[u]:
                        active_vertices_new.append((v, pulse_out[u]))
                        print('%s -> %s : %d' % (vertex_name[u], vertex_name[v], pulse_out[u]))

            active_vertices = active_vertices_new

        # print(flip_flop_state)

    for i in range(1000):
        push_button()
    print(n_pulses[0] * n_pulses[1])

def part2():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        nvertices = len(lines) + 1
        neighbors_out = [[] for _ in range(nvertices)]
        neighbors_in = [[] for _ in range(nvertices)]
        pulse_out = np.ones(nvertices, dtype = int)
        vertex2flipflopbit = {}
        vertex_type = ['' for _ in range(nvertices)]
        vertex_name = ['' for _ in range(nvertices)]
        name2int_map = {}
        active_idx = 0
        nbits = 0
        for line in lines:
            tmp_ = line.strip().split('->')
            src_name = tmp_[0].strip()
            destinations = tmp_[1].split(',')

            src_type = '*'
            if src_name != 'broadcaster':
                src_type = src_name[0]
                src_name = src_name[1:]

            
            if src_name not in name2int_map:
                name2int_map[src_name] = active_idx
                active_idx += 1

            if src_type == '%':
                vertex2flipflopbit[name2int_map[src_name]] = nbits
                nbits += 1

            vertex_type[name2int_map[src_name]] = src_type
            vertex_name[name2int_map[src_name]] = src_name

            for dst in destinations:
                if dst.strip() not in name2int_map:
                    name2int_map[dst.strip()] = active_idx
                    active_idx += 1
                neighbors_in[name2int_map[dst.strip()]].append(name2int_map[src_name])
                
            neighbors_out[name2int_map[src_name]] = [name2int_map[dst.strip()] for dst in destinations] 
            neighbors_out[name2int_map[src_name]].sort()
            # if line[0] == '%':
                # flip module
        starting_vertex = name2int_map['broadcaster']

    for u in range(nvertices):
        neighbors_in[u].sort()

    flip_flop_state = np.zeros(nbits, dtype = np.bool_)
    
    # print(starting_vertex, neighbors_out, neighbors_in, vertex_type, vertex_name)
    terminating_vertex = name2int_map['rx']
    vertex_type[terminating_vertex] = '-'
    # modules
    # % flip flop, initially off, ignores high pulse, low pulse flips it between on and off, if it turns on, it sends a high pulse, if it turns off, it sends a low pulse
    # & concujnction, remember recent pulse type,
    def eval_bit_state(arg):
        out = 0
        k = 1
        for i in arg:
            out += i * k
            k *= 2
        return out

    def push_button(sv, pulse, tgt):
        active_vertices = []
        out = []
        
        if vertex_type[sv] == '%' and pulse == 1:
            # low pulse
            if flip_flop_state[vertex2flipflopbit[sv]] == 0:
                pulse_out[sv] = 2
                flip_flop_state[vertex2flipflopbit[sv]] = 1
                for v in neighbors_out[sv]:
                    active_vertices.append((v, pulse_out[sv]))
            else:
                pulse_out[sv] = 1
                flip_flop_state[vertex2flipflopbit[sv]] = 0
                for v in neighbors_out[sv]:
                    active_vertices.append((v, pulse_out[sv]))

        elif vertex_type[sv] == '&':
            pulse_out[sv] = 1
            for w in neighbors_in[sv]:
                if pulse_out[w] == 1:
                    pulse_out[sv] = 2
                    break
            
            for v in neighbors_out[sv]:
                active_vertices.append((v, pulse_out[sv]))

        nsteps = 0
        while len(active_vertices) > 0:
            active_vertices_new = []
            nsteps += 1

            for u, pulse in active_vertices:
                if vertex_type[u] == '%' and pulse == 1:
                    # low pulse
                    if flip_flop_state[vertex2flipflopbit[u]] == 0:
                        pulse_out[u] = 2
                        flip_flop_state[vertex2flipflopbit[u]] = 1
                        for v in neighbors_out[u]:
                            active_vertices_new.append((v, pulse_out[u]))
                            # print('%s -> %s : %d' % (vertex_name[u], vertex_name[v], pulse_out[u]))
                    else:
                        pulse_out[u] = 1
                        flip_flop_state[vertex2flipflopbit[u]] = 0
                        for v in neighbors_out[u]:
                            active_vertices_new.append((v, pulse_out[u]))
                            # print('%s -> %s : %d' % (vertex_name[u], vertex_name[v], pulse_out[u]))

                elif vertex_type[u] == '&':
                    pulse_out[u] = 1
                    for w in neighbors_in[u]:
                        if pulse_out[w] == 1:
                            pulse_out[u] = 2
                            break
                    
                    if tgt == u:
                        # print(pulse_out[u], end = '')
                        out.append(pulse_out[u])
                    for v in neighbors_out[u]:
                        active_vertices_new.append((v, pulse_out[u]))
                        # print('%s -> %s : %d' % (vertex_name[u], vertex_name[v], pulse_out[u]))

            active_vertices = active_vertices_new
        return out
    
    vertex_colors = np.zeros((len(neighbors_out[starting_vertex]), nvertices), dtype = int)
    for color, sv in enumerate(neighbors_out[starting_vertex]):
        active_vertices = [sv]
        
        vertex_colors[color, sv] = 1
        
        while len(active_vertices) > 0:
            active_vertices_new = []
            for u in active_vertices:
                for v in neighbors_out[u]:
                    if vertex_colors[color, v] == 0:
                        active_vertices_new.append(v)
                        vertex_colors[color, v] = 1
            active_vertices = active_vertices_new

    for i in range(vertex_colors.shape[0]):
        for j in range(vertex_colors.shape[1]):
            print(vertex_colors[i, j], end = '')
        print()
    tmp_ = vertex_colors.sum(axis=0)

    partial_terminators = neighbors_in[[neighbors_in[terminating_vertex]][0][0]]
    print(partial_terminators)

    def periodic_behaviour(s, t):
        print(s, t)
        reached_flip_states = {}
        flip_state_history = []
        npushes = 0
        pulse_out.fill(1)
        flip_flop_state.fill(0)
        output_pulses = []
        # pulse_out[t] = -1

        initial_state = eval_bit_state(flip_flop_state)
        reached_flip_states[initial_state] = len(flip_state_history)

        while True:
            npushes += 1
            target_history = push_button(s, 1, t)
            output_pulses.append(target_history)
            tmp_state = eval_bit_state(flip_flop_state)

            if tmp_state in reached_flip_states:
                flip_state_history.append(reached_flip_states[tmp_state])
                break
            reached_flip_states[tmp_state] = len(flip_state_history)
            flip_state_history.append(reached_flip_states[tmp_state])
        
        print('# of pushes to find a cycle: ', npushes)

        return (flip_state_history, output_pulses, npushes)




    answer = 1
    for i, s in enumerate(neighbors_out[starting_vertex]):
        for t in partial_terminators:
            if vertex_colors[i, t] == 1:
                qh, qp, n_ = periodic_behaviour(s, t)
                # print(qh[:2], qh[-2:], qp[-1])
                answer *= n_
        # break
    print(answer)

        


    # for i in range(nvertices):
    #     if len(neighbors_in[i]) == 1 and len(neighbors_out[i]) == 1:
    #         print('%d%s' %  (i, vertex_type[i]), '%d%s' %  (neighbors_in[i][0], vertex_type[i]), '%d%s' %  (neighbors_out[i][0], vertex_type[i]))
    # print(starting_vertex, terminating_vertex)

    # print()
    # push_button()
    # print()
    # push_button()
    # def bool2int(boolarr):
    #     out = 0
    #     k = 1
    #     for b in boolarr:
    #         out += b * k
    #         k *= 2
    #     return out
    
    # state_transitions = {}
    # val_current = bool2int(flip_flop_state)
    # for i in range(100000000000):
    #     if val_current in state_transitions:
    #         print('REACHED A PAST POINT')
    #         break
    #     if i % 1000 == 0:
    #         print(i, len(state_transitions))
    #     push_button()
    #     val_new = bool2int(flip_flop_state)
    #     state_transitions[val_current] = val_new
    #     val_current = val_new
        
    #     if pulse_out[neighbors_in[terminating_vertex][0]] == 1:
    #         print(i + 1)
    #         break

# part1()

part2()

# 3761 * a = 3797 * b = 3919 * c = 4079 * d
# are prime numbers => 
# print(3761*3797*3919*4079)

