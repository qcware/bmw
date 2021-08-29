#pragma once

#include <vector>
#include "first_order_all_binary_expression.hpp"

namespace bmw {

class TestSet {

public:

TestSet(
    const std::vector<double>& weights,
    const std::vector<uint32_t>& counts,
    const std::vector<FirstOrderAllBinaryExpression>& expressions) :
    weights_(weights),
    counts_(counts),
    expressions_(expressions)
{
    if (weights_.size() != counts_.size()) throw std::runtime_error("weights.size != counts.size");
    if (expressions_.size() != counts_.size()) throw std::runtime_error("expressions.size != counts.size");
}

const std::vector<double>& weights() const { return weights_; }
const std::vector<uint32_t>& counts() const { return counts_; }
const std::vector<FirstOrderAllBinaryExpression>& expressions() const { return expressions_; }

std::pair<size_t, double> check_state(
    const std::vector<bool>& state) const 
{
    size_t npass = 0;
    double weight = 0.0; 
    for (size_t index = 0; index < weights_.size(); index++) {
        if (expressions_[index].evaluate(state)) {
            npass++;
            weight += weights_[index];
        }
    }

    return std::pair<size_t, double>(npass, weight);
}

std::pair<size_t, double> check_constellation(
    const std::vector<std::vector<bool>>& constellation) const 
{
    size_t npass = 0;
    double weight = 0.0; 
    for (size_t index = 0; index < weights_.size(); index++) {
        uint32_t count = 0;
        for (auto state : constellation) {
            if (expressions_[index].evaluate(state)) count++;
        }
        if (count >= counts_[index]) {
            npass++;
            weight += weights_[index];
        }
    }

    return std::pair<size_t, double>(npass, weight);
}

private:

std::vector<double> weights_;
std::vector<uint32_t> counts_;
std::vector<FirstOrderAllBinaryExpression> expressions_;

};

} // namespace bmw
