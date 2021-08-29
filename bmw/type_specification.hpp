#pragma once

#include "simple_binary_implication.hpp"

#include <vector>
#include <stdexcept>
#include <cmath>

namespace bmw {

class TypeSpecification {

public:

TypeSpecification(
    size_t nfeature,
    const std::vector<std::vector<uint32_t>>& groups,
    const std::vector<SimpleBinaryImplication>& rules)  :
    nfeature_(nfeature),
    groups_(groups),
    rules_(rules)
{
    for (auto group : groups_) {
        if (!std::is_sorted(group.begin(), group.end())) throw std::runtime_error("group is not sorted");
        if (std::adjacent_find(group.begin(), group.end()) != group.end()) throw std::runtime_error("group is not unique");
    }

    for (auto group : groups_) {
        active_features_.insert(active_features_.end(), group.begin(), group.end());
    }
    std::sort(active_features_.begin(), active_features_.end());
    if (std::adjacent_find(active_features_.begin(), active_features_.end()) != active_features_.end()) throw std::runtime_error("groups have collisions");

    for (auto index : active_features_) {
        if (index >= nfeature_) throw std::runtime_error("index >= nfeature");
    }

    for (auto rule : rules_) {
        if (rule.max_index() >= nfeature_) throw std::runtime_error("rule.max_index >= nfeature");
    }

    active_feature_mask_.resize(nfeature_);
    for (uint32_t index : active_features_) {
        active_feature_mask_[index] = true;
    }
}

size_t nfeature() const { return nfeature_; }
size_t nactive_feature() const { return active_features_.size(); }

double neffective_feature() const 
{ 
    double size = 0.0;    
    for (auto group : groups_) {
        size += log2(group.size() + 1.0); 
    }
    return size;
}

size_t ngroup() const { return groups_.size(); }
size_t nrule() const { return rules_.size(); }

const std::vector<std::vector<uint32_t>>& groups() const { return groups_; }
const std::vector<SimpleBinaryImplication>& rules() const { return rules_; }

const std::vector<uint32_t>& active_features() const { return active_features_; }
const std::vector<bool>& active_feature_mask() const { return active_feature_mask_; }

bool check_nfeature(
    const std::vector<bool>& state) const
{
    return state.size() == nfeature_;
}

bool check_groups(
    const std::vector<bool>& state) const
{   
    if (!check_nfeature(state)) return false;
    for (size_t index = 0; index < nfeature_; index++) {
        if (state[index] && !active_feature_mask_[index]) return false;
    }
    return true;
}

bool check_rules(
    const std::vector<bool>& state) const
{
    if (!check_nfeature(state)) return false;
    for (auto rule : rules_) {
        if (!rule.evaluate(state)) return false;
    }
    return true;
}

bool check_valid(
    const std::vector<bool>& state) const
{
    if (!check_groups(state)) return false;
    if (!check_rules(state)) return false;
    return true;
}

private:

size_t nfeature_;
std::vector<std::vector<uint32_t>> groups_;
std::vector<SimpleBinaryImplication> rules_;

// memoization (sorted)
std::vector<uint32_t> active_features_;

std::vector<bool> active_feature_mask_;

};

} // namespace bmw
