import bmw
import numpy as np

def generate_random_guess(
    test_expression,
    type_specification,
    max_depth=6,
    ):
    
    # Start with empty state
    state = [False]*type_specification.nfeature
    mask = [False]*type_specification.nfeature

    # Make the test true (random 1-hot for 'any' statements)
    for expression in test_expression.expressions:

        if expression.all:
            for index, phase in zip(expression.indices, expression.phases):
                state[index] = False if phase else True
        else:
            pivot = np.random.randint(len(expression.indices))
            index = expression.indices[pivot]
            phase = expression.phases[pivot]
            state[index] = False if phase else True

        for index in expression.indices:
            mask[index] = True

    # We should have just satisfied the test
    if not test_expression.evaluate(state): raiseRuntimeError('Sanity check')

    # Forcing the test might break the groups
    if not type_specification.check_groups(state): return [], []

    # Now chase implications until a valid car is built
    for depth in range(max_depth):    

        # Find the failing rules
        rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]

        if not len(rules): break

        # Make the implication of the failing rules true
        for rule in rules:
            implication = rule.implication
            if implication.all:
                for index, phase in zip(implication.indices, implication.phases):
                    state[index] = False if phase else True
            else:
                pivot = np.random.randint(len(implication.indices))
                index = implication.indices[pivot]
                phase = implication.phases[pivot]
                state[index] = False if phase else True

    # Implication chasing could break either the state or the test
    if type_specification.check_valid(state) and test_expression.evaluate(state):
        return state, mask
    else:
        return [], []

def generate_random_guess_2(
    test_expression,
    type_specifications,
    nattempt=1000, 
    max_depth=6,
    ):

    for attempt in range(nattempt):
        type_index = np.random.randint(len(type_specifications)) 
        type_specification = type_specifications[type_index]
        state, mask = generate_random_guess(
            test_expression=test_expression,
            type_specification=type_specification,
            max_depth=max_depth,
            )
        if len(state):
            return type_index, state, mask

    return -1, [], []
    
problem = bmw.Problem.parse(filepath='../../data/3-refined')

type_indices = []
states = []
masks = []

for test_index, test_expression in enumerate(problem.test_set.expressions):
    
    type_index, state, mask = generate_random_guess_2(
        test_expression=test_expression,
        type_specifications=problem.type_specifications,
        nattempt=10000,
        )
    
    print('%-2d : %2d : %s' % (test_index, type_index, test_expression))

    if not len(state):
        raise RuntimeError('Invalid Run')
    
    type_indices.append(type_index)
    states.append(state)
    masks.append(mask)

type_indices = np.array(type_indices)
states = np.array(states)
masks = np.array(masks)
        
# Do not overwrite canonical guess
# np.savez(
#     'test.npz',
#     type_indices=type_indices,
#     states=states,
#     masks=masks,
#     )
