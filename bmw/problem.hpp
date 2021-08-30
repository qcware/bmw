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
    const TestSet& test_set) :
    groups_(groups),
    type_specifications_(type_specifications),
    test_set_(test_set)
{
    // TODO
}

const std::vector<std::vector<uint32_t>>& groups() const { return groups_; }
const std::vector<TypeSpecification>& type_specifications() const { return type_specifications_; }
const TestSet& test_set() const { return test_set_; }
    

private:

std::vector<std::vector<uint32_t>> groups_;
std::vector<TypeSpecification> type_specifications_;
TestSet test_set_;

};

} // namespace bmw
