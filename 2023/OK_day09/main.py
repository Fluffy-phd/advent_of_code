import numpy as np


def part1():
    def get_next(sequence, inter_val):
        tmp_ = [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]
        # print(sequence, tmp_, inter_val)

        cont = False
        for t in sequence:
            if t != 0:
                cont = True
        if cont:
            return get_next(tmp_, sequence[-1] + inter_val)
        return inter_val + sequence[-1]

    sequences = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            sequences.append([int(i) for i in line.split()])
    
    answer = 0
    for s in sequences:
        answer += get_next(s, 0)
        # print(s, get_next(s, 0))
    
    # print(sequences)
    print(answer)

def part2():
    def get_next(sequence, inter_val):
        tmp_ = [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]
        # print(sequence, tmp_, inter_val)

        cont = False
        for t in sequence:
            if t != 0:
                cont = True
        if cont:
            return get_next(tmp_, sequence[-1] + inter_val)
        return inter_val + sequence[-1]

    sequences = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            sequences.append([int(i) for i in line.split()])
    
    answer = 0
    for s in sequences:
        s.reverse()
        answer += get_next(s, 0)
        # print(s, get_next(s, 0))
    
    # print(sequences)
    print(answer)

part1()

part2()