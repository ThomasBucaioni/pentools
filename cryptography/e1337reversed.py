class e1337rannumgen:
    def __init__(self, seed):
        self.state = 0
        for i in range(16):
            print(f"{i=}, {seed=:>08b}")
            self.cur = seed & 3
            seed >>= 2
            print(f"{self.cur=:08b}, {seed=:08b}")
            print(f"state << 0 = {(self.state << 0):08b}")
            print(f"state << 1 = {(self.state << 1):08b}")
            print(f"state << 2 = {(self.state << 2):08b}")
            print(f"state << 3 = {(self.state << 3):08b}")
            print(f"state << 4 = {(self.state << 4):08b}")
            print(f"state  & 3 = {(self.state & 3):08b}")
            print(f"{self.state=:08b}")
            self.state = (self.state << 4) | ((self.state & 3) ^ self.cur)
            print(f"{self.state=:08b}")
            print(f"self.cur={(self.cur << 2):08b}")
            self.state |= self.cur << 2
            print(f"{self.state=:08b}")
            print(f"{self.state=}")
            print(f"--- end of step {i} ---")
            print(f"------------------------")
            input("pause")

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

SEED = 33082914 # 33082914 50693495 66568751 
prng = e1337rannumgen(SEED)
v1 = prng.next(26)
v2 = prng.next(26)
print(SEED, v1, v2)
