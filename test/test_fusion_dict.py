d1 = {"aaa":111}
d2 = {"bbb":222}
d = d1 | d2
print(d)

g = {}
li = [ d1, d2, d1, d2 ]
for l in li:
    g |= l
print(g)
