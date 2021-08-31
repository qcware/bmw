import bmw

problem = bmw.Problem.parse(filepath='../../data/3-refined')

print(bmw.ProblemAnalysis.analyze_groups(problem=problem))
