import bmw
import numpy as np

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

seed = state

for k in range(20):

    results = bmw.HammingStateGenerator.generate_distance_2(
        state=seed,
        type_specification=types[-1],
        test_set=test_set,
        nresult_target=10000,
        )
    print('Iter %d:' % k)
    print(len(results))
    print(test_set.check_state(state=results[0]))
    print(test_set.check_constellation(constellation=results))

    # seed = results[0]
    seed = results[np.random.choice(list(range(len(results))))]

