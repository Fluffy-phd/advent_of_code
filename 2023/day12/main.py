import numpy as np
from time import time
from math import comb

def parse_line(line):
    tmp = line.split(' ')
    groups_ = tmp[0].split('.')
    targets = [int(v) for v in tmp[1].split(',')]
    groups = [g for g in groups_ if len(g) > 0]

    if len(targets) != len(groups):
        return 0
    
    for i in range(len(targets)):
        if targets[i] != len(groups[i]):
            return 0

    # print(line)
    return 1

def parse_line_general(line):
    out = 0

    questionmark_indices = []
    for i, c in enumerate(line):
        if c == '?':
            questionmark_indices.append(i)

    ncombinations = 2**len(questionmark_indices)


    for i in range(ncombinations):
        line_tmp = ''
        k = 1
        for j, c in enumerate(line):
            if c == '?':
                if (k & i) == k:
                    line_tmp += '#'
                else:
                    line_tmp += '.'
                k *= 2
            else:
                line_tmp += c
        
        out += parse_line(line_tmp)

    return out

def recursive_patter_search(pattern, targets, dots, dot_idx, ndots):
    # print(len(pattern), np.sum(targets), np.sum(dots), ndots)
    # print(dots)

    if dot_idx >= len(dots) and ndots > 0:
        return 0

    if ndots == 0:
        pattern_idx = 0
        for segment_idx in range(len(targets)):
            #dots
            for i in range(dots[segment_idx]):
                if pattern[pattern_idx + i] == '#':
                    return 0
            pattern_idx += dots[segment_idx]
            #non-dots
            for i in range(targets[segment_idx]):
                if pattern[pattern_idx + i] == '.':
                    return 0
            pattern_idx += targets[segment_idx]
        #terminating dots
        for i in range(dots[-1]):
            if pattern[pattern_idx + i] == '#':
                return 0
        return 1
    
    # are already defined dots contradicting the pattern?
    pattern_idx = 0
    for segment_idx in range(dot_idx):
        #dots
        for i in range(dots[segment_idx]):
            if pattern[pattern_idx + i] == '#':
                return 0
        pattern_idx += dots[segment_idx]
        #non-dots
        for i in range(targets[segment_idx]):
            if pattern[pattern_idx + i] == '.':
                return 0
        pattern_idx += targets[segment_idx]

    out = 0
    for i in range(ndots + 1):
        dots[dot_idx] += i
        # print('  adding %d dots to position %d' % (i, dot_idx))
        out += recursive_patter_search(pattern, targets, dots, dot_idx + 1, ndots - i)
        dots[dot_idx] -= i
    return out


def generate_patterns(pattern, targets, spaces_to_fill):
    dots = [0 for _ in range(len(targets) + 1)]
    for i in range(1, len(targets)):
        dots[i] = 1
    # print(targets, dots, pattern)
    nvalid_patterns = recursive_patter_search(pattern, targets, dots, 0, spaces_to_fill)

    return nvalid_patterns



def analyze_pattern(pattern, targets):
    if len(targets) == 0:
        return 1
    
    pattern_len = len(pattern)
    pattern_fixed_len = np.sum(targets) + len(targets) - 1
    spaces_to_fill = pattern_len - pattern_fixed_len

    nquestionmarks = len([v for v in pattern if v == '?'])
    naive_complexity = 2**nquestionmarks

    
    ndelimiters = len(targets) - 1
    nspaces = ndelimiters + spaces_to_fill
    fill_complexity = comb(nspaces, ndelimiters)

    return generate_patterns(pattern, targets, spaces_to_fill)
    if fill_complexity >= naive_complexity:
        return parse_line_general(line)
    else:
        return generate_patterns(pattern, targets, spaces_to_fill)



def parse_line_exp(line):
    tmp = line.split(' ')
    pattern = tmp[0]
    targets = [int(v) for v in tmp[1].split(',')]

    return analyze_pattern(pattern, targets)

def get_all_splits(P, T):

    # print(P, T)
    F = []
    M = len(P) - T + 1
    nshifts = M
    # print(nshifts)

    for i in range(nshifts):
        subP = P[i:i + T]
        Pprev = P[:i]
        Pnext = P[i + T:]

        isvalid = True
        if '#' in Pprev:
            isvalid = False
        
        if len(Pnext) > 0:
            if Pnext[0] == '#':
                isvalid = False

        if isvalid:

            p1hash = '#' in subP
            p2hash = '#' in P[i + T + 1:]

            if len(P[i + T + 1:]) > 0:
                if p1hash and p2hash:
                    F.append([subP, P[i + T + 1:]])
                elif p1hash:
                    F.append([subP, P[i + T + 1:]])
                    F.append([subP])
                elif p2hash:
                    F.append([subP, P[i + T + 1:]])
                    F.append([P[i + T + 1:]])
                else:
                    F.append([subP, P[i + T + 1:]])
                    F.append([subP])
                    F.append([P[i + T + 1:]])
                    F.append([])
            else:
                if p1hash:
                    F.append([subP])
                else:
                    F.append([subP])
                    F.append([])
    return F
    # print('F', F)

    # out_ = []
    # for i in range(1, len(P) - 1):
    #     if P[i] == '?':
    #         p1 = P[:i]
    #         p2 = P[i + 1:]
    #         out_.append([p1, p2])

    # tmp_ref = get_n_elementary_combinations(P, T)
    # if tmp_ref == 0:
    #     return []
    
    # out = []
    # for Q in out_:
    #     P1 = Q[0]
    #     tmp_ = get_n_elementary_combinations(P1, T)
    #     if tmp_ == 0:
    #         continue
    #     else:
    #         out.append(Q)

    #     if tmp_ == tmp_ref:
    #         break
    #     tmp_ref = tmp_


        
    # return out


def get_n_elementary_combinations(P, n):
    # print(P, n)
    if len(P) < n:
        return 0

    if len(P) == n:
        return 1
    
    
    out = len(P) - n + 1

    nshifts = out

    for i in range(nshifts):
        isvalid = True
        for c in P[:i]:
            if c == '#':
                isvalid = False
                break
        if isvalid:
            for c in P[i + n:]:
                if c == '#':
                    isvalid = False
                    break
        if not isvalid:
            out -= 1

    return out


def recursive_subpattern_analysis(subpatterns, targets, ncombs, subpattern_to_split):
    
    if len(subpatterns) > len(targets) or subpattern_to_split >= len(subpatterns):
        return 0
    
    if len(subpatterns) == len(targets):
        for i in range(subpattern_to_split, len(targets)):
            ncombs[i] = get_n_elementary_combinations(subpatterns[i], targets[i])
        tmp = 1
        for c in ncombs:
            tmp *= c
        print('   ', tmp, ncombs, subpatterns)

        return tmp
    

    subpatter_splits = get_all_splits(subpatterns[subpattern_to_split], targets[subpattern_to_split])
    print(subpatterns, subpatterns[subpattern_to_split], subpatter_splits)
    if len(subpatter_splits) > 0:
        tmp_ = 0
        for sp_split in subpatter_splits:
            if len(sp_split) == 2:
                subpatterns_ = subpatterns.copy()
                subpatterns_.pop(subpattern_to_split)
                subpatterns_.insert(subpattern_to_split, sp_split[1])
                subpatterns_.insert(subpattern_to_split, sp_split[0])
                
                ncombs[subpattern_to_split] = get_n_elementary_combinations(subpatterns_[subpattern_to_split], targets[subpattern_to_split])
                # print(subpatterns_, ncombs[subpattern_to_split])
                # print(subpattern_to_split, subpatterns_[subpattern_to_split], targets[subpattern_to_split], ncombs[subpattern_to_split])
                if ncombs[subpattern_to_split] == 0:
                    # print(subpatterns[subpattern_to_split], targets[subpattern_to_split])
                    continue
                tmp_ += recursive_subpattern_analysis(subpatterns_, targets, ncombs, subpattern_to_split + 1)
            elif len(sp_split) == 1:
                subpatterns_ = subpatterns.copy()
                subpatterns_.pop(subpattern_to_split)
                subpatterns_.insert(subpattern_to_split, sp_split[0])
                
                ncombs[subpattern_to_split] = get_n_elementary_combinations(subpatterns_[subpattern_to_split], targets[subpattern_to_split])
                # print(subpatterns_, ncombs[subpattern_to_split])
                # print(subpattern_to_split, subpatterns_[subpattern_to_split], targets[subpattern_to_split], ncombs[subpattern_to_split])
                if ncombs[subpattern_to_split] == 0:
                    # print(subpatterns[subpattern_to_split], targets[subpattern_to_split])
                    continue
                tmp_ += recursive_subpattern_analysis(subpatterns_, targets, ncombs, subpattern_to_split + 1)
            else:
                subpatterns_ = subpatterns.copy()
                subpatterns_.pop(subpattern_to_split)
                tmp_ += recursive_subpattern_analysis(subpatterns_, targets, ncombs, subpattern_to_split)

        return tmp_
    
    ncombs[subpattern_to_split] = get_n_elementary_combinations(subpatterns[subpattern_to_split], targets[subpattern_to_split])
    return recursive_subpattern_analysis(subpatterns, targets, ncombs, subpattern_to_split + 1)

def first_check_ok(T, P):
    for i, t in enumerate(T):
        # sum of items in one bucket cannot exceed the limit of the bucket, items need to be separated by a dot
        if np.sum(t) + len(t) - 1 > len(P[i]):
            # print('    FAIL:', T, P, T[i], P[i], np.sum(t) + len(t) - 1, len(P[i]))
            return False
        # buckets with '#' cannot be empty

        if '#' in P[i] and len(t) == 0:
            # print('    FAIL:', t, P)
            return False
    return True

def get_bucket_assignments(nitems, nbuckets, P, T):

    indices = [i for i in range(nitems)]
    out = []

    # print('ANALYSING', nitems, nbuckets)

    bucket_distribution = [[] for _ in range(nbuckets)]
    bucket_contents = [[] for _ in range(nbuckets)]
    def recursive_bucket_definition(bucket_idx, first_item_index, nitems_to_assign):
        if bucket_idx >= nbuckets:
            return
        if bucket_idx == nbuckets - 1:
            bucket_distribution[bucket_idx] = indices[first_item_index:first_item_index + nitems_to_assign]
            # print(bucket_distribution[bucket_idx])
            bucket_contents[bucket_idx] = tuple([T[j] for j in bucket_distribution[bucket_idx]])
            # print(bucket_contents[bucket_idx])
            out.append(bucket_contents.copy())
            bucket_distribution[bucket_idx] = []
            bucket_contents[bucket_idx] = []
            return
        
        # for i in range(bucket_idx):
        #     # sum of items in one bucket cannot exceed the limit of the bucket, items need to be separated by a dot
        #     # buckets with '#' cannot be empty
        #     if (np.sum(bucket_contents[i]) + len(bucket_contents[i]) - 1 > len(P[i])) or ('#' in P[i] and len(bucket_contents[i]) == 0):
        #         return

        recursive_bucket_definition(bucket_idx + 1, first_item_index, nitems_to_assign)
        for n in range(1, nitems_to_assign + 1):
            bucket_distribution[bucket_idx] = indices[first_item_index:first_item_index + n]
            bucket_contents[bucket_idx] = tuple([T[j] for j in bucket_distribution[bucket_idx]])
            if not ((np.sum(bucket_contents[bucket_idx]) + len(bucket_contents[bucket_idx]) - 1 > len(P[bucket_idx])) or ('#' in P[bucket_idx] and len(bucket_contents[bucket_idx]) == 0)):
                recursive_bucket_definition(bucket_idx + 1, first_item_index + n, nitems_to_assign - n)
            bucket_distribution[bucket_idx] = []
            bucket_contents[bucket_idx] = []

    recursive_bucket_definition(0, 0, nitems)
    # print('  ', len(out))
    return out

global_result_memory = {}
def get_n_combinations(P, T):
    if len(T) == 0:
        if '#' in P:
            return 0
        return 1
    
    if P not in global_result_memory:
        global_result_memory[P] = {}

    if T not in global_result_memory[P]:
        # print('computing', P, T)
        result = analyze_pattern(P, T)
        global_result_memory[P][T] = result

    return global_result_memory[P][T]

def EXP(pattern, targets):
    out = 0
    # print(pattern, targets)

    subpatterns = []
    subpattern = ''
    for c in pattern:
        if c != '.':
            subpattern += c
        elif len(subpattern) > 0:
            subpatterns.append(subpattern)
            subpattern = ''
    if len(subpattern) > 0:
        subpatterns.append(subpattern)


    targets_possibilities = get_bucket_assignments(nitems = len(targets), nbuckets = len(subpatterns), P = subpatterns, T = targets)
    # print(subpatterns)

    explorable_targets = []
    for i, T in enumerate(targets_possibilities):
    # for i, v in enumerate(targets_possibilities):
        # T = [tuple([targets[j] for j in w]) for w in v]
        if first_check_ok(T, subpatterns):
            # print('  ', T)
            explorable_targets.append(T)

    # print('  ', len(targets_possibilities), len(explorable_targets))
    nbuckets = len(subpatterns)
    for T in explorable_targets:
        out_tmp = 1
        for i in range(nbuckets):
            # print(subpatterns[i], T[i])
            out_tmp *= get_n_combinations(subpatterns[i], T[i])
        out += out_tmp
    # return recursive_subpattern_analysis(subpatterns, targets, ncombs, subpattern_to_split = 0)

    return out

def parse_line_part2_exp(line):
    S1 = 0
    S2 = 0
    S3 = 0
    S4 = 0
    S5 = 0
    
    tmp = line.split(' ')
    pattern1 = tmp[0]
    targets1 = [int(v) for v in tmp[1].split(',')]


    S1 = EXP(pattern1, targets1)

    targets2 = targets1.copy()
    pattern2 = pattern1
    pattern2 += '#'
    for c in pattern1:
        pattern2 += c
    for v in targets1:
        targets2.append(v)
    S2 = EXP(pattern2, targets2)

    targets3 = targets2.copy()
    pattern3 = pattern2
    pattern3 += '#'
    for c in pattern1:
        pattern3 += c
    for v in targets1:
        targets3.append(v)
    S3 = EXP(pattern3, targets3)

    targets4 = targets3.copy()
    pattern4 = pattern3
    pattern4 += '#'
    for c in pattern1:
        pattern4 += c
    for v in targets1:
        targets4.append(v)
    S4 = EXP(pattern4, targets4)

    targets5 = targets4.copy()
    pattern5 = pattern4
    pattern5 += '#'
    for c in pattern1:
        pattern5 += c
    for v in targets1:
        targets5.append(v)
    S5 = EXP(pattern5, targets5)

    # # print(S1, S2, S3, S4, S5)

    #S.S.S.S.S
    S = (S1**5)

    #S#S.S.S.S
    #S.S#S.S.S
    #S.S.S#S.S
    #S.S.S.S#S
    S += 4*(S1**3)*S2

    #S#S#S.S.S
    #S.S#S#S.S
    #S.S.S#S#S
    S += 3*S3*(S1**2)

    #S#S.S#S.S
    #S#S.S.S#S
    #S.S#S.S#S
    S += 3*(S2**2)*(S1)

    #S#S#S#S.S
    #S.S#S#S#S
    S += 2*S1*S4

    #S#S#S.S#S
    #S#S.S#S#S
    S += 2*S2*S3

    #S#S#S#S#S
    S += S5

    # pattern_ver = pattern1 + '?' + pattern1 + '?' + pattern1 + '?' + pattern1 + '?' + pattern1
    # print(pattern_ver, targets5)
    # Sver = analyze_pattern(pattern_ver, targets5, line)

    print(S1, S2, S3, S4, S5)
    # print(Sver, S1**5)

    return S

def parse_line_part2(line):
    tmp = line.split(' ')
    pattern1 = tmp[0]
    targets1 = [int(v) for v in tmp[1].split(',')]

    S1 = analyze_pattern(pattern1, targets1)

    targets2 = targets1.copy()
    pattern2 = pattern1
    pattern2 += '#'
    for c in pattern1:
        pattern2 += c
    for v in targets1:
        targets2.append(v)
    S2 = analyze_pattern(pattern2, targets2)

    targets3 = targets2.copy()
    pattern3 = pattern2
    pattern3 += '#'
    for c in pattern1:
        pattern3 += c
    for v in targets1:
        targets3.append(v)
    S3 = analyze_pattern(pattern3, targets3)

    targets4 = targets3.copy()
    pattern4 = pattern3
    pattern4 += '#'
    for c in pattern1:
        pattern4 += c
    for v in targets1:
        targets4.append(v)
    S4 = analyze_pattern(pattern4, targets4)

    targets5 = targets4.copy()
    pattern5 = pattern4
    pattern5 += '#'
    for c in pattern1:
        pattern5 += c
    for v in targets1:
        targets5.append(v)
    S5 = analyze_pattern(pattern5, targets5)

    print(S1, S2, S3, S4, S5)

    #S.S.S.S.S
    S = (S1**5)

    #S#S.S.S.S
    #S.S#S.S.S
    #S.S.S#S.S
    #S.S.S.S#S
    S += 4*(S1**3)*S2

    #S#S#S.S.S
    #S.S#S#S.S
    #S.S.S#S#S
    S += 3*S3*(S1**2)

    #S#S.S#S.S
    #S#S.S.S#S
    #S.S#S.S#S
    S += 3*(S2**2)*(S1)

    #S#S#S#S.S
    #S.S#S#S#S
    S += 2*S1*S4

    #S#S#S.S#S
    #S#S.S#S#S
    S += 2*S2*S3

    #S#S#S#S#S
    S += S5

    # pattern_ver = pattern1 + '?' + pattern1 + '?' + pattern1 + '?' + pattern1 + '?' + pattern1
    # print(pattern_ver, targets5)
    # Sver = analyze_pattern(pattern_ver, targets5, line)

    # print(S1, S2, S3, S4, S5)
    # print(Sver, S1**5)

    return S



def part1():
    t0 = time()
    answer = 0
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            answer += parse_line_general(line.strip())
            print(i, line.strip())
    t1 = time()
    print(t1 - t0, answer)
    # time: 24.664729118347168 [s], result: 6827
        
def part1_new():
    t0 = time()
    answer = 0
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            answer += parse_line_exp(line.strip())
    t1 = time()
    print(t1 - t0, answer)
    # time: 0.06576204299926758 [s], result: 6827
        
def part2():

    def gen(A, B, targets, targets_len, target_idx, pattern_position, prev_pattern_end, history, pattern):
        n = len(pattern)
        if B[pattern_position - prev_pattern_end] == 0 or targets_len > n - pattern_position:
            return 0

        # B[l][p] = can there be a pause of length l starting at position p in the pattern?
        # A[l][p] = can an item of length l be placed at position p in the pattern?

        l = targets[target_idx]
        for p in range(pattern_position, n):
            if A[l][p] == 0:
                continue
            history_local = history.copy()
            history_local.append((l, pattern_position))
            


        # if target_idx == len(targets):
        #     # print('OK', targets_len, pattern_idx, n, history)
        #     # pout = np.zeros(n, dtype = int)
        #     # for i, c in enumerate(history):
        #     #     clen = c[0]
        #     #     cpos = c[1]
        #     #     pout[cpos:cpos + clen] = 1
        #     # pout_str = ''
        #     # for c in pout:
        #     #     if c == 1:
        #     #         pout_str += '#'
        #     #     else:
        #     #         pout_str += '.'
        #     # print(pout_str)
        #     return 1

        # if pattern_idx >= n or targets_len > (n - pattern_idx):
        #     # print('   ', target_idx, pattern_idx)
        #     # print(pattern_idx >= n, targets_len, targets_len > (n - pattern_idx))
        #     return 0


        # tn = targets[target_idx]
        # # print(pattern_idx, target_idx, targets_len)
        # # print(pattern_idx >= n or targets_len > (n - pattern_idx))
        # # print(target_idx == len(targets))
        # # print(A[pattern_idx, tn - 1] == 0)

        # # A[r, c] = can an item of length (c + 1) be placed at position r?
        # if A[pattern_idx, tn - 1] == 0:
        #     return gen(A, B, targets, targets_len, target_idx, pattern_idx + 1, history, pattern)
        # # B[r, c] = does an item of length (c + 1) HAVE to be placed at position r?
        # if pattern[pattern_idx] == '#':
        #     history_tmp = history.copy()
        #     history_tmp.append((tn, pattern_idx))
        #     return gen(A, B, targets, targets_len - (tn + 1), target_idx + 1, pattern_idx + tn + 1, history_tmp, pattern)
        # else:
        #     out = 0
        #     for cc in range(n - pattern_idx):
        #         # print('c:', cc)
        #         # if target_idx <= 1:
        #         #     print('F', target_idx, pattern_idx + c)
        #         # print('  ', B[pattern_idx, :cc + 1], cc,n - pattern_idx)
        #         if A[pattern_idx + cc, tn - 1] == 1 and B[pattern_idx - 1, cc] == 0:
        #             history_tmp = history.copy()
        #             history_tmp.append((tn, pattern_idx + cc))
        #             # print(target_idx, pattern_idx, c, B[pattern_idx])
        #             tmp = gen(A, B, targets, targets_len - (tn + 1), target_idx + 1, pattern_idx + tn + 1 + cc, history_tmp, pattern)
        #             out += tmp
        #             if tmp == 0:
        #                 break

        # return out


    t0 = time()
    answer = 0
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        # lidx = 8
        ninvalid = 0
        # for i, line in enumerate(lines[lidx:lidx + 1]):
        for i, line in enumerate(lines):
            tmp = line.split(' ')
            pattern = tmp[0]
            targets_ = [int(v) for v in tmp[1].split(',')]
            targets = []
            for r in range(1):
                for t in targets_:
                    targets.append(t)

            n = len(pattern)

            # A[l] = list of positions at which an item of length l can be placed
            A = {}
            for t in targets_:
                if t in A:
                    continue

                Aloc = np.zeros(n, dtype = int)
                for r in range(n - t):
                    if '.' not in pattern[r:r + t]:
                        Aloc[r] = 1
                    if r - 1 >= 0:
                        if pattern[r - 1] == '#':
                            Aloc[r] = 0
                    if r + t < n:
                        if pattern[r + t] == '#':
                            Aloc[r] = 0
                A[t] = set(tuple([i for i in range(n) if Aloc[i] == 1]))
            print(pattern)
            for l in A:
                print(l, A[l])

            # B[l] = list of positions at which an empty space of length l cannot be placed
            B = {}
            for t in range(n):
                if t in B:
                    continue
                Bloc = np.zeros(n, dtype = int)
                for r in range(n - t):
                    if '#' not in pattern[r:r + t]:
                        Bloc[r] = 1
                B[t] = set(tuple([i for i in range(n) if Bloc[i] == 1]))
            print(pattern)
            for l in B:
                print(l, B[l])

            # tmp = gen(A, B, targets, np.sum(targets) + len(targets) - 1, 0, 0, 0, history = [], pattern = pattern)
            tmp = 0
            tmp2 = parse_line_exp(line.strip())
            # print(ncalls)

            if tmp2 != tmp:
                print(i, tmp2, tmp, pattern, targets)
                break
            answer += tmp
    t1 = time()
    print(t1 - t0, answer, '# of invalid', ninvalid)
    # time: 0.06576204299926758 [s], result: 61950310334
        
        

# part1_new()
part2()

# ?????.???????## 3,1,6
# ###?#.??. 3,1
# ###??.#?. 3,1
# ###??.?#. 3,1
# ?###?.#?. 3,1
# ?###?.?#. 3,1
# ??###.#?. 3,1
# ??###.?#. 3,1

