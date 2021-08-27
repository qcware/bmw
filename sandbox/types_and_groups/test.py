import bmw

types = bmw.TestCarProblemParser.parse_types(filename='../../data/3-refined/types.txt')
groups = bmw.TestCarProblemParser.parse_groups(filename='../../data/3-refined/groups.txt')

for tindex, type2 in enumerate(types):

    active_group_indices = [gindex for gindex, group in enumerate(groups) if len(set(type2).intersection(set(group)))]
    print(active_group_indices)

    active_group_indices = [gindex for gindex, group in enumerate(groups) if len(set(type2).intersection(set(group))) == len(set(group))]
    print(active_group_indices)
