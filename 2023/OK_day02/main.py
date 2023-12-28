if __name__ == "__main__":

    rules = {}
    rules['r'] = 12
    rules['g'] = 13
    rules['b'] = 14

    # part one
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        answer = 0
        for line in lines:
            tmp = line.strip().split(':')
            G = int(tmp[0].split()[1])
            
            L = tmp[1].split(';')
            game_possible = True
            for l in L: #l - jeden tah z jedne hry
                l_ = l.split(',')

                for c in l_: # c - pocet kosticek a jejich barva z jednoho tahu
                    c_ = c.split()

                    cc = int(c_[0])
                    co = c_[1][0]

                    if rules[co] < cc:
                        game_possible = False
                        break

            if game_possible:
                answer += G
                    # print(cc, co)

        print(answer)

    # part two
    with open('input.txt', 'r') as f:
        lines = f.readlines()

        answer = 0
        for line in lines:
            tmp = line.strip().split(':')
            L = tmp[1].split(';')

            cmin = {}
            cmin['r'] = 0
            cmin['g'] = 0
            cmin['b'] = 0
            for l in L: #l - jeden tah z jedne hry
                l_ = l.split(',')

                for c in l_: # c - pocet kosticek a jejich barva z jednoho tahu
                    c_ = c.split()

                    cc = int(c_[0])
                    co = c_[1][0]

                    cmin[co] = max(cmin[co], cc)
            answer += cmin['r'] * cmin['g'] * cmin['b']


        print(answer)
