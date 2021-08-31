import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

print('Seed:')

states0 = []
for tindex, type_specification in enumerate(problem.type_specifications):

    state = bmw.LowSeedGenerator.generate_rule_following_predicate(type_specification=type_specification)[0]
    print('%-2d : %3d' % (
        tindex,
        problem.test_set.npass_state(state=state),
        ))
    states0.append(state)

generator = bmw.RandomStateGenerator.build_random_seed()

constellation = []
test_set = problem.test_set

states = states0

for k in range(24):

    if k % 8 == 0: states = states0

    print('Phase %d:' % k)
    
    new_states = []
    for tindex, type_specification in enumerate(problem.type_specifications):
    
        state0 = states[tindex]
    
        state1 = generator.leapfrog_distance_2(
            state=state0,
            type_specification=type_specification,
            test_set=test_set,
            niteration=10000)
    
        new_states.append(state1)
        
        print('%-2d : %3d' % (
            tindex,
            test_set.npass_state(state=state1),
            ))
    
    states = new_states
    
    pivot = np.argmax([test_set.npass_state(state=_) for _ in states])
    
    constellation += [states[pivot]]

    print('Constellation pass: %d' % (problem.test_set.npass_constellation(constellation=constellation)))

    indices = problem.test_set.passes_constellation(constellation=constellation)
    
    indices2 = [_ for _ in range(problem.test_set.ntest) if _ not in indices]

    test_set = bmw.TestSet(
        counts=[problem.test_set.counts[_] for _ in indices2],
        expressions=[problem.test_set.expressions[_] for _ in indices2],
        )

indices = problem.test_set.passes_constellation(constellation=constellation)

indices2 = [_ for _ in range(problem.test_set.ntest) if _ not in indices]

for i2, index in enumerate(indices2):

    print('%1d : %s' % (
        problem.test_set.counts[index],
        problem.test_set.expressions[index]))





