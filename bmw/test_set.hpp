#pragma once

#include <vector>
#include "first_order_all_binary_expression.hpp"

namespace bmw {

class TestSet {

public:

TestSet(
    const std::vector<uint32_t>& counts,
    const std::vector<FirstOrderAllBinaryExpression>& expressions) :
    counts_(counts),
    expressions_(expressions)
{
    if (expressions_.size() != counts_.size()) throw std::runtime_error("expressions.size != counts.size");
}

size_t ntest() const { return counts_.size(); }

const std::vector<uint32_t>& counts() const { return counts_; }
const std::vector<FirstOrderAllBinaryExpression>& expressions() const { return expressions_; }

size_t check_state(
    const std::vector<bool>& state) const 
{
    size_t npass = 0;
    for (size_t index = 0; index < counts_.size(); index++) {
        if (expressions_[index].evaluate(state)) {
            npass++;
        }
    }

    return npass;
}

size_t check_constellation(
    const std::vector<std::vector<bool>>& constellation) const 
{
    size_t npass = 0;
    for (size_t index = 0; index < counts_.size(); index++) {
        uint32_t count = 0;
        for (auto state : constellation) {
            if (expressions_[index].evaluate(state)) count++;
        }
        if (count >= counts_[index]) {
            npass++;
        }
    }

    return npass;
}

private:

std::vector<uint32_t> counts_;
std::vector<FirstOrderAllBinaryExpression> expressions_;

};

} // namespace bmw
