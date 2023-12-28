import numpy as np

if __name__ == "__main__":

    # part 1
    with open('input.txt', 'r') as f:
        answer = 0
        lines = f.readlines()

        for line in lines:
            tmp = line.split('|')
            # print(tmp)
            winning_numbers_ = (tmp[0].split(':')[1]).split()
            real_numbers_ = tmp[1].strip().split()

            winning_numbers = np.sort(np.array([int(i) for i in winning_numbers_], dtype = int))
            real_numbers = np.sort(np.array([int(i) for i in real_numbers_], dtype = int))
            common_numbers = np.intersect1d(winning_numbers, real_numbers)
            # print(winning_numbers, real_numbers, np.intersect1d(winning_numbers, real_numbers), len(common_numbers))

            if len(common_numbers) > 0:
                answer += 2**(len(common_numbers) - 1)
            # pass

        print(answer)

    
                            
    with open('input.txt', 'r') as f:
        answer = 0
        lines = f.readlines()

        scratchcards_count = np.ones(len(lines), dtype = int)
        scratchcards_winn = np.zeros(len(lines), dtype = int)

        for line in lines:
            tmp = line.split('|')
            # print(tmp)
            winning_numbers_ = (tmp[0].split(':')[1]).split()
            real_numbers_ = tmp[1].strip().split()
            card_id = int(tmp[0].split(':')[0].split()[1])


            winning_numbers = np.sort(np.array([int(i) for i in winning_numbers_], dtype = int))
            real_numbers = np.sort(np.array([int(i) for i in real_numbers_], dtype = int))
            common_numbers = np.intersect1d(winning_numbers, real_numbers)
            scratchcards_winn[card_id - 1] = len(common_numbers)
        
        for i in range(len(scratchcards_winn)):
            nwins = scratchcards_winn[i]
            ncards = scratchcards_count[i]
            for j in range(i + 1, min(i + 1 + scratchcards_winn[i], len(scratchcards_winn))):
                scratchcards_count[j] += ncards

        # print(scratchcards_count)
        print(sum(scratchcards_count))

    
                            
