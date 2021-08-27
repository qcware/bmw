import bmw

tests = [
    'F218',
    'F218 & ~F233',
    '( F218 | F219 ) F233',
    '( F139 | F121 ) F218 ( F220 | F224 ) F233',
    '( F121 | F139 | F141 ) ~F144',
    '( F121 | F139 | F141 ) ( ~F144 )',
    ]

for test in tests:

    expr = bmw.FirstOrderAllBinaryExpression.parse(test)
    print(expr)
    
