import numpy as np
import re

from .simple_binary_implication import SimpleBinaryImplication
from .first_order_all_binary_expression import FirstOrderAllBinaryExpression

# => Parsing-Level Context-Aware Representation <= #

class TestCarProblem(object):

    def __init__(
        self,
        *,
        nfeature,
        types,
        groups,
        rules,
        test_weights,
        test_counts,
        test_expressions,
        ):

        self.nfeature = nfeature
        self.types = types
        self.groups = groups
        self.rules = rules
        self.test_weights = test_weights
        self.test_counts = test_counts
        self.test_expressions = test_expressions

        if len(self.test_weights) != len(self.test_counts): raise RuntimeError('len(test_weights) != len(test_counts)')
        if len(self.test_weights) != len(self.test_expressions): raise RuntimeError('len(test_weights) != len(test_expressions)')

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
    def parse_tests(
        *,
        filename,
        ):

        lines = open(filename).readlines()

        re0 = re.compile('^(\d+)\s*:(.*)$')

        test_weights = []
        test_counts = []
        test_expressions = []
        
        for line in lines:
            mobj = re.match(re0, line)
            count = int(mobj.group(1))
            expression = FirstOrderAllBinaryExpression.parse(mobj.group(2).strip())
            weight = 1.0
            test_weights.append(weight)
            test_counts.append(count)
            test_expressions.append(expression)
        
        return test_weights, test_counts, test_expressions

    @staticmethod
    def parse_problem(
        *,
        filepath,
        ):

        types = TestCarProblem.parse_types(filename='%s/types.txt' % filepath)
        groups = TestCarProblem.parse_groups(filename='%s/groups.txt' % filepath)
        rules = TestCarProblem.parse_rules(filename='%s/rules.txt' % filepath)

        test_weights, test_counts, test_expressions = TestCarProblem.parse_tests(filename='%s/tests.txt' % filepath)

        nfeature = max(
            max([max(_) for _ in types]),
            max([max(_) for _ in groups]),
            ) + 1

        return TestCarProblem(
            nfeature=nfeature,
            types=types,
            groups=groups, 
            rules=rules,
            test_weights=test_weights,
            test_counts=test_counts,
            test_expressions=test_expressions,
            )

from .type_specification import TypeSpecification
from .test_set import TestSet

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

            type3 = TypeSpecification(
                nfeature=problem.nfeature,
                groups=groups,
                rules=problem.rules[tindex],
                ) 

            types.append(type3)

        test_set = TestSet(
            weights=problem.test_weights,
            counts=problem.test_counts,
            expressions=problem.test_expressions,
            )

        return types, test_set


