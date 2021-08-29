import bmw

problem = bmw.TestCarProblem.parse_problem(filepath='../../data/3-refined')

types, test_set = bmw.TestCarProblemTranslater.translate_problem(problem=problem)

for tindex, typ in enumerate(types):

    states0 = bmw.LowSeedGenerator.generate_rule_following_predicate(typ)
    
    print(tindex, len(states0))

for tindex, typ in enumerate(types):

    states1 = bmw.LowSeedGenerator.generate_rule_following_implication(typ)
    
    print(tindex, len(states1))

state = states1[0]

print(test_set.check_state(state=state))
print(test_set.check_constellation(constellation=states1))

