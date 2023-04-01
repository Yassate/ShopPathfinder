from ui import AreaGrid
from storage_types import Location
from astar import AStarSolver
import numpy as np


def test_simple_case():
    a = ["1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1"]
    mygrid = AreaGrid(filepath=a, wh_pix=(500, 500))
    astar = AStarSolver(mygrid.get_org_grid())
    start_loc = Location(0,0)
    target_loc = Location(4,4)
    val = astar.get_shortest_length_between_locations(start_loc, target_loc)
    print(val)
    assert val==9