import numpy as np
import re

class GeneratorUtility(object):

    @staticmethod
    def propose_random(
        *,
        type_rule,
        ):

        state = [False]*type_rule.nfeature
        for group in type_rule.groups:
            val = np.random.randint(len(group)+1)
            if val == 0: continue
            state[group[val-1]] = True
        return state

    @staticmethod
    def check_rules(
        *,
        type_rule,
        state,
        ):

        return [rule.evaluate(state) for rule in type_rule.rules]
        

class PrimitiveTypeRule(object):

    def __init__(
        self,
        *,
        nfeature,
        groups,
        rules,
        ):

        self.nfeature = nfeature
        self.groups = groups
        self.rules = rules

    @property
    def nactive_feature(self):
        return len(set().union(*self.groups))

    @property
    def neffective_feature(self):
        return sum(np.log2(len(_) + 1) for _ in self.groups)

    @property
    def ngroup(self):
        return len(self.groups)

    @property
    def nrule(self):
        return len(self.rules)

# => Parsing-Level Context-Aware Representation <= #

class SimpleBinaryExpression(object):

    def __init__(   
        self,
        *,
        indices,
        phases,
        reduction='all',
        ):

        self.indices = indices
        self.phases = phases 
        self.reduction = reduction

        if len(self.indices) != len(self.phases): raise RuntimeError('len(indices) != len(phases)')
        if not self.reduction in ['all', 'any']: raise RuntimeError('Unknown reduction: %s' % self.reduction)

    def __str__(self):

        if self.reduction == 'all':
            join_char = '&'
        elif self.reduction == 'any':
            join_char = '|'

        return (' ' + join_char + ' ').join(['%sF%d' % (
            '~' if phase else '',
            index,
            ) for phase, index in zip(self.phases, self.indices)])

    @staticmethod
    def parse(string): 

        if string.count('|') and string.count('&'): raise RuntimeError('& and | in string -> non-simple expression') 

        reduction = 'any' if string.count('|') else 'all'

        if reduction == 'all':
            join_char = '&'
        elif reduction == 'any':
            join_char = '|'

        toks = string.strip().split(' ' + join_char + ' ')

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

        return SimpleBinaryExpression(
            indices=indices,    
            phases=phases,
            reduction=reduction,
            )

    def evaluate(
        self,
        state,
        ):

        vals = [(not state[index] if phase else state[index]) for index, phase in zip(self.indices, self.phases)]
        if self.reduction == 'all':
            return all(vals)
        elif self.reduction == 'any':
            return any(vals)
        

class SimpleBinaryImplication(object):

    def __init__(
        self,
        *,
        predicate,
        implication,
        ):

        self.predicate = predicate
        self.implication = implication

    def __str__(self):
        return str(self.predicate) + ' => ' + str(self.implication)

    @staticmethod
    def parse(string):
        predicate_str, implication_str = string.strip().split(' => ')
        return SimpleBinaryImplication(
            predicate=SimpleBinaryExpression.parse(predicate_str), 
            implication=SimpleBinaryExpression.parse(implication_str), 
            )

    def evaluate(
        self,
        state,
        ):

        if self.predicate.evaluate(state):
            return self.implication.evaluate(state)
        else:
            return True
    
class TestCarProblem(object):

    def __init__(
        self,
        *,
        nfeature,
        types,
        groups,
        rules,
        ):

        self.nfeature = nfeature
        self.types = types
        self.groups = groups
        self.rules = rules

class TestCarProblemParser(object):

    @staticmethod
    def parse_types(
        *,
        filename,
        ):

        lines = open(filename).readlines()

        re1 = re.compile('^(\S+)\s+:\s+(.*)$') 
        re2 = re.compile('^T(\d+)$')
        re3 = re.compile('^F(\d+)$')

        types = []
        for lindex, line in enumerate(lines):
            mobj = re.match(re1, line)
            if mobj is None: raise RuntimeError('Type line %d is malformed: %s' % (lindex, line))
            type_str = mobj.group(1).strip()
            feature_str = mobj.group(2).strip()
            type_int = int(re.match(re2, type_str).group(1)) 
            if (type_int != lindex): raise RuntimeError('Type line %d is not lexical: T%d' (lindex, type_int))
            tokens = list(sorted([int(re.match(re3, _).group(1)) for _ in feature_str.split()]))
            if len(set(tokens)) != len(tokens): raise RuntimeError('Type has duplicate features')
            types.append(tokens)

        return types

    @staticmethod
    def parse_groups(
        *,
        filename,
        ):

        lines = open(filename).readlines()

        re0 = re.compile('^F(\d+)$')
        groups = []
        for lindex, line in enumerate(lines):
            tokens = list(sorted([int(re.match(re0, _).group(1)) for _ in line.strip().split()]))
            if len(set(tokens)) != len(tokens): raise RuntimeError('Group has duplicate features')
            groups.append(tokens)

        return groups

    @staticmethod
    def parse_rules(
        *,
        filename,
        ):

        lines = open(filename).readlines()

        re0 = re.compile('^T(\d+)\s*:(.*)$')
        ntype = max([int(re.match(re0, _).group(1)) for _ in lines]) + 1

        rules = [[] for _ in range(ntype)]
        for line in lines:
            mobj = re.match(re0, line)
            implication = SimpleBinaryImplication.parse(mobj.group(2))
            rules[int(mobj.group(1))].append(implication)

        return rules

    @staticmethod
    def parse_problem(
        *,
        filepath,
        ):

        types = TestCarProblemParser.parse_types(filename='%s/types.txt' % filepath)
        groups = TestCarProblemParser.parse_groups(filename='%s/groups.txt' % filepath)
        rules = TestCarProblemParser.parse_rules(filename='%s/rules.txt' % filepath)

        nfeature = max(
            max([max(_) for _ in types]),
            max([max(_) for _ in groups]),
            ) + 1

        return TestCarProblem(
            nfeature=nfeature,
            types=types,
            groups=groups, 
            rules=rules,
            )
            
class TestCarProblemTranslater(object):

    @staticmethod
    def translate_problem(
        *,
        problem,
        ):

        types = []

        for tindex, type2 in enumerate(problem.types):

            reduced_groups = [[_ for _ in group if _ in type2] for group in problem.groups]
            reduced_groups = [_ for _ in reduced_groups if len(_)] 

            all_indices = [index for sublist in reduced_groups for index in sublist]

            trivial_groups = [[index] for index in type2 if not index in all_indices]
    
            groups = reduced_groups + trivial_groups

            type3 = PrimitiveTypeRule(
                nfeature=problem.nfeature,
                groups=groups,
                rules=problem.rules[tindex],
                ) 

            types.append(type3)

        return types

        

            
        
        
            
        
        
