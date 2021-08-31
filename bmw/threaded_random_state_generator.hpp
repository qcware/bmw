#pragma once 

#include <vector>
#include "random_state_generator.hpp"

#include <omp.h>

namespace bmw {

class ThreadedRandomStateGenerator {

public:

ThreadedRandomStateGenerator(
    const std::vector<RandomStateGenerator>& generators) :
    generators_(generators)
    {}

size_t nthread() const { return generators_.size(); }
const std::vector<RandomStateGenerator>& generators() const { return generators_; }

static
ThreadedRandomStateGenerator build_random_seed(size_t nthread) 
{
    std::vector<RandomStateGenerator> generators;
    for (size_t index = 0; index < nthread; index++) {
        generators.push_back(RandomStateGenerator::build_random_seed());
    }
    return ThreadedRandomStateGenerator(generators);
}

std::vector<std::vector<bool>> leapfrog_distance_2_mask(
    const std::vector<std::vector<bool>>& states,
    const std::vector<TypeSpecification>& type_specifications,
    const TestSet& test_set,
    size_t niteration,
    const std::vector<std::vector<bool>>& masks)
{
    if (states.size() != type_specifications.size()) throw std::runtime_error("states.size != type_specifications.size");
    if (states.size() != masks.size()) throw std::runtime_error("states.size != masks.size");
    
    std::vector<std::vector<bool>> results = states;

    #pragma omp parallel for num_threads(nthread()) schedule(dynamic, 1)
    for (size_t index = 0; index < states.size(); index++) {
        size_t tindex = omp_get_thread_num();
        results[index] = generators_[tindex].leapfrog_distance_2_mask(
            states[index],
            type_specifications[index],
            test_set,
            niteration,
            masks[index]);
    }
    
    return results;
}

private:

std::vector<RandomStateGenerator> generators_;

};

} // namespace bmw
