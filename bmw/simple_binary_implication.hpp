#pragma once

#include "simple_binary_expression.hpp"

namespace bmw {

class SimpleBinaryImplication {

public:

SimpleBinaryImplication(
    const SimpleBinaryExpression& predicate,
    const SimpleBinaryExpression& implication) :
    predicate_(predicate),
    implication_(implication)
    {}

const SimpleBinaryExpression& predicate() const { return predicate_; }
const SimpleBinaryExpression& implication() const { return implication_; }

uint32_t max_index() const 
{ 
    return std::max(predicate_.max_index(), implication_.max_index());
}

bool evaluate(const std::vector<bool>& state) const 
{
    return predicate_.evaluate(state) ? implication_.evaluate(state) : true;
}

private:

SimpleBinaryExpression predicate_;
SimpleBinaryExpression implication_;

};
    
} // namespace bmw
