#pragma once

#include <vector>
#include <stdexcept>
#include "type_specification.hpp"
#include "test_set.hpp"

namespace bmw {

class Problem {

public:

Problem(
    const std::vector<std::vector<uint32_t>>& groups,
    const std::vector<TypeSpecification>& type_specifications,
    const TestSet& test_set,
    const std::vector<uint32_t>& test_groups) :
    groups_(groups),
    type_specifications_(type_specifications),
    test_set_(test_set),
    test_groups_(test_groups)
{
    // TODO
    if (test_set.ntest() != test_groups.size()) throw std::runtime_error("test_set.ntest != test_groups.size");
}

const std::vector<std::vector<uint32_t>>& groups() const { return groups_; }
const std::vector<TypeSpecification>& type_specifications() const { return type_specifications_; }
const TestSet& test_set() const { return test_set_; }
const std::vector<uint32_t>& test_groups() const { return test_groups_; }
    

private:

std::vector<std::vector<uint32_t>> groups_;
std::vector<TypeSpecification> type_specifications_;
TestSet test_set_;
std::vector<uint32_t> test_groups_;

};

} // namespace bmw
