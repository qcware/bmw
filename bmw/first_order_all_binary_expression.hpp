#pragma once

#include "simple_binary_expression.hpp"

#include <vector>
#include <stdexcept>

namespace bmw {

class FirstOrderAllBinaryExpression {

public:

FirstOrderAllBinaryExpression(
    const std::vector<SimpleBinaryExpression>& expressions) : 
    expressions_(expressions)
{
    if (expressions_.size() == 0) throw std::runtime_error("expressions.size == 0");
}

const std::vector<SimpleBinaryExpression>& expressions() const { return expressions_; }

uint32_t max_index() const 
{
    return std::max_element(expressions_.begin(), expressions_.end(), [](const SimpleBinaryExpression& a, const SimpleBinaryExpression& b) { return a.max_index() < b.max_index(); })->max_index(); 
}

bool is_simple_binary_expression() const { return expressions_.size() == 1; }

const SimpleBinaryExpression& simple_binary_expression() const 
{
    if (!is_simple_binary_expression()) throw std::runtime_error("Not a simple binary expression");
    return expressions_[0];
}

bool evaluate(const std::vector<bool>& state) const
{
    for (auto expression : expressions_) {
        if (!expression.evaluate(state)) return false;
    }
    return true;
}

private:

std::vector<SimpleBinaryExpression> expressions_;

};

} // namespace bmw
