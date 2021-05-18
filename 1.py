from pygame import Vector2
pos = [Vector2(40,40)]




def propagate_position(pos):
    result = []
    modificators = [ Vector2(-20, 20),
                     Vector2(0, -20),
                     Vector2(20, -20),
                     Vector2(-20, 0),
                     Vector2(20, 0),
                     Vector2(-20, -20),
                     Vector2(0, 20),
                     Vector2(20, 20)]

    for m in modificators:
        if m + pos not in result:
            result.append(m + pos)

    return result

for i in range(1):
    temp_pos = pos[:]
    for p in pos:
        result = propagate_position(p)
        for r in result:
            if r not in temp_pos:
                temp_pos.append(r)
                #print(temp_pos)
    pos = temp_pos
    print(len(pos))

#for p in pos: print(p)



