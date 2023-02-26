from ui import AreaGrid
from main import exec_salesman
from storage_types import Location

def test_simple_case():
    a = ["1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1", "1 1 1 1 1"]

    to_find = []
    correct_ordered_locations = [Location(0,0), Location(1,1), Location(2,3), Location(3,3)]
    wrong_ordered_locations =   [Location(0,0), Location(3,3), Location(2,3), Location(1,1)]
    to_find = wrong_ordered_locations.copy()

    mygrid = AreaGrid(filepath=a, wh_pix=(500, 500))
    exec_salesman(mygrid, to_find)

    assert to_find == correct_ordered_locations