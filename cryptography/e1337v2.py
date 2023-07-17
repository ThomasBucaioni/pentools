# https://vovohelo.medium.com/cracking-rolling-code-locks-the-lazy-way-d9ab36ea9e8a 

import numpy as np

class npRNG:
    def __init__(self, seeds):
        # self.state = 0
        self.states = np.array([0]*len(seeds), dtype=np.ulonglong)
        for _ in range(16):
            # self.cur = seed & 3
            self.cur = np.bitwise_and(seeds, 3)
            # seed >>= 2
            seeds = np.right_shift(seeds, 2)
            # self.state = (self.state << 4) | ((self.state & 3) ^ self.cur)
            self.states = np.bitwise_or(np.left_shift(self.states, 4), np.bitwise_xor(
                np.bitwise_and(self.states, 3), self.cur))
            # self.state |= self.cur << 2
            self.states = np.bitwise_or(
                self.states, np.left_shift(self.cur, 2))

    def get_states(self):
        return self.states

    def next(self, bits):
        ret = np.array([0]*len(self.states), dtype=np.ulonglong)
        for _ in range(bits):
            # ret <<= 1
            ret = np.left_shift(ret, 1)
            # ret |= self.state & 1
            ret = np.bitwise_or(ret, np.bitwise_and(
                self.states, 1))
            for _ in range(3):
                # self.state = (self.state << 1) ^ (self.state >> 61)
                self.states = np.bitwise_xor(np.left_shift(self.states, 1), np.right_shift(
                    self.states, 61))
                # self.state &= 0xFFFFFFFFFFFFFFFF
                self.states = np.bitwise_and(self.states, 0xFFFFFFFFFFFFFFFF)
                # self.state ^= 0xFFFFFFFFFFFFFFFF
                self.states = np.bitwise_xor(self.states, 0xFFFFFFFFFFFFFFFF)
                for j in range(0, 64, 4):
                    # self.cur = (self.state >> j) & 0xF
                    self.cur = np.bitwise_and(
                        np.right_shift(self.states, j), 0xF)
                    # self.cur = (self.cur >> 3) | ((self.cur >> 2) & 2) | ((self.cur << 3) & 8) | ((self.cur << 2) & 4) ==> a | b | c
                    a = np.bitwise_or(np.right_shift(self.cur, 3), np.bitwise_and(
                        np.right_shift(self.cur, 2), 2))
                    b = np.bitwise_and(np.left_shift(self.cur, 3), 8)
                    c = np.bitwise_and(np.left_shift(self.cur, 2), 4)
                    self.cur = np.bitwise_or(np.bitwise_or(a, b), c)
                    # self.state ^= self.cur << j
                    self.states = np.bitwise_xor(self.states, np.left_shift(
                        self.cur, j))
        return ret

    def next2(self, bits):
        self.next(bits)
        return self.next(bits)


SEED_MAX = 0xFFFFFFFF
STEP = 10000000

V1 =  1170723147175696553
V2 =  13824566107725628344
print(V1, V2)
candidates = []
for s in range(0, SEED_MAX, STEP):
    print('{}% complete'.format((s/SEED_MAX)*100))
    print("Initializing npRNG:", s, s+STEP, "...")
    seeds = np.array(range(s, s+STEP), dtype=np.ulonglong)
    npprng = npRNG(seeds)
    print("Calculating candidates ...")
    values = npprng.next(8)
    print("Looking for V1 matches ...")
    matches = np.where(values == (V1 >> 56))[0]
    if len(matches) > 0:
        print("Matches found:", len(matches))
        candidates.append(seeds[matches])
    else:
        print("Trying next batch ...\n")

for i, c in enumerate(candidates):
    print('{}% complete'.format((i/len(candidates))*100))
    print("Initializing npRNG ...")
    seeds = np.array(c, dtype=np.ulonglong)
    npprng = npRNG(seeds)
    print("Calculating candidates ...")
    values = npprng.next(64)
    print("Looking for V1 matches ...")
    matches = np.where(values == V1)[0]
    if len(matches) > 0:
        print("Matches found:", len(matches))
        print(seeds[matches])
        values2 = npRNG(np.array(seeds[matches], dtype=np.ulonglong)).next2(64)
        matches2 = np.where(values2 == V2)[0]
        if len(matches2) > 0:
            print("Seeds found:", values2, matches2, seeds[matches2])
            sys.exit(0)
    else:
        print("Trying next batch ...\n")

print("Sorry, no matches found =T")
