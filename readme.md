# ShopPathfinder

Can be used for finding the *"shortest"* path between multiple points on the map. First idea was to shorten time spent in large shops.
It uses [pathfinding](https://pypi.org/project/pathfinding/) library and most trivial traveling salesman algorithm which every time takes the closest neighbour.

## Installation

Use the package manager *pip* and *venv* to install ShopPathfinder.

```bash
python -m venv .venv
./venv/Scripts/activate.bat
pip install -r requirements.txt
```

## Usage
*main.py* loads map from *obstacles.txt* and location list from *locations.csv*, just fill the files with your data.\

First selected location is start of the path\
<img src="https://user-images.githubusercontent.com/32523464/231804419-8f05715c-4991-4db9-b498-f2a0a2d64138.PNG" width="50%" height="50%"/>\
Next locations show up on the map accordingly\
<img src="https://user-images.githubusercontent.com/32523464/231806719-6526b80b-af05-4b76-a111-cf2a13b51fb9.PNG" width="50%" height="50%"/>\
*Find path* button draws *"shortest"* path between chosen locations, it's suboptimal solution -> see trivial TSP algorithm mentioned above\
<img src="https://user-images.githubusercontent.com/32523464/231804464-2b26df4e-2ba6-4abd-a1fd-dbc61a31c14d.PNG" width="50%" height="50%"/>\

## Possible next steps
* Better TSP algorithm
* Define start and end locations
* Mark direction of movement on generated paths
* Hints about locations shown on map (on hover?)

## License

[MIT](https://choosealicense.com/licenses/mit/)