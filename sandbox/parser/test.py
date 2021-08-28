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

generator = bmw.RandomStateGenerator(seed=0)

state = generator.generate_random(type=problem2[0])
print(state)

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
