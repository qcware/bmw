import bmw

expr = bmw.SimpleBinaryExpression.parse('F12')
print(expr)

expr = bmw.SimpleBinaryExpression.parse('~F12')
print(expr)

expr = bmw.SimpleBinaryExpression.parse('~F12 | F13 | F22')
print(expr)

expr = bmw.SimpleBinaryExpression.parse('~F12 & F13 & ~F22')
print(expr)

impl = bmw.SimpleBinaryImplication.parse('~F13 & F35 => ~F22 | ~F34')
print(impl)

print(expr.max_index)
