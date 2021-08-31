#pragma once

#include "type_specification.hpp"

#include <random>
#include <vector>

namespace bmw {

class RandomStateGenerator {

public:

RandomStateGenerator(size_t seed=0) : 
    seed_(seed),
    random_engine_(seed)
    {}

static
RandomStateGenerator build_random_seed()
{
    std::random_device dev;
    return RandomStateGenerator(dev());
}

size_t seed() const { return seed_; }
const std::mt19937& random_engine() const { return random_engine_; }

std::vector<bool> generate_random(
    const TypeSpecification& type)
{
    std::vector<bool> state(type.nfeature());
    for (auto group : type.groups()) {
        std::uniform_int_distribution<uint32_t> dist(0, group.size());
        uint32_t index = dist(random_engine_);
        if (index == 0) continue;
        state[group[index-1]] = true;
    }
    return state;
}

std::vector<bool> generate_random_valid(
    const TypeSpecification& type,
    size_t niteration=1)
{
    std::vector<bool> state(type.nfeature());
    for (size_t iteration = 0; iteration < niteration; iteration++) {
        std::fill(state.begin(), state.end(), false);
        for (auto group : type.groups()) {
            std::uniform_int_distribution<uint32_t> dist(0, group.size());
            uint32_t index = dist(random_engine_);
            if (index == 0) continue;
            state[group[index-1]] = true;
        }
        if (type.check_rules(state)) {
            return state;
        }
    }
    return {};
}

std::vector<bool> leapfrog_distance_2(
    const std::vector<bool>& state,
    const TypeSpecification& type_specification,
    const TestSet& test_set,
    size_t niteration)
{
    if (!type_specification.check_valid(state)) throw std::runtime_error("state is not valid");

    size_t npass = test_set.npass_state(state);

    std::vector<bool> result = state;
    std::vector<bool> trial = state;
    
    for (size_t iteration = 0; iteration < niteration; iteration++) {

        std::uniform_int_distribution<uint32_t> dist1(0, type_specification.ngroup() - 1);
        uint32_t group_index0 = dist1(random_engine_);
        uint32_t group_index1 = dist1(random_engine_);
        if (group_index0 == group_index1) continue;

        auto group0 = type_specification.groups()[group_index0];
        auto group1 = type_specification.groups()[group_index1];

        trial = result;
        for (auto i0 : group0) trial[i0] = false;
        for (auto i1 : group1) trial[i1] = false;

        std::uniform_int_distribution<uint32_t> dist2(0, 1);
        bool active0 = dist2(random_engine_);
        bool active1 = dist2(random_engine_);
            
        if (active0) {
            std::uniform_int_distribution<uint32_t> dist3(0, group0.size() - 1);
            uint32_t pivot = dist3(random_engine_);
            trial[group0[pivot]] = true;
        } 

        if (active1) {
            std::uniform_int_distribution<uint32_t> dist3(0, group1.size() - 1);
            uint32_t pivot = dist3(random_engine_);
            trial[group1[pivot]] = true;
        } 
                 
        if (!type_specification.check_rules(trial)) continue;
        
        size_t npass2 = test_set.npass_state(trial);
        
        if (npass2 > npass) {
            npass = npass2;
            result = trial;
        }
    }
    
    return result;
}

std::vector<bool> leapfrog_distance_2_mask(
    const std::vector<bool>& state,
    const TypeSpecification& type_specification,
    const TestSet& test_set,
    size_t niteration,
    const std::vector<bool>& mask)
{
    if (!type_specification.check_valid(state)) throw std::runtime_error("state is not valid");
    if (mask.size() != state.size()) throw std::runtime_error("mask is wrong size");

    size_t npass = test_set.npass_state(state);

    std::vector<bool> result = state;
    std::vector<bool> trial = state;
    
    for (size_t iteration = 0; iteration < niteration; iteration++) {

        std::uniform_int_distribution<uint32_t> dist1(0, type_specification.ngroup() - 1);
        uint32_t group_index0 = dist1(random_engine_);
        uint32_t group_index1 = dist1(random_engine_);
        if (group_index0 == group_index1) continue;

        auto group0 = type_specification.groups()[group_index0];
        auto group1 = type_specification.groups()[group_index1];

        for (auto i0 : group0) if (mask[i0]) continue;
        for (auto i1 : group1) if (mask[i1]) continue;

        trial = result;
        for (auto i0 : group0) trial[i0] = false;
        for (auto i1 : group1) trial[i1] = false;

        std::uniform_int_distribution<uint32_t> dist2(0, 1);
        bool active0 = dist2(random_engine_);
        bool active1 = dist2(random_engine_);
            
        if (active0) {
            std::uniform_int_distribution<uint32_t> dist3(0, group0.size() - 1);
            uint32_t pivot = dist3(random_engine_);
            trial[group0[pivot]] = true;
        } 

        if (active1) {
            std::uniform_int_distribution<uint32_t> dist3(0, group1.size() - 1);
            uint32_t pivot = dist3(random_engine_);
            trial[group1[pivot]] = true;
        } 
                 
        if (!type_specification.check_rules(trial)) continue;
        
        size_t npass2 = test_set.npass_state(trial);
        
        if (npass2 > npass) {
            npass = npass2;
            result = trial;
        }
    }
    
    return result;
}

std::vector<std::vector<bool>> improve_constellation(
    const std::vector<std::vector<bool>>& constellation,
    const std::vector<size_t>& constellation_types,
    const Problem& problem,
    size_t niteration)
{
    for (size_t index = 0; index < constellation.size(); index++) {
        if (!problem.type_specifications()[constellation_types[index]].check_valid(constellation[index])) throw std::runtime_error("constellation is not valid");
    }

    std::vector<std::vector<bool>> result = constellation;
    std::vector<std::vector<bool>> trial = constellation;

    size_t npass = problem.test_set().npass_constellation(result);

    for (size_t iteration = 0; iteration < niteration; iteration++) {
        size_t index = iteration % constellation.size(); 

        auto type_specification = problem.type_specifications()[constellation_types[index]];

        std::uniform_int_distribution<uint32_t> dist1(0, type_specification.ngroup() - 1);
        uint32_t group_index0 = dist1(random_engine_);
        uint32_t group_index1 = dist1(random_engine_);
        if (group_index0 == group_index1) continue;

        auto group0 = type_specification.groups()[group_index0];
        auto group1 = type_specification.groups()[group_index1];

        trial = result;
        for (auto i0 : group0) trial[index][i0] = false;
        for (auto i1 : group1) trial[index][i1] = false;

        std::uniform_int_distribution<uint32_t> dist2(0, 1);
        bool active0 = dist2(random_engine_);
        bool active1 = dist2(random_engine_);
            
        if (active0) {
            std::uniform_int_distribution<uint32_t> dist3(0, group0.size() - 1);
            uint32_t pivot = dist3(random_engine_);
            trial[index][group0[pivot]] = true;
        } 

        if (active1) {
            std::uniform_int_distribution<uint32_t> dist3(0, group1.size() - 1);
            uint32_t pivot = dist3(random_engine_);
            trial[index][group1[pivot]] = true;
        } 
                 
        if (!type_specification.check_rules(trial[index])) continue;
        
        size_t npass2 = problem.test_set().npass_constellation(trial);
        
        if (npass2 > npass) {
            npass = npass2;
            result = trial;
        }
    }

    return result;
}    

private:

size_t seed_;
std::mt19937 random_engine_;

};

} // namespace bmw
