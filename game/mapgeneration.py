def mapgenerator(level):
    import random
    i=0
    j=[]
    z=level*10
    x=random.randrange(1,50+z)
    while i in range(0, 50+z):
        i+=1
        k=0

        m=[]
        while k in range(0, 50+z):
            k+=1

            if k==x or k==(x-1) or k==(x+1):
                m.append(' ')
            else:
                m.append('#')
        if x<7:
            d=x
            r=x+(random.randrange(0, 2+level))
            x=r
        elif x>43:
            d=x
            r=x+(random.randrange(-2-level, 0))
            x=r
        else:
            d=x
            r=x+(random.randrange(-2-level, 2+level))
            x=r
        print(m)
        j.append(m)
    level_array=j
    print(level_array)
mapgenerator(0)
