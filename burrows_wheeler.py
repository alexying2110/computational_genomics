import math
import subprocess

class Node:
    def __init__(self, data, next_node = None):
        self.data = data
        self.next_node = next_node

    def get_next(self):
        return self.next_node

    def set_next(self, next_node):
        self.next_node = next_node

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

class CircularLinkedList:
    def __init__(self, nodes):
        self.root = nodes[0]
        self.size = len(nodes)

        for i in len(nodes):
            if i + 1 > len(nodes):
                nodes[i].set_next(nodes[0])
            else:
                nodes[i].set_next(nodes[i + 1])

    def get_size(self):
        return self.size

def bwTransform(genome):
    suffixes = []
    for i in range(len(genome)):
        suffixes.append(genome[i:] + genome[0:i])

    suffixes.sort()
    return "".join(suffixes[i][-1] for i in range(len(suffixes)))

def getCounts(genome):
    counts = [0, 0, 0, 0]
    for base in genome:
        if base == 'a':
            counts[0] += 1

        if base == 'c':
            counts[1] += 1

        if base == 'g':
            counts[2] += 1

        if base == 't':
            counts[3] += 1

    return counts

if __name__ == "__main__":

    ref_genome = "agtcagctttcgtggggcataagctaacgttgcgcctgagaaagtgtcaccata"
    test_genome = "cataagc"

    transformed = bwTransform(ref_genome)
    full_counts = getCounts(ref_genome)

    ref_len = len(transformed)

    sparse_array = []

    log_len = 2 ** math.ceil(math.log(math.log(ref_len, 2), 2))

    for i in range(math.floor(ref_len / log_len)):
        sub_counts = getCounts(transformed[i * log_len : (i + 1) * log_len])
        if i > 0:
            sub_counts = [sum(x) for x in zip(sub_counts, sparse_array[i - 1])]
        sparse_array.append(sub_counts)

    #implement 
