import numpy as np

# Returns the total cost of a gap of length gap_len
def init_cost(gap_len):
    return gap_len + 2 + gap_len % 3

# Returns marginal cost between gap_len and gap_len - 1
def add_cost(gap_len):
    return 4 if gap_len == 1 else -1 if gap_len % 3 == 0 else 2

# Returns the marginal cost of a match/mismatch
def match_cost(match):
  return -1 if match else 1

# Returns a 3-dimensional tensor with rows corresponding to the query, 
# columns corresponding to the reference, and a data vector
def make_cost_array(query, ref):
    query_len = len(query)
    ref_len = len(ref)

    # Each point of matrix is match cost, delete cost, 
    # insert cost, delete gap length, insert gap length

    cost_array = np.zeros((query_len + 1, ref_len + 1, 5))

    cost_array[:, 0] =\
      [[np.inf, init_cost(i), np.inf, i, 0] for i in range(query_len + 1)]
    cost_array[0, :] =\
      [[np.inf, np.inf, init_cost(i), 0, i] for i in range(ref_len + 1)]
    cost_array[0, 0] = [0, np.inf, np.inf, 0, 0]

    for r in range(query_len):
        for c in range(ref_len):
            match_from = cost_array[r, c, 0:3]
            cost_array[r + 1, c + 1, 0] =\
              match_cost(query[r] == ref[c]) + min(match_from)

            ins_from = cost_array[r, c + 1]
            ins_cost = min(\
              ins_from[0] + add_cost(1),\
              ins_from[2] + add_cost(1),\
              ins_from[1] + add_cost(ins_from[3] + 1)\
            )
            cost_array[r + 1, c + 1, 1] = ins_cost
            cost_array[r + 1, c + 1, 3] =\
              ins_from[3] + 1 if ins_cost == ins_from[1] + add_cost(ins_from[3] + 1)\
              else 1

            del_from = cost_array[r + 1, c]
            del_cost = min(\
              del_from[0] + add_cost(1),\
              del_from[1] + add_cost(1),\
              del_from[2] + add_cost(del_from[4] + 1)\
            )
            cost_array[r + 1, c + 1, 2] = del_cost
            cost_array[r + 1, c + 1, 4] =\
              del_from[4] + 1 if del_cost == del_from[2] + add_cost(del_from[4] + 1)\
              else 1

    return cost_array

# Returns a string representing the actions that arrive at the lowest score alignment
def traceback(cost_array, last_action, r, c):
    if r == 0 or c == 0:
        return ""
    else:
        # If the previous action was an insert, 
        # check if the insert score was the result of an extension
        if last_action == 'i' and cost_array[r, c, 3] > 1:
            return traceback(cost_array, 'i', r - 1, c) + 'i'

        # If the previous action was an delete, 
        # check if the delete score was the result of an extension
        if last_action == 'd' and cost_array[r, c, 4] > 1:
            return traceback(cost_array, 'd', r, c - 1) + 'd'
        
        # Default to matching in cases where multiple actions result in the same score
        next_step =\
          np.where(cost_array[r, c, 0:3] == np.amin(cost_array[r, c, 0:3]) )[0][0]

        if next_step == 0:
            return traceback(cost_array, 'm', r - 1, c - 1) + 'm'
        elif next_step == 1:
            return traceback(cost_array, 'i', r - 1, c) + 'i'
        else:
            return traceback(cost_array, 'd', r, c - 1) + 'd'

# Simply displays the alignment, including a line break at 80 for display purposes
# Note: This function doesn't really handle edge cases where the start or end
# of a query is not aligned with the reference and vice versa. These cases could 
# be implemented, but it's irrelevant for the use case, since the alignments
# from BLAST will not include these trailing regions
def get_alignment(query, ref, alignment_string):
    match_lines = ""
    for (idx, char) in enumerate(alignment_string):
        if char == "m" and query[idx] == ref[idx]:
            match_lines += "|"
        else:
            match_lines += " "

        if char == "d":
            query = query [:idx] + "-" + query[idx:]
        if char == "i":
            ref = ref[:idx] + "-" + ref[idx:]

    print(query[:80])
    print(match_lines[:80])
    print(ref[:80])
    print(query[80:])
    print(match_lines[80:])
    print(ref[80:])


query =     "AGATCTAATGGCTGCTTATGTAGACAATTCTAGTCTTACTATTAAGAAACCTAATGAATTATCTAGAGTATT\
AGGTTTGAAAACCCTTGCTACTCATGGTTTAGCTGCTGTTAATAGTGTCCCTTGG"
reference = "AGATCTAATGGCTGCTTATGTAGAAAATACAAGCATTACCATTAAGAAACCTAATGAGCTCTCGTTGGCCTT\
AGGTTTAAAAACACTTGCCACTCATGGTGCTGCTGCAATCAATAGTGTCCCTTGG"

cost_array = make_cost_array(query, reference)
alignment_string = traceback(cost_array, 'm', len(query), len(reference))

init_cost = lambda gap_len: gap_len + gap_len % 3
add_cost = lambda gap_len: -3 if gap_len % 3 == 0 else 2
match_cost = lambda match: -2 if match else 1

test = make_cost_array(query, reference)
'''
for r in range(test.shape[0]):
    for i in range(5):
        for c in range(test.shape[1]):
            if c == test.shape[1] - 1:
                print(test[r, c, i])
            else:
                print(test[r, c, i], end  ='\t')

    print('\n')
'''
alignment_string = traceback(test, 'm', len(query), len(reference))
print(alignment_string)
get_alignment(query, reference, alignment_string)
