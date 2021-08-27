from .bmw_plugin import SimpleBinaryImplication
from .simple_binary_expression import SimpleBinaryExpression

def _simple_binary_implication__str__(self):
    return str(self.predicate) + ' => ' + str(self.implication)

SimpleBinaryImplication.__str__ = _simple_binary_implication__str__

@staticmethod
def _simple_binary_implication_parse(string): 
    predicate_str, implication_str = string.strip().split(' => ')
    return SimpleBinaryImplication(
        predicate=SimpleBinaryExpression.parse(predicate_str), 
        implication=SimpleBinaryExpression.parse(implication_str), 
        )

SimpleBinaryImplication.parse = _simple_binary_implication_parse
