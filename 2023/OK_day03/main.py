import numpy as np

if __name__ == "__main__":

    # tmp = '..999.'

    # print(len(tmp.split('.')))

    with open('input.txt', 'r') as f:
        lines = f.readlines()

        game_board = np.zeros((len(lines), len(lines[0].strip())), dtype = int)
        r = 0
        for line in lines:
            line = lines[r].strip()

            for i in range(len(line)):
                if line[i] == '.':
                    game_board[r, i] = -1
                elif line[i].isnumeric():
                    game_board[r, i] = int(line[i])
                else:
                    game_board[r, i] = 10
            r += 1

        # print(game_board[1])
        def extract_number(r, c):
            i = c
            # print('X', game_board[r, c])
            for _ in range(c + 1):
                if game_board[r, i] < 0 or game_board[r, i] > 9:
                    break
                i -= 1
            i += 1

            j = c
            for _ in range(game_board.shape[1] - c):
                if game_board[r, j] < 0 or game_board[r, j] > 9:
                    break
                j += 1

            n = 0
            for k in range(j - i, 0, -1):
                n += game_board[r, i + k - 1] * 10**(j - i - k)
            # print(game_board[r])
            # print(game_board[r, i:j], n)
            game_board[r, i:j] = -1
            return n

        answer = 0
        for r in range(game_board.shape[0]):
            for c in range(game_board.shape[1]):
                if game_board[r, c] == 10:
                    
                    for rr in [-1, 0, 1]:
                        r_ = rr + r
                        if r_ < 0 or r_ >= game_board.shape[0]:
                            continue

                        for cc in [-1, 0, 1]:
                            c_ = cc + c
                            if (c_ < 0 or c_ >= game_board.shape[1]) or(c_ == 0 and r_ == 0):
                                continue

                            if game_board[r_, c_] >= 0 and game_board[r_, c_] < 10:
                                n = extract_number(r_, c_)
                                answer += n
                    
                    game_board[r, c] = -1

        print(answer)

    
                            
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        game_board = np.zeros((len(lines), len(lines[0].strip())), dtype = int)
        r = 0
        for line in lines:
            line = lines[r].strip()

            for i in range(len(line)):
                if line[i] == '*':
                    game_board[r, i] = 10
                elif line[i].isnumeric():
                    game_board[r, i] = int(line[i])
                else:
                    game_board[r, i] = -1
            r += 1

        # print(game_board[1])
        def extract_number(r, c):
            i = c
            # print('X', game_board[r, c])
            for _ in range(c + 1):
                if game_board[r, i] < 0 or game_board[r, i] > 9:
                    break
                i -= 1
            i += 1

            j = c
            for _ in range(game_board.shape[1] - c):
                if game_board[r, j] < 0 or game_board[r, j] > 9:
                    break
                j += 1

            n = 0
            for k in range(j - i, 0, -1):
                n += game_board[r, i + k - 1] * 10**(j - i - k)
            # print(game_board[r])
            # print(game_board[r, i:j], n)
            game_board[r, i:j] = -1
            return n

        answer = 0
        for r in range(game_board.shape[0]):
            for c in range(game_board.shape[1]):
                if game_board[r, c] == 10:
                    
                    adjacent = []
                    for rr in [-1, 0, 1]:
                        r_ = rr + r
                        if r_ < 0 or r_ >= game_board.shape[0]:
                            continue

                        for cc in [-1, 0, 1]:
                            c_ = cc + c
                            if (c_ < 0 or c_ >= game_board.shape[1]) or(c_ == 0 and r_ == 0):
                                continue

                            if game_board[r_, c_] >= 0 and game_board[r_, c_] < 10:
                                n = extract_number(r_, c_)
                                adjacent.append(n)
                    if len(adjacent) == 2:
                        answer += adjacent[0] * adjacent[1]
                    
                    game_board[r, c] = -1

        print(answer)

    
                            
