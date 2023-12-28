import numpy as np

def part1():
    instructions = []
    nodes = {}


    with open('input.txt', 'r') as f:
        tmp = f.readlines()
        instructions_ = tmp[0].strip()
        instructions = np.zeros(len(instructions_), dtype = int)
        for j, i in enumerate(instructions_):
            if i == 'R':
                instructions[j] = 1

        for i in range(2, len(tmp)):
            line = tmp[i].strip()
            line_ = line.split('=')
            
            LR = line_[1].split(', ')
            L = LR[0].strip()[1:]
            R = LR[1].strip()[:-1]
            SRC = line_[0].strip()

            nodes[SRC] = (L, R)

    current_node = 'AAA'
    nsteps = 0
    ninstructions = len(instructions)
    while current_node != 'ZZZ':
        instruction = instructions[nsteps % ninstructions]
        nsteps += 1
        current_node = nodes[current_node][instruction]
    print(nsteps)


def part2():
    instructions = []
    nodes = {}


    with open('input.txt', 'r') as f:
        tmp = f.readlines()
        instructions_ = tmp[0].strip()
        instructions = np.zeros(len(instructions_), dtype = int)
        for j, i in enumerate(instructions_):
            if i == 'R':
                instructions[j] = 1

        for i in range(2, len(tmp)):
            line = tmp[i].strip()
            line_ = line.split('=')
            
            LR = line_[1].split(', ')
            L = LR[0].strip()[1:]
            R = LR[1].strip()[:-1]
            SRC = line_[0].strip()

            nodes[SRC] = (L, R)

    # distance from terminating nodes to a terminating node
    terminating_nodes = [f for f in nodes if f[-1] == 'Z']

    # distance from starting nodes to a terminating node
    starting_nodes = [f for f in nodes if f[-1] == 'A']

    ninstructions = len(instructions)
    print('number of instructions', ninstructions)
    new_nodes = {}
    for sn in starting_nodes:
        nsteps = 0
        current_node = sn
        while current_node[-1] != 'Z':
            instruction = instructions[nsteps % ninstructions]
            nsteps += 1
            current_node = nodes[current_node][instruction]
        new_nodes[sn] = (current_node, nsteps)
    
    cycling_nodes = {}
    for tn in terminating_nodes:

        nsteps = 0
        current_node = tn
        instruction = instructions[0]
        nsteps += 1
        current_node = nodes[current_node][instruction]

        while current_node[-1] != 'Z':
            instruction = instructions[(nsteps) % ninstructions]
            nsteps += 1
            current_node = nodes[current_node][instruction]
        cycling_nodes[tn] = (current_node, nsteps)
    
    for k in new_nodes:
        print(k, new_nodes[k])
    for k in cycling_nodes:
        print(k, cycling_nodes[k])


    for k in new_nodes:
        a = new_nodes[k][1]
        b = cycling_nodes[new_nodes[k][0]][1]
        # print(a, b)
        print('%d + k*%d' % (a, b))
    


    # current_nodes = [(new_nodes[k][0], new_nodes[k][1]) for k in new_nodes]
    # terminating_condition = False
    # print(current_nodes)
    # while terminating_condition == False:
    #     terminating_condition = True

    #     c_ref = current_nodes[0][1]
    #     for c in current_nodes:
    #         if c[1] != c_ref:
    #             terminating_condition = False
    #             break
        
    #     idx_to_be_altered = 0
    #     nstep_ref = current_nodes[idx_to_be_altered][1]
    #     for i, c in enumerate(current_nodes):
    #         if c[1] < nstep_ref:
    #             nstep_ref = c[1]
    #             idx_to_be_altered = i
    #             code_ref = c[0]

    #     new_code, new_steps = cycling_nodes[code_ref]

    #     current_nodes[idx_to_be_altered] = (new_code, nstep_ref + new_steps)

    #     print(current_nodes)

    
# part1()
# part2()

def f(x: int, y: int):
    out = []

    for b in range(1000000000):
        r = (b*x + x - y) % y
        if r == 0:
            out.append((b*x + x - y) // y)
            if len(out) == 2:
                break
    s = out[-1] - out[0]
    t = out[-1] + s

    print(out[0], s)

    for i in range(100000000):
        out.append(t)
        t += s


    return out

ab = f(18157, 19241)
ac = f(19783, 19241)
ad = f(16531, 19241)
ae = f(21409, 19241)
af = f(14363, 19241)

print(len(ab), len(ac), len(ad), len(ae), len(af))

a = np.intersect1d(ab, ac)
print(len(a))
a = np.intersect1d(a, ad)
print(len(a))
a = np.intersect1d(a, ae)
print(len(a))
a = np.intersect1d(a, af)
print(len(a), print(a))

a = a[0]

print(19241 * a + 19241)