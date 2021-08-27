from .bmw_plugin import FirstOrderAllBinaryExpression
from .simple_binary_expression import SimpleBinaryExpression
import re

def _first_order_all_binary_expression__str__(self):

    return ' '.join(['( %s )' % str(_) for _ in self.expressions])

FirstOrderAllBinaryExpression.__str__ = _first_order_all_binary_expression__str__

@staticmethod
def _first_order_all_binary_expression_parse(string): 

    # TODO: More rigorous checks that these do not nest

    tokens = re.split(r'\) \(|\(|\)', string)
    tokens = [_.strip() for _ in tokens]
    tokens = [_ for _ in tokens if len(_)]

    return FirstOrderAllBinaryExpression(
        expressions=[SimpleBinaryExpression.parse(_) for _ in tokens],
        ) 

FirstOrderAllBinaryExpression.parse = _first_order_all_binary_expression_parse
