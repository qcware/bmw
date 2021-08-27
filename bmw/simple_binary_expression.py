from .bmw_plugin import SimpleBinaryExpression
import re

def _simple_binary_expression__str__(self):

    if self.any:
        join_char = '|'
    else:
        join_char = '&'

    return (' ' + join_char + ' ').join(['%sF%d' % (
        '~' if phase else '',
        index,
        ) for phase, index in zip(self.phases, self.indices)])

SimpleBinaryExpression.__str__ = _simple_binary_expression__str__

@staticmethod
def _simple_binary_expression_parse(string): 

    if string.count('|') and string.count('&'): raise RuntimeError('& and | in string -> non-simple expression') 

    reduction = 'any' if string.count('|') else 'all'

    if reduction == 'all':
        join_char = '&'
    elif reduction == 'any':
        join_char = '|'

    toks = re.split(r' \%s | ' % join_char, string.strip())

    indices = []
    phases = []
    for tok in toks:
        if tok[0] == '~':
            phases.append(True)
            tok = tok[1:]
        else:
            phases.append(False)

        if tok[0] != 'F': raise RuntimeError('No F')
        indices.append(int(tok[1:]))

    order = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(indices))]
    indices = [indices[_] for _ in order]
    phases = [phases[_] for _ in order]
    
    return SimpleBinaryExpression(
        any=True if reduction == 'any' else False,
        indices=indices,    
        phases=phases,
        )

SimpleBinaryExpression.parse = _simple_binary_expression_parse
