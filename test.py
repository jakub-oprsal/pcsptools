import structure

def neq(n):
    yield from ( (i,j) for i in range(n) for j in range(n) if i != j )

clique3 = structure.new(range(3), (neq(3),))
print(clique3)

clique3 = structure.cache(structure.new(range(3),(neq(3),)))
print(clique3)

square = structure.power(clique3,2)
print(square)
for edge in square.relations[0]:
    print(edge)

