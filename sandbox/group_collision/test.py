import bmw

groups = bmw.TestCarProblemParser.parse_groups(filename='../../data/2-polished/groups.txt')

group40 = groups[40]
group41 = groups[41]

print('40:')
print(group40)
print(len(group40))
print('41:')
print(group41)
print(len(group41))

unique = list(sorted(set().union(group40, group41)))

print('Union:')
print(unique)
print(len(unique))

print('Intersection:')
print([_ for _ in unique if _ in group40 and _ in group41])
print(len([_ for _ in unique if _ in group40 and _ in group41]))
print('In 40 but not 41:')
print([_ for _ in unique if _ in group40 and _ not in group41])
print(len([_ for _ in unique if _ in group40 and _ not in group41]))
print('In 41 but not 40:')
print([_ for _ in unique if _ not in group40 and _ in group41])
print(len([_ for _ in unique if _ not in group40 and _ in group41]))

   
