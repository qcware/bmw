import bmw
problem = bmw.Problem.parse(filepath='../../data/3-refined')

type_specification = problem.type_specifications[3]

state = [False]*type_specification.nfeature
mask = [False]*type_specification.nfeature

print('Pass 1:')

state[14] = True
print(type_specification.check_groups(state))
mask[14] = True
rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
for rule in rules:
    print(rule)

print('Pass 2:')

# state[315] = True
# state[431] = True
# state[299] = True
# state[302] = True
# state[193] = True
# state[124] = True
# state[182] = True
state[140] = True
# state[430] = True
# tate[366] = True
print(type_specification.check_groups(state))

rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
for rule in rules:
    print(rule)

print('Pass 3:')

state[414] = True
print(type_specification.check_groups(state))

rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
for rule in rules:
    print(rule)

print(problem.test_set.npass_state(state))

print([index for index, _ in enumerate(state) if _])

generator = bmw.RandomStateGenerator.build_random_seed()

state1 = generator.leapfrog_distance_2_mask(
    state=state,
    type_specification=type_specification,
    test_set=problem.test_set,
    niteration=30000,
    mask=mask)
    
print(problem.test_set.npass_state(state1))
