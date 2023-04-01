from ui import AreaGrid
from storage_types import Location
from tsp import TrivialTSP

HEIGHT = 750
GRID_WIDTH = HEIGHT
BUTTONS_WIDTH = round(1/4*GRID_WIDTH)
WIDTH = GRID_WIDTH + BUTTONS_WIDTH

def test_simple_case():
    a = ["1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1"]

# doesnt work yet; get_shortest~ needs to be extracted from mygrid

    to_find = []
    correct_ordered_locations = [Location(0,0), Location(1,1), Location(2,3), Location(3,3)]
    wrong_ordered_locations =   [Location(0,0), Location(3,3), Location(2,3), Location(1,1)]
    to_find = wrong_ordered_locations.copy()
    mygrid = AreaGrid(filepath=a, wh_pix=(500, 500))
    tsp = TrivialTSP(mygrid.get_shortest_length_between_locations, WIDTH*HEIGHT)
    solved = tsp.solve(to_find)

    #exec_salesman(mygrid, to_find)

    assert solved == correct_ordered_locations