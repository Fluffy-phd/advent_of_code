import numpy as np

def hash_aoc(inp):
    out = 0
    for c in inp:
        a = ord(c)
        out = ((out + a) * 17) % 256
    return out
    



def part1():

    init_sequences = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            tmp_ = line.strip().split(',')
            for t in tmp_:
                init_sequences.append(t.strip())

    # print(init_sequences)

    answer = 0
    for seq in init_sequences:
        answer += hash_aoc(seq)
    print(answer)


    

def part2():
    init_sequences = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            tmp_ = line.strip().split(',')
            for t in tmp_:
                init_sequences.append(t.strip())

    boxes = [[] for _ in range(256)]
    lens2box_map = {}
    answer = 0
    for seq in init_sequences:
        tmp_ = seq.split('-')
        if len(tmp_) > 1:
            # print('remove:', tmp_[0])

            label = tmp_[0]
            if label in lens2box_map:
                box = lens2box_map.pop(label)
                # print(label, box)
                idx = -1
                for i, j in enumerate(boxes[box]):
                    if j[0] == label:
                        idx = i
                        break
                if idx >= 0:
                    boxes[box].pop(idx)
                    print('removed', label)



        else:
            tmp_ = seq.split('=')
            label = tmp_[0]
            focal = int(tmp_[1])
            box = hash_aoc(label)

            if label in lens2box_map:
                box_current = lens2box_map.pop(label)
                if box_current != box:
                    print('ERROR')
                    return

                for i, j in enumerate(boxes[box]):
                    if j[0] == label:
                        boxes[box][i] = (label, focal)
                        break
                

            else:
                boxes[box].append((label, focal))
            lens2box_map[label] = box

            # print('add:', label, 'to box:', box, 'focal: ', focal)
    # print(boxes)

    answer = 0
    for i, box in enumerate(boxes):
        box_score = i + 1

        for j, lens in enumerate(box):
            slot_score = j + 1
            focal_score = lens[1]

            score_ = focal_score * slot_score * box_score
            answer += score_

            print('box: ', i, lens)
    
    print(answer)

part1()

part2()