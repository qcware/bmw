#pragma once

#include <vector>
#include "type_specification.hpp"
#include "test_set.hpp"

namespace bmw {

class HammingStateGenerator {

public:

static
std::vector<std::vector<bool>> generate_distance_2(
    const std::vector<bool>& state,
    const TypeSpecification& type_specification,
    const TestSet& test_set,
    size_t nresult_target) 
{
    if (!type_specification.check_valid(state)) throw std::runtime_error("state is not valid");

    std::vector<std::vector<std::vector<bool>>> results(test_set.ntest() + 1);

    std::vector<bool> start(type_specification.nfeature());
    std::vector<bool> work(type_specification.nfeature());

    size_t min_acceptable_pass = 0;

    for (size_t index0 = 0; index0 < type_specification.ngroup(); index0++) {
        auto group0 = type_specification.groups()[index0];
    for (size_t index1 = index0 + 1; index1 < type_specification.ngroup(); index1++) {
        auto group1 = type_specification.groups()[index1];

        start = state;
        for (auto i0 : group0) start[i0] = false;
        for (auto i1 : group1) start[i1] = false;
        
        for (size_t pivot0 = 0; pivot0 < group0.size() + 1; pivot0++) {
        for (size_t pivot1 = 0; pivot1 < group1.size() + 1; pivot1++) {
            work = start; 
            if (pivot0 > 0) work[group0[pivot0 - 1]] = true;
            if (pivot1 > 0) work[group1[pivot1 - 1]] = true;
            if (!type_specification.check_rules(work)) continue;
            size_t npass = test_set.npass_state(work);
            if (npass < min_acceptable_pass) continue;
            results[npass].push_back(work);
        }}
        
        size_t wins = 0; 
        for (ssize_t npass = test_set.ntest(); npass >= 0; npass--) {
            min_acceptable_pass = npass;
            wins += results[npass].size();
            if (wins >= nresult_target) break;
        }

        for (size_t npass = 0; npass < min_acceptable_pass; npass++) {
            results[npass] = {};
        }
    }}
    
    std::vector<std::vector<bool>> results2;
    for (ssize_t npass = test_set.ntest(); npass >= 0; npass--) {
        results2.insert(results2.end(), results[npass].begin(), results[npass].end());
    }
    return results2;
}

};

} // namespace bmw
