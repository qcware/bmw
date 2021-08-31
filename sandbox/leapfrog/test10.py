import bmw
import numpy as np

problem = bmw.Problem.parse(filepath='../../data/3-refined')

type_specification = problem.type_specifications[4]

state = [False]*type_specification.nfeature
mask = [False]*type_specification.nfeature

print('Pass 1:')

state[14] = True
print(type_specification.check_groups(state))
rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
for rule in rules:
    print(rule)

print('Pass 2:')

state[315] = True
state[431] = True
state[299] = True
state[302] = True
state[193] = True
state[182] = True
state[124] = True
state[233] = True # Predicate
state[366] = True # Huge
print(type_specification.check_groups(state))
rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
for rule in rules:
    print(rule)

print('Pass 3:')

state[218] = True
print(type_specification.check_groups(state))
rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
for rule in rules:
    print(rule)

print(problem.test_set.npass_state(state))

generator = bmw.RandomStateGenerator.build_random_seed()

mask = [False]*len(state)
mask[14] = True

for k in range(10):

    state = generator.leapfrog_distance_2_mask(
        state=state,
        type_specification=type_specification,
        test_set=problem.test_set,
        niteration=30000,
        mask=mask)
        
    print(problem.test_set.npass_state(state))

np.savez(
    'test10.npz',
    constellation=[state],
    constellation_types=[4],    
    )

