import bmw

problem = bmw.Problem.parse(filepath='../../data/3-refined')

type_specification = problem.type_specifications[5]

state = bmw.LowSeedGenerator.generate_rule_following_predicate(type_specification=type_specification)[0]

generator = bmw.RandomStateGenerator.build_random_seed()

print(problem.test_set.check_state(state=state))

for k in range(10):

    state = generator.leapfrog_distance_2(
        state=state,
        type_specification=type_specification,
        test_set=problem.test_set,
        niteration=10000)
    
    print(problem.test_set.check_state(state=state))
