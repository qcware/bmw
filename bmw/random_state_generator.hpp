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

private:

size_t seed_;
std::mt19937 random_engine_;

};

} // namespace bmw
