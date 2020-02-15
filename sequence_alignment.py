from enum import Enum
import numpy as np

class Last(Enum):
    MATCH = 0
    DEL = 1
    INS = 2

def init_cost(gap_len):
    return gap_len + 2 + gap_len % 3

def add_cost(gap_len):
    return 4 if gap_len == 1 else -1 if gap_len % 3 == 0 else 2

def make_cost_array(seq1, seq2):

    len1 = len(seq1) + 1
    len2 = len(seq2) + 1

    # Each point of matrix is match cost, delete cost, insert cost, delete gap, insert gap
    cost_array = np.zeros((len1, len2, 5))

    cost_array[:, 0] = [[np.inf, init_cost(i), np.inf, i, 0] for i in range(len1)]
    cost_array[0, :] = [[np.inf, np.inf, init_cost(i), 0, i] for i in range(len2)]
    cost_array[0, 0] = [0, np.inf, np.inf, 0, 0]

    for r in range(len(seq1)):
        for c in range(len(seq2)):
            match_from = cost_array[r, c, 0:3]
            cost_array[r + 1, c + 1, 0] = (-1 if seq1[r] == seq2[c] else 1) + min(match_from)

            del_from = cost_array[r, c + 1]
            del_cost = min(del_from[0] + add_cost(1), del_from[2] + add_cost(1), del_from[1] + add_cost(del_from[3] + 1))
            cost_array[r + 1, c + 1, 1] = del_cost
            cost_array[r + 1, c + 1, 3] = del_from[3] + 1 if del_cost == del_from[1] + add_cost(del_from[3] + 1) else 1

            ins_from = cost_array[r + 1, c]
            ins_cost = min(ins_from[0] + add_cost(1), ins_from[1] + add_cost(1), ins_from[2] + add_cost(ins_from[4]) + 1)
            cost_array[r + 1, c + 1, 2] = ins_cost
            cost_array[r + 1, c + 1, 4] = ins_from[4] + 1 if del_cost == del_from[2] + add_cost(del_from[4] + 1) else 1

    return cost_array[:, :, 0:3]

def traceback(cost_array, r, c):
    if r == 0 or c == 0:
        return ""
    else:
        next_step = np.where(cost_array[r, c] == min(cost_array[r, c]))[0]
        if next_step == 0:
            return traceback(cost_array, r - 1, c - 1) + 'm'
        elif next_step == 1:
            return traceback(cost_array, r - 1, c) + 'd'
        else:
            return traceback(cost_array, r, c - 1) + 'i'

if __name__ == "__main__":
    test = make_cost_array("aggat", "tgcgat")
    for r in range(test.shape[0]):
        for i in range(3):
            for c in range(test.shape[1]):
                if c == test.shape[1] - 1:
                    print(test[r, c, i])
                else:
                    print(test[r, c, i], end  ='\t')

        print('\n')

    print(traceback(test, 5, 6))
