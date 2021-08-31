#pragma once

#include <vector>
#include <algorithm>
#include <stdexcept>

namespace bmw {

class SimpleBinaryExpression {

public:

SimpleBinaryExpression(
    bool any,
    const std::vector<uint32_t>& indices,
    const std::vector<bool>& phases) :
    any_(any),
    indices_(indices),
    phases_(phases)
{
    if (indices_.size() != phases_.size()) throw std::runtime_error("indices.size != phases.size");
    if (!std::is_sorted(indices_.begin(), indices_.end())) throw std::runtime_error("indices is not sorted");
    if (std::adjacent_find(indices_.begin(), indices_.end()) != indices_.end()) throw std::runtime_error("indices is not unique");

    if (indices_.size() == 0) throw std::runtime_error("indices.size == 0");

    max_index_ = indices_.size() ? *std::max_element(indices_.begin(), indices_.end()) : 0;
}

bool any() const { return any_; }
bool all() const { return !any_; }
const std::vector<uint32_t>& indices() const { return indices_; }
const std::vector<bool>& phases() const { return phases_; }

uint32_t max_index() const { return max_index_; }

bool evaluate(const std::vector<bool>& state) const 
{
    if (max_index_ >= state.size()) throw std::runtime_error("max_index >= state.size");
    
    if (any_) {
        for (size_t index = 0; index < indices_.size(); index++) {
            if (phases_[index] ? (!state[indices_[index]]) : state[indices_[index]]) return true;
        }     
        return false;
    } else { 
        for (size_t index = 0; index < indices_.size(); index++) {
            if (!(phases_[index] ? (!state[indices_[index]]) : state[indices_[index]])) return false;
        }     
        return true;
    }
}

private:

bool any_; // any (True) or all (False) ?
std::vector<uint32_t> indices_;
std::vector<bool> phases_;

// memoization
uint32_t max_index_;

};

} // namespace bmw
