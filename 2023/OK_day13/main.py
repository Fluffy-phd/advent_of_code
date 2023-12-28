import numpy as np

def convert_string(inp):
    out = 0
    k = 1
    for c in inp:
        if c == '#':
            out += k
        k *= 2
    return out


def convert_note(note):
    row_vals = []
    col_vals = []

    for rowidx in range(len(note)):
        row_vals.append(convert_string(note[rowidx]))
    
    for colidx in range(len(note[0])):
        inp = ''
        for r in range(len(note)):
            inp += note[r][colidx]
        col_vals.append(convert_string(inp))

    return (row_vals, col_vals)

def nreflections_exp(vals, invalid_indices = []):

    candidate_j = []
    for i in range(1, len(vals)):
        if vals[i] == vals[i - 1] and i not in invalid_indices:
            candidate_j.append(i)
    # print(vals)
    # print(candidate_j)
    out = 0
    for j in candidate_j:
        out_tmp = 0
        for k in range(j):
            idxa = j - (k + 1)
            idxb = j + k

            if idxb >= len(vals):
                out_tmp += 1
                continue
            
            # print(idxa, idxb, vals[idxa], vals[idxb])
            if vals[idxa] == vals[idxb]:
                out_tmp += 1
            else:
                out_tmp = 0
                break
        if out_tmp > out:
            out = out_tmp

    return out


def nreflections(vals):

    candidate_j = []
    for i in range(1, len(vals)):
        if vals[i] == vals[i - 1]:
            candidate_j.append(i)

    # print(candidate_j)
    out = 0
    for j in candidate_j:
        out_tmp = 0
        for k in range(j):
            idxa = j - (k + 1)
            idxb = j + k

            if idxb >= len(vals):
                out_tmp += 1
                continue
            
            # print(idxa, idxb, vals[idxa], vals[idxb])
            if vals[idxa] == vals[idxb]:
                out_tmp += 1
            else:
                out_tmp = 0
                break
        if out_tmp > out:
            out = out_tmp

    return out


def part1():

    notes = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        current_note = []
        for line in lines:
            if len(line.strip()) == 0:
                # print(current_note)
                nrows = len(current_note)
                ncols = len(current_note[0])
                cn = np.zeros((nrows, ncols), dtype = int)
                for r in range(nrows):
                    for c in range(ncols):
                        if current_note[r][c] == '#':
                            cn[r, c] = 1
                notes.append(cn)
                current_note = []
                # print('NEW')

            else:
                current_note.append(line.strip())
                # print(current_note[-1])
        if len(current_note) > 0:
            nrows = len(current_note)
            ncols = len(current_note[0])
            cn = np.zeros((nrows, ncols), dtype = int)
            for r in range(nrows):
                for c in range(ncols):
                    if current_note[r][c] == '#':
                        cn[r, c] = 1
            notes.append(cn)

    def get_value(vals):
        k = 1
        v = 0
        for val in vals:
            v += k * val
            k *= 2
        return v


    answer = 0
    for note in notes:
        # print(note)
        row_values = [get_value(note[r, :]) for r in range(note.shape[0])]
        col_values = [get_value(note[:, c]) for c in range(note.shape[1])]

        a = nreflections(row_values)
        b = nreflections(col_values)

        answer += b + 100*a
    print(answer)

def part2():

    notes = []
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        current_note = []
        for line in lines:
            if len(line.strip()) == 0:
                nrows = len(current_note)
                ncols = len(current_note[0])
                cn = np.zeros((nrows, ncols), dtype = int)
                for r in range(nrows):
                    for c in range(ncols):
                        if current_note[r][c] == '#':
                            cn[r, c] = 1
                notes.append(cn)
                current_note = []
                # print('NEW')

            else:
                current_note.append(line.strip())
                # print(current_note[-1])
        if len(current_note) > 0:
            nrows = len(current_note)
            ncols = len(current_note[0])
            cn = np.zeros((nrows, ncols), dtype = int)
            for r in range(nrows):
                for c in range(ncols):
                    if current_note[r][c] == '#':
                        cn[r, c] = 1
            notes.append(cn)
    def get_value(vals):
        k = 1
        v = 0
        for val in vals:
            v += k * val
            k *= 2

        val_reconstructed = np.zeros(len(vals), dtype = int)
        v_ = v
        for i in range(len(vals)):
            val_reconstructed[i] = v_ % 2
            v_ = (v_ - val_reconstructed[i]) // 2
            if val_reconstructed[i] != vals[i]:
                print('ERRR')

        # if val_reconstructed != vals:
            
        return v
    
    # for i, note in enumerate(notes):
    #     row_values = [get_value(note[r, :]) for r in range(note.shape[0])]
    #     col_values = [get_value(note[:, c]) for c in range(note.shape[1])]

    #     row_differences = [abs(row_values[j] - row_values[j - 1]) for j in range(1, note.shape[0])]
    #     col_differences = [abs(col_values[j] - col_values[j - 1]) for j in range(1, note.shape[1])]

    #     print('row_diff', row_differences)
    #     print('col_diff', col_differences)
    #     aref = nreflections(row_values)
    #     bref = nreflections(col_values)
    #     print(aref, bref)

    #     print('rows', row_values)
    #     aref = nreflections_exp(row_values, invalid_indices = [aref])
    #     bref = nreflections_exp(col_values, invalid_indices = [bref])
    #     print(aref, bref)
    #     score_ref_row = 100 * aref
    #     score_ref_col = bref


    answer = 0
    for iiii, note in enumerate(notes):
        # print()
        answer_tmp = 0

        row_values = [get_value(note[r, :]) for r in range(note.shape[0])]
        col_values = [get_value(note[:, c]) for c in range(note.shape[1])]
        aref = nreflections(row_values)
        bref = nreflections(col_values)
        score_ref_row = 100 * aref
        score_ref_col = bref
        score_ref = score_ref_col + score_ref_row
        if score_ref_col > 0 and score_ref_row > 0:
            print('WOW', score_ref_col, score_ref_row)
        if score_ref_col == 0 and score_ref_row == 0:
            print('WOW2', score_ref_col, score_ref_row)

        # print(col_values)
        # print(row_values)

        altered_values = np.zeros((note.shape[0], note.shape[1]), dtype = int)
        for r in range(note.shape[0]):
            col_shift = 2 ** r
            for c in range(note.shape[1]):
                row_shift = 2 ** c

                note[r, c] = (note[r, c] + 1) % 2
                if note[r, c] == 1:
                    row_values[r] += row_shift
                    col_values[c] += col_shift
                else:
                    row_values[r] -= row_shift
                    col_values[c] -= col_shift

                altered_values[r, c] = 1

                # if r == 1 and c == 4:
                #     print(note)
                #     print(row_values[r], row_shift, col_shift)
                #     nreflections_exp(row_values)

                a = nreflections_exp(row_values, invalid_indices = [aref])
                b = nreflections_exp(col_values, invalid_indices = [bref])
                score_row = 100 * a
                score_col = b
                # print((r, c))
                # if score_col + score_row > 0:
                #     print('-----')
                #     print((r, c), score_ref, score_col + score_row)
                #     print(col_values)
                #     print(row_values)
                    

                if score_row == score_ref_row:
                    score_row = 0
                if score_col == score_ref_col:
                    score_col = 0

                # print((r, c), score_ref, score_col + score_row)

                if score_row == score_ref_row and score_col == score_ref_col:
                    score = 0
                    # print('poof')
                else:
                    score = score_col + score_row
                    # print('oof')

                note[r, c] = (note[r, c] + 1) % 2
                if note[r, c] == 1:
                    row_values[r] += row_shift
                    col_values[c] += col_shift
                else:
                    row_values[r] -= row_shift
                    col_values[c] -= col_shift

                if score > 0:
                    answer_tmp = score
                    # for i in range(note.shape[0]):
                    #     for j in range(note.shape[1]):
                    #         if note[i, j] > 0:
                    #             print('#', end = '')
                    #         else:
                    #             print(' ', end = '')
                    #     print()
                    # print(answer_tmp)
                    break


            if answer_tmp > 0:
                break

        
        if answer_tmp == 0:
            # answer_tmp = score_ref_row + score_ref_col
            print('ERROR', iiii)
        answer += answer_tmp
        # print(altered_values)
            

    print(answer)
    



part1()

part2() # given asnwers: 21398, 26024, 28235

