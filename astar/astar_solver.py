from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from storage_types import Location, Path


class AStarSolver:
    def __init__(self, grid):
        self.org_grid = grid
        self._cached_paths: list[Path] = []

    def solve_for_locations(self, start_loc: Location, target_loc: Location) -> Path:
        if cached_path:= self._check_for_cached_solution(start_loc, target_loc):
            return cached_path
        else:
            grid = Grid(matrix=self.org_grid)
            start = grid.node(start_loc.x, start_loc.y)
            end = grid.node(target_loc.x, target_loc.y)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, _ = finder.find_path(start, end, grid)
            cur_path = Path([start_loc] + [Location(p[0], p[1]) for p in path[1:-1]] + [target_loc])
            self._cached_paths.append(cur_path)
            return cur_path
        
    def _check_for_cached_solution(self, loc1: Location, loc2: Location) -> Path:
        for path in self._cached_paths:
            if path.is_between_points(loc1, loc2):
                return path
            
    def get_shortest_length_between_locations(self, loc1: Location, loc2: Location) -> int:
        return self.solve_for_locations(loc1, loc2).length()