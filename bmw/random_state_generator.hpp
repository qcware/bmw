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

private:

size_t seed_;
std::mt19937 random_engine_;

};

} // namespace bmw
