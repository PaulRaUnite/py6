from typing import List, Dict, Set


class City:
    def __init__(self, name: str):
        self.name = name
        self.nexts: List[City] = list()

    def __str__(self) -> str:
        return "<{} -> {}>".format(self.name, [city.name for city in self.nexts])

    def __repr__(self):
        return self.__str__()


def play(current: City, routes: List[List[City]], was: Set[City] = set(), prefix: List[City] = list()):
    was.add(current)
    prefix.append(current)
    before = len(routes)
    for city in current.nexts:
        if city not in was:
            play(city, routes, was, prefix)
    if before == len(routes):
        routes.append(prefix.copy())
    prefix.pop()
    if len(was) > 0:
        was.remove(current)


filename = "fine_cities.txt"  # input()
file = open(filename)

cities: Set[City] = set()
city_index: Dict[chr, List[City]] = dict()

for line in file:
    # prepare
    city = City(line.lstrip().rstrip().lower())
    cities.add(city)

    # fill the index
    first_letter = city.name[0]
    if first_letter not in city_index:
        city_index[first_letter] = [city]
    else:
        city_index[first_letter].append(city)

for city in cities:
    # complete graph
    last_letter = city.name[-1]
    if last_letter in city_index:
        city.nexts = city_index[last_letter]

routes = list()
for city in cities:
    play(city, routes)

# print(routes)

game_can_end = False
for route in routes:
    if len(route) == len(cities):
        if not game_can_end:
            print("Solutions that contain every city:")
        game_can_end = True
        print([city.name for city in route])

if not game_can_end:
    print("There are no solutions that have every city.")
    print("Print incomplete routes...")
    for route in routes:
        print([city.name for city in route])
