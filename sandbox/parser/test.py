import bmw
import time

start = time.time()

problem = bmw.TestCarProblem.parse_problem(filepath='../../data/3-refined')

print(time.time() - start)

start = time.time()
problem2 = bmw.TestCarProblemTranslater.translate_problem(problem=problem)
print(time.time() - start)

# for type2 in problem2:
#     print(type2.ngroup, type2.nfeature, type2.nactive_feature, type2.neffective_feature, type2.nrule)


print('%-4s : %11s %11s %11s %11s' % (
    'type',
    'nfeature',
    'nactive',
    'neffective',
    'nrule',
    ))
for tindex, type2 in enumerate(problem2):
    print('%-4d : %11d %11d %11.1f %11d' % (
        tindex,
        type2.nfeature,
        type2.nactive_feature,
        type2.neffective_feature,
        type2.nrule,
        ))
        
for index in range(len(problem.test_weights)):
    print('%11.3E : %3d %s' % (
        problem.test_weights[index],
        problem.test_counts[index],
        problem.test_expressions[index],
        ))
print(len(problem.test_weights))

# generator = bmw.RandomStateGenerator(seed=0)
generator = bmw.RandomStateGenerator.build_random_seed()

for tindex, typ in enumerate(problem2):

    print('Type %d:' % tindex)
# state = generator.generate_random(type=typ)
    state = [False]*typ.nfeature
    
    
    print(typ.check_nfeature(state))
    print(typ.check_groups(state))
    print(typ.check_rules(state))
    print(typ.check_valid(state))
    
    for rindex, rule in enumerate(typ.rules):
        if (rule.evaluate(state)): continue
        print('%3d : %4s %s' % (rindex, rule.evaluate(state), rule))

for tindex, typ in enumerate(problem2):

    state = [False]*typ.nfeature
    print('Type %2d: %1d' % (tindex, sum(1 for rule in typ.rules if not rule.evaluate(state))))


print("Special Type 5 Solution:")

typ = problem2[5]

state = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, True, True, False, False, False, True, False, False, False, False, True, False, True, True, False, False, False, False, True, False, True, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, True, True, False, False, True, False, False, False, True, False, False, False, True, False, False, False, False, False, True, True, True, False, False, True, False, True, True, True, False, True, False, False, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, False, True, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, True, True, False, True, False, False, False, False, False, False, False, True, False, False, True, True, False, False, True, False, False, False, True, False, False, True, False, True, False, False, True, True, False, True, False, False, True, False, True, False, True, False, False, False, False, False, False, False, False, True, True, False, True, False, False, False, False, False, True, False, False, False, False, False, False, True, False, True, False]

print(typ.check_nfeature(state))
print(typ.check_groups(state))
print(typ.check_rules(state))
print(typ.check_valid(state))

for rindex, rule in enumerate(typ.rules):
    if (rule.evaluate(state)): continue
    print('%3d : %4s %s' % (rindex, rule.evaluate(state), rule))

# print(problem2[5].nrule)
# import time
# start = time.time()
# # state = generator.generate_random_valid(type=problem2[5], niteration=1000000)
# state = generator.generate_random_valid(type=problem2[5], niteration=1000000)
# stop = time.time()
# delta = stop - start
# print(delta, 1000000 / delta)
# print(state)

if len(state) == 0: fuck()

sval = 0
for test in problem.test_expressions:
    print(test.evaluate(state))
    if test.evaluate(state): sval += 1
print(sval)

# type_rule = problem2[5]
# 
# state = bmw.GeneratorUtility.propose_random(type_rule=type_rule)
# print(state)
# 
# checks = bmw.GeneratorUtility.check_rules(type_rule=type_rule, state=state)
# print(checks)
# 
# print(len([_ for _ in checks if _]))
# print(len([_ for _ in checks if not _]))
# 
# print('Yo: %d' % len(type_rule.rules))
# 
# for k in range(1000000):
#     state = bmw.GeneratorUtility.propose_random(type_rule=type_rule)
#     checks = bmw.GeneratorUtility.check_rules(type_rule=type_rule, state=state)
#     if len([_ for _ in checks if not _]) < 5:
#         print(len([_ for _ in checks if not _]))
#     if len([_ for _ in checks if not _]) == 0:
#         print(state)
