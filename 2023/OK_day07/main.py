import numpy as np


def alter_code(code, code_map):

    out = 0
    a = 1
    for i in range(len(code)):
        c = code_map[code[len(code) - i - 1]]
        out += a * c
        a *= 13

    return out

def part1():
    code_map = {}
    code_map['2'] = 0
    code_map['3'] = 1
    code_map['4'] = 2
    code_map['5'] = 3
    code_map['6'] = 4
    code_map['7'] = 5
    code_map['8'] = 6
    code_map['9'] = 7
    code_map['T'] = 8
    code_map['J'] = 9
    code_map['Q'] = 10
    code_map['K'] = 11
    code_map['A'] = 12    
    hands = []
    # hands_s = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            tmp = line.split()
            code = tmp[0]
            bid = int(tmp[1])

            hand_strength = 0
            hand_tmp = {}
            for c in code:
                if c in hand_tmp: 
                    hand_tmp[c] += 1
                else:
                    hand_tmp[c] = 1
            hand_tmp_ = []
            for k in hand_tmp:
                hand_tmp_.append(hand_tmp[k])
            hand_tmp_ = np.sort(hand_tmp_)

            if len(hand_tmp_) == 1:
                hand_strength = 7     # five of a kind
            elif len(hand_tmp_) == 2:
                if hand_tmp_[-1] == 4:
                    hand_strength = 6 # four of a kind
                elif hand_tmp_[-1] == 3:
                    hand_strength = 5 # full house
            elif len(hand_tmp_) == 3:
                if hand_tmp_[-1] == 3:
                    hand_strength = 4 # three of a kind
                elif hand_tmp_[-1] == 2:
                    hand_strength = 3 # two pairs
            elif len(hand_tmp_) == 4:
                if hand_tmp_[-1] == 2:
                    hand_strength = 2 # one pair
            elif len(hand_tmp_) == 5:
                hand_strength = 1     # High card

            code_numeric = alter_code(code, code_map)
            hands.append((code_numeric, hand_strength, bid))
            # hands_s.append(hand_strength)

    # order = np.argsort(hands_s)
    hands_t = [[], [], [], [], [], [], [], []]
    for h in hands:
        hands_t[h[1]].append((h[0], h[2]))

    reward = 0
    mult = 1
    for i in range(1, 8):
        hands_i = hands_t[i]
        if len(hands_i) == 1:
            reward += hands_i[0][1] * mult
            mult += 1
        elif len(hands_i) > 1:
            tmp_ = []
            for t in hands_i:
                tmp_.append(t[0])
            o_ = np.argsort(tmp_)

            for o in o_:
                reward += hands_i[o][1] * mult
                mult += 1

    print(reward)

def part2():
    def eval_hand(nonjokers, njokers):
        n = len(nonjokers)
        if njokers == 5:
            return 7 # five of a kind
        
        if njokers == 4:
            return 7 # five of a kind
        
        if njokers == 3 and n == 2:
            return 6 # four of a kind

        if njokers == 3 and n == 1:
            return 7 # five of a kind
            
        if njokers == 2 and n == 3:
            return 4 # three of a kind
            
        if njokers == 2 and n == 2:
            return 6 # four of a kind
            
        if njokers == 2 and n == 1:
            return 7 # five of a kind
        
        if njokers == 1 and n == 4:
            return 2 # one pair
        
        if njokers == 1 and n == 3:
            return 4 # three of a kind
        
        if njokers == 1 and n == 2:
            if nonjokers[-1] == 3:
                return 6 # four of a kind
            if nonjokers[-1] == 2:
                return 5 # full house
        
        if njokers == 1 and n == 1:
           return 7 # five of a kind
        
        if n == 1:
            return 7     # five of a kind
        if n == 2:
            if nonjokers[-1] == 4:
                return 6 # four of a kind
            elif nonjokers[-1] == 3:
                return 5 # full house
        if n == 3:
            if nonjokers[-1] == 3:
                return 4 # three of a kind
            elif nonjokers[-1] == 2:
                return 3 # two pairs
        if n == 4:
            return 2 # one pair
        
        return 1     # High card        
        
            

    code_map = {}
    code_map['J'] = 0
    code_map['2'] = 1
    code_map['3'] = 2
    code_map['4'] = 3
    code_map['5'] = 4
    code_map['6'] = 5
    code_map['7'] = 6
    code_map['8'] = 7
    code_map['9'] = 8
    code_map['T'] = 9
    code_map['Q'] = 10
    code_map['K'] = 11
    code_map['A'] = 12    
    hands = []
    # hands_s = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            tmp = line.split()
            code = tmp[0]
            bid = int(tmp[1])

            hand_strength = 0
            hand_tmp = {}
            for c in code:
                if c in hand_tmp: 
                    hand_tmp[c] += 1
                else:
                    hand_tmp[c] = 1

            njokers = 0
            if 'J' in hand_tmp:
                njokers = hand_tmp['J']
            
            hand_tmp_ = []
            for k in hand_tmp:
                if k != 'J':
                    hand_tmp_.append(hand_tmp[k])
            hand_tmp_ = np.sort(hand_tmp_)

            hand_strength = eval_hand(hand_tmp_, njokers)
            code_numeric = alter_code(code, code_map)
            if njokers == 2:
                print(code, hand_strength, code_numeric)
            hands.append((code_numeric, hand_strength, bid))
            # hands_s.append(hand_strength)

    # order = np.argsort(hands_s)
    hands_t = [[], [], [], [], [], [], [], []]
    for h in hands:
        hands_t[h[1]].append((h[0], h[2]))

    reward = 0
    mult = 1
    for i in range(1, 8):
        hands_i = hands_t[i]
        if len(hands_i) == 1:
            reward += hands_i[0][1] * mult
            mult += 1
        elif len(hands_i) > 1:
            tmp_ = []
            for t in hands_i:
                tmp_.append(t[0])
            o_ = np.argsort(tmp_)

            for o in o_:
                reward += hands_i[o][1] * mult
                mult += 1

    print(reward)

part1()

part2()