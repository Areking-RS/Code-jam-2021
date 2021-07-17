import random
from typing import List, Tuple

MapType = List[List[str]]


def mapgenerator(map_width: int, map_height: int, room_frequency: int, room_size: int, path_width: int) -> \
        Tuple[MapType, int]:
    """
    Generate a map

    :param map_width: Width of the map
    :param map_height: Height of the map
    :param room_frequency: Frequency of rooms generated in the map
    :param room_size: Size of rooms in the map
    :param path_width: Average width of path
    :return: A tuple containing the map and a x-coordinate spawn location for the player
    """
    t = 0
    i = 0
    j = []
    z = map_width
    level = room_size
    x = random.randrange(3, 47 + z)
    original_spawn = x
    while i in range(0, map_height):
        i += 1
        k = 0

        m = []
        vb = random.randrange(1, room_frequency)

        while k in range(0, 50 + z):
            k += 1

            if k in range(x - (path_width // 2), x + (path_width // 2)):
                m.append(' ')
            else:
                m.append('#')
        if x < 7:
            r = x + (random.randrange(0, (path_width // 2) - 1))
            x = r
        elif x > 43:
            r = x + (random.randrange(-((path_width // 2) - 1), 0))
            x = r
        else:
            r = x + (random.randrange(-((path_width // 2) - 1), (path_width // 2) - 1))
            x = r
        vb = random.randrange(1, 10)
        if x < level + 2 and vb == 3:
            t = 0
            v = []
            while t < (level + 3):
                t += 1
                m[x + t] = ' '
                v.append(x + t)
        elif x > z + 48 - level and vb == 3:
            t = 0
            v = []
            while t < (level + 3):
                t += 1
                m[x - t] = ' '
                v.append(x - t)
        elif z + 48 - level > x > level + 2 and vb == 3:
            t = 0
            v = []
            e = random.randint(0, 1)
            if e == 1:
                while t < (level + 3):
                    t += 1
                    m[x - t] = ' '
                    v.append(x - t)
            else:
                while t < (level + 3):
                    t += 1
                    m[x + t] = ' '
                    v.append(x + t)
        elif t > 0:
            for q in v:
                m[q] = ' '
            t -= 1

        j.append(m)
    return j, original_spawn
