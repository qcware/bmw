class ProblemAnalysis(object):

    @staticmethod
    def analyze_groups(problem):

        s = ''
        for gindex, group in enumerate(problem.groups):
            s += 'Group %2d : Size %3d\n' % (gindex, len(group))

            for index in group:  
                s += 'F%-3d : %s\n' % (index,
                    ''.join([('X' if typ.active_feature_mask[index] else ' ') for typ in problem.type_specifications]),
                    )
                

        return s
        
