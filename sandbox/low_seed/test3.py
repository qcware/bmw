import bmw

problem = bmw.TestCarProblem.parse_problem(filepath='../../data/3-refined')

types, test_set = bmw.TestCarProblemTranslater.translate_problem(problem=problem)

state = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, True, True, False, False, False, True, False, False, False, False, True, False, True, True, False, False, False, False, True, False, True, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, True, True, False, False, True, False, False, False, True, False, False, False, True, False, False, False, False, False, True, True, True, False, False, True, False, True, True, True, False, True, False, False, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, False, True, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, True, True, False, True, False, False, False, False, False, False, False, True, False, False, True, True, False, False, True, False, False, False, True, False, False, True, False, True, False, False, True, True, False, True, False, False, True, False, True, False, True, False, False, False, False, False, False, False, False, True, True, False, True, False, False, False, False, False, True, False, False, False, False, False, False, True, False, True, False]

print(test_set.check_state(state=state))

seed = state

for k in range(10):

    results = bmw.HammingStateGenerator.generate_distance_2(
        state=seed,
        type_specification=types[5],
        test_set=test_set,
        nresult_target=10000,
        )
    print('Iter %d:' % k)
    print(len(results))
    print(test_set.check_state(state=results[0]))
    # print(test_set.check_constellation(constellation=results))

    seed = results[0]

for l in range(4):

    indices = [index for index, test in enumerate(test_set.expressions) if not test.evaluate(seed)]
    
    test_set = bmw.TestSet(
        weights=[test_set.weights[index] for index in indices],
        counts=[test_set.counts[index] for index in indices],
        expressions=[test_set.expressions[index] for index in indices],
        )
    
    seed = state
    
    for k in range(10):
    
        results = bmw.HammingStateGenerator.generate_distance_2(
            state=seed,
            type_specification=types[5],
            test_set=test_set,
            nresult_target=10000,
            )
        print('Iter %d:' % k)
        print(len(results))
        print(test_set.check_state(state=results[0]))
        # print(test_set.check_constellation(constellation=results))

        seed = results[0]