#include "simple_binary_expression.hpp"
#include "simple_binary_implication.hpp"
#include "first_order_all_binary_expression.hpp"
#include "type_specification.hpp"
#include "test_set.hpp"
#include "random_state_generator.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
using namespace py::literals;

namespace bmw {

PYBIND11_MODULE(bmw_plugin, m) {

py::class_<SimpleBinaryExpression>(m, "SimpleBinaryExpression")
.def(py::init<bool, const std::vector<uint32_t>&, const std::vector<bool>&>(), "any"_a, "indices"_a, "phases"_a)
.def_property("any", &SimpleBinaryExpression::any, nullptr)
.def_property("all", &SimpleBinaryExpression::all, nullptr)
.def_property("indices", &SimpleBinaryExpression::indices, nullptr)
.def_property("phases", &SimpleBinaryExpression::phases, nullptr)
.def_property("max_index", &SimpleBinaryExpression::max_index, nullptr)
.def("evaluate", &SimpleBinaryExpression::evaluate, "state"_a)
;

py::class_<SimpleBinaryImplication>(m, "SimpleBinaryImplication")
.def(py::init<const SimpleBinaryExpression&, const SimpleBinaryExpression&>(), "predicate"_a, "implication"_a)
.def_property("predicate", &SimpleBinaryImplication::predicate, nullptr)
.def_property("implication", &SimpleBinaryImplication::implication, nullptr)
.def_property("max_index", &SimpleBinaryImplication::max_index, nullptr)
.def("evaluate", &SimpleBinaryImplication::evaluate, "state"_a)
;

py::class_<FirstOrderAllBinaryExpression>(m, "FirstOrderAllBinaryExpression")
.def(py::init<const std::vector<SimpleBinaryExpression>&>(), "expressions"_a)
.def_property("expressions", &FirstOrderAllBinaryExpression::expressions, nullptr)
.def_property("is_simple_binary_expression", &FirstOrderAllBinaryExpression::is_simple_binary_expression, nullptr)
.def_property("simple_binary_expression", &FirstOrderAllBinaryExpression::simple_binary_expression, nullptr)
.def("evaluate", &FirstOrderAllBinaryExpression::evaluate, "state"_a)
;

py::class_<TypeSpecification>(m, "TypeSpecification")
.def(py::init<
    size_t,
    const std::vector<std::vector<uint32_t>>&,
    const std::vector<SimpleBinaryImplication>&>(),
    "nfeature"_a, "groups"_a, "rules"_a)
.def_property("nfeature", &TypeSpecification::nfeature, nullptr)
.def_property("neffective_feature", &TypeSpecification::neffective_feature, nullptr)
.def_property("nactive_feature", &TypeSpecification::nactive_feature, nullptr)
.def_property("ngroup", &TypeSpecification::ngroup, nullptr)
.def_property("nrule", &TypeSpecification::nrule, nullptr)
.def_property("groups", &TypeSpecification::groups, nullptr)
.def_property("rules", &TypeSpecification::rules, nullptr)
.def_property("active_features", &TypeSpecification::active_features, nullptr)
.def("check_nfeature", &TypeSpecification::check_nfeature, "state"_a)
.def("check_groups", &TypeSpecification::check_groups, "state"_a)
.def("check_rules", &TypeSpecification::check_rules, "state"_a)
.def("check_valid", &TypeSpecification::check_valid, "state"_a)
;

py::class_<TestSet>(m, "TestSet")
.def(py::init<
    const std::vector<double>&,
    const std::vector<uint32_t>&,
    const std::vector<FirstOrderAllBinaryExpression>&>(),
    "weights"_a, "counts"_a, "expressions"_a)
.def_property("weights", &TestSet::weights, nullptr)
.def_property("counts", &TestSet::counts, nullptr)
.def_property("expressions", &TestSet::expressions, nullptr)
.def("check_state", &TestSet::check_state, "state"_a)
.def("check_constellation", &TestSet::check_constellation, "constellation"_a)
;

py::class_<RandomStateGenerator>(m, "RandomStateGenerator")
.def(py::init<size_t>(), "seed"_a=0)
.def_static("build_random_seed", &RandomStateGenerator::build_random_seed)
.def_property("seed", &RandomStateGenerator::seed, nullptr)
.def_property("random_engine", &RandomStateGenerator::random_engine, nullptr)
.def("generate_random", &RandomStateGenerator::generate_random, "type"_a)
.def("generate_random_valid", &RandomStateGenerator::generate_random_valid, "type"_a, "niteration"_a=1)
;

}

} // namespace bmw
