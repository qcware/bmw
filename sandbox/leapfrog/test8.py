import bmw
import numpy as np
import itertools

def force_solutions_following_predicate(
    type_specification,
    test_expression,
    ):

    if not isinstance(test_expression, bmw.SimpleBinaryExpression): raise RuntimeError('Must be simple boolean test_expression')
    if not test_expression.all: raise RuntimeError('Must be all')

    state = [False]*type_specification.nfeature

    for index, phase in zip(test_expression.indices, test_expression.phases):
        state[index] = False if phase else True
    
    if not type_specification.check_groups(state=state):
        return []

    rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]

    groups = [rule.predicate.indices for rule in rules]

    valid_states = []
    for indices in itertools.product(*[list(range(len(group)+1)) for group in groups]):
        state = [False]*type_specification.nfeature
        for index, group in zip(indices, groups):
            if index == 0: continue
            state[group[index-1]] = True
        if type_specification.check_valid(state):
            valid_states.append(state)
    return valid_states

# Doesn't work:
def force_solutions_following_implication(
    type_specification,
    test_expression,
    ):

    if not isinstance(test_expression, bmw.SimpleBinaryExpression): raise RuntimeError('Must be simple boolean test_expression')
    if not test_expression.all: raise RuntimeError('Must be all')

    state = [False]*type_specification.nfeature

    for index, phase in zip(test_expression.indices, test_expression.phases):
        state[index] = False if phase else True
    
    if not type_specification.check_groups(state=state):
        return []

    rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]

    groups = [rule.implication.indices for rule in rules]

    valid_states = []
    for indices in itertools.product(*[list(range(len(group)+1)) for group in groups]):
        state = [False]*type_specification.nfeature
        for index, group in zip(indices, groups):
            if index == 0: continue
            state[group[index-1]] = True
        if type_specification.check_valid(state):
            valid_states.append(state)
    return valid_states

    

problem = bmw.Problem.parse(filepath='../../data/3-refined')

test_counts, test_expressions = bmw.ProblemParser.parse_tests(filename='test7-fail.txt')

for test_expression in test_expressions:

    if not test_expression.is_simple_binary_expression: continue
    test_expression2 = test_expression.simple_binary_expression
    if not test_expression2.all: continue

    found = False
    
    for type_specification in problem.type_specifications:
    
        valid_states = force_solutions_following_predicate(
            type_specification=type_specification,
            test_expression=test_expression2,
            )

        if len(valid_states): 
            found = True
            break

    print('%5s : %s' % (found, test_expression))

        



