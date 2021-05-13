from pygame import Vector2

a = Vector2((1,1))
b = Vector2((2,2))
t= Vector2((4,4))

c = [a,b]
l=[]
for e in c:
    l.append(e.distance_to(t))

n_p = c[l.index(min(l))]
print(n_p)

