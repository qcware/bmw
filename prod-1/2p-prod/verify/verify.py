import numpy as np

np.set_printoptions(threshold=np.inf)

sol = np.load('../test-2.npz')
constellation = sol['constellation']
constellation_type_indices = sol['constellation_type_indices']

num_allowed_features = len(constellation[0])

with open('../../../data/2-polished/types.txt') as f:
    line = f.readlines()
    dat_types_index = np.zeros(len(line),dtype=int)
    dat_types_allowed = np.full((len(line),num_allowed_features),False,dtype=bool)
    i_car = 0
    for l in line:
        lhs, rhs = l.split(' : ',1)
        lhs = lhs.replace('T','')
        dat_types_index[i_car] = lhs
        rhs = rhs.replace('F','')
        rhssplit = rhs.split(' ')
        rhssplit.pop()
        newrhs = np.array(rhssplit)
        for elem in newrhs:
            dat_types_allowed[i_car][int(elem)] = True
        i_car += 1

with open('../../../data/2-polished/groups.txt') as f:
    line = f.readlines()
    dat_feat_groups = np.full((len(line),num_allowed_features),False,dtype=bool)
    i_group = 0
    for l in line:
        l = l.replace('F','')
        lsplit = l.split(' ')
        lsplit.pop()
        group = np.array(lsplit)
        for elem in group:
            dat_feat_groups[i_group][int(elem)] = True
        i_group += 1

with open('../../../data/2-polished/rules.txt') as f:
    line = f.readlines()
    dat_condition_forced_all_on = np.full((len(line),num_allowed_features),False,dtype=bool)
    dat_condition_forced_all_off = np.full((len(line),num_allowed_features),False,dtype=bool)
    dat_condition_forced_any_on = np.full((len(line),num_allowed_features),False,dtype=bool)
    dat_implication_forced_all_on = np.full((len(line),num_allowed_features),False,dtype=bool)
    dat_implication_forced_all_off = np.full((len(line),num_allowed_features),False,dtype=bool)
    dat_implication_forced_any_on = np.full((len(line),num_allowed_features),False,dtype=bool)
    dat_rule_type = np.zeros(len(line),dtype=int)
    rule_index = 0
    for l in line:
        lhs, rhs = l.split(' : ',1)
        lhs = lhs.replace('T','')
        dat_rule_type[rule_index] = lhs
        rhs = rhs.replace('F','')
        if '=>' in rhs:
            condition, implication = rhs.split('=> ',1)
            condition = condition.replace(' ','')
            implication = implication.replace(' ','')
            if '&' in condition:            # forced all
                forced_cond = condition.split('&')
                for feat_i in forced_cond:
                    if '~' in feat_i:         # forced off
                        feat_i = feat_i.replace('~','')
                        dat_condition_forced_all_off[rule_index][int(feat_i)] = True
                    else:                   # forced on
                        dat_condition_forced_all_on[rule_index][int(feat_i)] = True
            elif '|' in condition:          # forced any
                forced_any_cond = condition.split('|')
                for feat_j in forced_any_cond:
                    dat_condition_forced_any_on[rule_index][int(feat_j)] = True

            else:                           # forced all (one elem conditions)
                if '~' in condition:        # forced off
                    feat_k = condition.replace('~','')
                    dat_condition_forced_all_off[rule_index][int(feat_k)] = True
                else:                       # forced on
                    feat_k = condition
                    dat_condition_forced_all_on[rule_index][int(feat_k)] = True
        
            if '&' in implication:            # forced all
                forced_imp = implication.split('&')
                forced_imp[-1] = forced_imp[-1].strip()
                for feat_l in forced_imp:
                    if '~' in feat_l:         # forced off
                        feat_l = feat_l.replace('~','')
                        dat_implication_forced_all_off[rule_index][int(feat_l)] = True
                    else:                     # forced on
                        dat_implication_forced_all_on[rule_index][int(feat_l)] = True
            elif '|' in implication:          # forced any
                forced_any_imp = implication.split('|')
                forced_any_imp[-1] = forced_any_imp[-1].strip()
                for feat_m in forced_any_imp:
                    dat_implication_forced_any_on[rule_index][int(feat_m)] = True
            else:                             # on or off, single elem cond
                if '~' in implication:
                    feat_n = implication.replace('~','')
                    dat_implication_forced_all_off[rule_index][int(feat_n)] = True
                else: 
                    feat_o = implication
                    dat_implication_forced_all_on[rule_index][int(feat_o)] = True
        else:
            print('line does not contain implication')
        rule_index += 1


for sol_car_i in range(len(constellation)):
    sol_car_type = constellation_type_indices[sol_car_i]
    for k in range(len(constellation[0])):
        sol_car_feature = constellation[sol_car_i,k]

# is feature allowed? [types.txt]
        if sol_car_feature == True:
            assert sol_car_feature == dat_types_allowed[sol_car_type][k], 'Test car doesn\'t comply with type rules.'

# is only one feature in group active? [groups.txt]
            for group in range(len(dat_feat_groups)):
                if dat_feat_groups[group][k] == True:
                    # compare test car features to group features, overlap should be 1.
                    comparison = np.logical_and(constellation[sol_car_i][:],dat_feat_groups[group][:])
                    comp = sum(comparison)
                    assert comp == 1, 'Test car doesn\'t comply with group rules.'

#  do necessary constraints followed? [rules.txt]
num_tests_passed = np.zeros(len(constellation),dtype=int)
for sol_car_i in range(len(constellation)):
    sol_car_type = constellation_type_indices[sol_car_i]
    for rule_i in range(len(dat_rule_type)):
        rule_i_type = dat_rule_type[rule_i]
        if sol_car_type == rule_i_type:
            cond_num_on = sum(dat_condition_forced_all_on[rule_i][:])
            cond_num_off = sum(dat_condition_forced_all_off[rule_i][:])
            cond_num_any = sum(dat_condition_forced_any_on[rule_i][:])
            impl_num_on = sum(dat_implication_forced_all_on[rule_i][:])
            impl_num_off = sum(dat_implication_forced_all_off[rule_i][:])
            impl_num_any = sum(dat_implication_forced_any_on[rule_i][:])
            if (cond_num_on != 0 and cond_num_off == 0 and cond_num_any == 0):              # conditions: on only
                test_cond_on = np.logical_and(constellation[sol_car_i][:],dat_condition_forced_all_on[rule_i][:])
                if sum(test_cond_on) == sum(dat_condition_forced_all_on[rule_i][:]):        # if cond met, check imp 
                    if (impl_num_on != 0 and impl_num_off == 0 and impl_num_any == 0):      # implication: on only
                        test_impl_on = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_all_on[rule_i][:])
                        if sum(test_impl_on) == sum(dat_implication_forced_all_on[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off != 0 and impl_num_any == 0):      # implication: off only
                        temp = np.invert(constellation[sol_car_i][:])
                        test_impl_off = np.logical_and(temp,dat_implication_forced_all_off[rule_i][:])
                        if sum(test_impl_off) == sum(dat_implication_forced_all_off[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off == 0 and impl_num_any != 0):       # implication: any only
                        test_impl_any = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_any_on[rule_i][:])
                        if sum(test_impl_any) == 1:
                            num_tests_passed[sol_car_i] += 1
            if (cond_num_on == 0 and cond_num_off != 0 and cond_num_any == 0):               # conditions: off only
                temp = np.invert(constellation[sol_car_i][:])
                test_cond_off = np.logical_and(temp,dat_condition_forced_all_off[rule_i][:])
                if sum(test_cond_off) == sum(dat_condition_forced_all_off[rule_i][:]):       # if cond met, check imp
                    if (impl_num_on != 0 and impl_num_off == 0 and impl_num_any == 0):       # implication: on only
                        test_impl_on = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_all_on[rule_i][:])
                        if sum(test_impl_on) == sum(dat_implication_forced_all_on[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off != 0 and impl_num_any == 0):       # implication: off only
                        temp = np.invert(constellation[sol_car_i][:])
                        test_impl_off = np.logical_and(temp,dat_implication_forced_all_off[rule_i][:])
                        if sum(test_impl_off) == sum(dat_implication_forced_all_off[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off == 0 and impl_num_any != 0):       # implication: any only
                        test_impl_any = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_any_on[rule_i][:])
                        if sum(test_impl_any) == 1:
                            num_tests_passed[sol_car_i] += 1
            if (cond_num_on == 0 and cond_num_off == 0 and cond_num_any != 0):               # conditions: any only
                test_cond_any = np.logical_and(constellation[sol_car_i][:],dat_condition_forced_any_on[rule_i][:])
                if sum(test_cond_any) == 1:
                    if (impl_num_on != 0 and impl_num_off == 0 and impl_num_any == 0):       # implication: on only
                        test_impl_on = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_all_on[rule_i][:])
                        if sum(test_impl_on) == sum(dat_implication_forced_all_on[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off != 0 and impl_num_any == 0):       # implication: off only
                        temp = np.invert(constellation[sol_car_i][:])
                        test_impl_off = np.logical_and(temp,dat_implication_forced_all_off[rule_i][:])
                        if sum(test_impl_off) == sum(dat_implication_forced_all_off[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off == 0 and impl_num_any != 0):       # implication: any only
                        test_impl_any = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_any_on[rule_i][:])
                        if sum(test_impl_any) == 1:
                            num_tests_passed[sol_car_i] += 1
            if (cond_num_on != 0 and cond_num_off != 0 and cond_num_any == 0):               # conditions: on and off only
                test_cond_on = np.logical_and(constellation[sol_car_i][:],dat_condition_forced_all_on[rule_i][:])
                temp = np.invert(constellation[sol_car_i][:])
                test_cond_off = np.logical_and(temp,dat_condition_forced_all_off[rule_i][:])
                if ((sum(test_cond_on) == sum(dat_condition_forced_all_on[rule_i][:])) and (sum(test_cond_off) == sum(dat_condition_forced_all_off[rule_i][:]))):
                    if (impl_num_on != 0 and impl_num_off == 0 and impl_num_any == 0):       # implication: on only
                        test_impl_on = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_all_on[rule_i][:])
                        if sum(test_impl_on) == sum(dat_implication_forced_all_on[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off != 0 and impl_num_any == 0):       # implication: off only
                        temp = np.invert(constellation[sol_car_i][:])
                        test_impl_off = np.logical_and(temp,dat_implication_forced_all_off[rule_i][:])
                        if sum(test_impl_off) == sum(dat_implication_forced_all_off[rule_i][:]):
                            num_tests_passed[sol_car_i] += 1
                    if (impl_num_on == 0 and impl_num_off == 0 and impl_num_any != 0):       # implication: any only
                        test_impl_any = np.logical_and(constellation[sol_car_i][:],dat_implication_forced_any_on[rule_i][:])
                        if sum(test_impl_any) == 1:
                            num_tests_passed[sol_car_i] += 1

            # never encountered
            # if (cond_num_on != 0 and cond_num_off == 0 and cond_num_any != 0):     # conditons: on and any only
            # if (cond_num_on == 0 and cond_num_off != 0 and cond_num_any != 0):     # conditions: off and any only
            # if (cond_num_on!= 0 and cond_num_off != 0 and cond_num_any != 0):      # conditions on and off and any
            # if (impl_num_on != 0 and impl_num_off != 0 and impl_num_any == 0):     # implication: on and off
            # if (impl_num_on != 0 and impl_num_off == 0 and impl_num_any != 0):     # implication: on and any
            # if (impl_num_on == 0 and impl_num_off != 0 and impl_num_any != 0):     # implication: off and any
            # if (impl_num_on!= 0 and impl_num_off != 0 and impl_num_any != 0):      # implication and and off and any
assert np.count_nonzero(num_tests_passed) == len(constellation), 'Test car doesn\'t comply with rules.'

