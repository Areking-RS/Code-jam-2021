
def mapgenerator(map_width, map_height, room_frequency, room_size, path_width):
    import random
    t = 0
    i = 0
    j = []
    z = map_width
    level = room_size
    x = random.randrange(3, 47 + z)
    original_spawn=x
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
            d = x
            r = x + (random.randrange(0, (path_width // 2) - 1))
            x = r
        elif x > 43:
            d = x
            r = x + (random.randrange(-((path_width // 2) - 1), 0))
            x = r
        else:
            d = x
            r = x + (random.randrange(-((path_width // 2) - 1), (path_width // 2) - 1))
            x = r
        vb = random.randrange(1, room_frequency)
        if x < level + 2 and vb == random.randrange(1, room_frequency):
            t = 0
            v = []
            while t < (level):
                t += 1
                m[x + t] = ' '
                v.append(x + t)
        elif x > z + 48 - level and vb == random.randrange(1, room_frequency):
            t = 0
            v = []
            while t < (level):
                t += 1
                m[x - t] = ' '
                v.append(x - t)
        elif z + 48 - level > x > level + 2 and vb == random.randrange(1, room_frequency):
            t = 0
            v = []
            e = random.randint(0, 1)
            if e == 1:
                while t < (level):
                    t += 1
                    m[x - t] = ' '
                    v.append(x - t)
            else:
                while t < (level):
                    t += 1
                    m[x + t] = ' '
                    v.append(x + t)
        elif t > 0:
            for q in v:
                m[q] = ' '
            t -= 1

        j.append(m)
    map_gen=[j, original_spawn]
    return map_gen
