import itertools

class LowSeedGenerator(object):

    @staticmethod
    def generate_rule_following_predicate(type_specification):
        
        state = [False]*type_specification.nfeature
        rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
        groups = [rule.predicate.indices for rule in rules]

        valid_states = []
        for indices in itertools.product(*[list(range(len(group)+1)) for group in groups]):
            state = [False]*type_specification.nfeature
            for index, group in zip(indices, groups):
                if index == 0: continue
                state[group[index-1]] = True
            if type_specification.check_valid(state):
                valid_states.append(state)
        return valid_states

    @staticmethod
    def generate_rule_following_implication(type_specification):
        
        state = [False]*type_specification.nfeature
        rules = [rule for rule in type_specification.rules if not rule.evaluate(state)]
        groups = [rule.implication.indices for rule in rules]

        valid_states = []
        for indices in itertools.product(*[list(range(len(group)+1)) for group in groups]):
            state = [False]*type_specification.nfeature
            for index, group in zip(indices, groups):
                if index == 0: continue
                state[group[index-1]] = True
            if type_specification.check_valid(state):
                valid_states.append(state)
        return valid_states
