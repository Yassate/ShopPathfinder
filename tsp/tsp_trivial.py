from storage_types import Location
from typing import Callable

class TrivialTSP:
    def __init__(self, distCalc: Callable, init_max_dist: int):
        self.distCalc = distCalc
        self.init_max_dist = init_max_dist

    def solve(self, loc_input: list[Location]):
        solved = loc_input[:]
        for i in range(len(solved)-1):
            shortest = self.init_max_dist
            for j in range(i+1, len(solved)):
                dist = self.distCalc(solved[i], solved[j])
                if dist < shortest:
                    shortest = dist
                    nearest_p = solved[j]
            solved.remove(nearest_p)
            solved.insert(i+1, nearest_p)
        return solved