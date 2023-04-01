from ui import AreaGrid
from storage_types import Location
from tsp import TrivialTSP
from astar import AStarSolver

HEIGHT = 750
GRID_WIDTH = HEIGHT
BUTTONS_WIDTH = round(1/4*GRID_WIDTH)
WIDTH = GRID_WIDTH + BUTTONS_WIDTH

def test_simple_case():
    input = ["1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1"]

# doesnt work yet; get_shortest~ needs to be extracted from mygrid

    to_find = []
    correct_ordered_locations = [Location(0,0), Location(1,1), Location(2,3), Location(3,3)]
    wrong_ordered_locations =   [Location(0,0), Location(3,3), Location(2,3), Location(1,1)]
    to_find = wrong_ordered_locations.copy()
    mygrid = AreaGrid(filepath=input, wh_pix=(500, 500))

    astar = AStarSolver(mygrid.get_org_grid())

    tsp = TrivialTSP(astar.get_shortest_length_between_locations, WIDTH*HEIGHT)
    solved = tsp.solve(to_find)

    assert solved == correct_ordered_locations