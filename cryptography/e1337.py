# https://vovohelo.medium.com/cracking-rolling-code-locks-the-lazy-way-d9ab36ea9e8a

from z3 import *

class RNG:
    def __init__(self, seed):
        self.state = 0
        for _ in range(16):
            self.cur = seed & 3
            seed >>= 2
            self.state = (self.state << 4) | ((self.state & 3) ^ self.cur)
            self.state |= self.cur << 2

    def next(self, bits):
        ret = 0
        for _ in range(bits):
            ret <<= 1
            ret |= self.state & 1
            self.state = (self.state << 1) ^ (self.state >> 61)
            self.state &= 0xFFFFFFFFFFFFFFFF
            self.state ^= 0xFFFFFFFFFFFFFFFF
            for j in range(0, 64, 4):
                self.cur = (self.state >> j) & 0xF
                self.cur = (self.cur >> 3) | ((self.cur >> 2) & 2) | (
                    (self.cur << 3) & 8) | ((self.cur << 2) & 4)
                self.state ^= self.cur << j
        return ret

    def next2(self, bits):
        self.next(bits)
        return self.next(bits)


seed = BitVec("seed", 128)


#SEED = 33082914 # 33082914 50693495 66568751 
#prng = RNG(SEED)
#v1 = prng.next(26)
#v2 = prng.next(26)
#print(SEED, v1, v2)

prng = RNG(SEED)
v1 = input('V1 value: ')
v2 = input('V2 value: ')
print(f"Looking for the seed with {v1} and {v2}")

s = Solver()
s.add(seed >= 0)
s.add(seed <= 0xFFFFFFFF)
s.add(RNG(seed).next(26) == v1)
s.add(RNG(seed).next2(26) == v2)
s.check()
m = s.model()

print("Seed is: ", m[seed])

prng = RNG(int(str(m[seed])))
prng.next(26)
prng.next(26)
v3 = prng.next(26)
print("V3 is:", v3)

