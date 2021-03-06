#include "simple_binary_expression.hpp"
#include "simple_binary_implication.hpp"
#include "first_order_all_binary_expression.hpp"
#include "type_specification.hpp"
#include "test_set.hpp"
#include "problem.hpp"
#include "random_state_generator.hpp"
#include "threaded_random_state_generator.hpp"
#include "hamming_state_generator.hpp"
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
.def_property("active_feature_mask", &TypeSpecification::active_feature_mask, nullptr)
.def("check_nfeature", &TypeSpecification::check_nfeature, "state"_a)
.def("check_groups", &TypeSpecification::check_groups, "state"_a)
.def("check_rules", &TypeSpecification::check_rules, "state"_a)
.def("check_valid", &TypeSpecification::check_valid, "state"_a)
;

py::class_<TestSet>(m, "TestSet")
.def(py::init<
    const std::vector<uint32_t>&,
    const std::vector<FirstOrderAllBinaryExpression>&>(),
    "counts"_a, "expressions"_a)
.def_property("ntest", &TestSet::ntest, nullptr)
.def_property("counts", &TestSet::counts, nullptr)
.def_property("expressions", &TestSet::expressions, nullptr)
.def("npass_state", &TestSet::npass_state, "state"_a)
.def("npass_constellation", &TestSet::npass_constellation, "constellation"_a)
.def("passes_state", &TestSet::passes_state, "state"_a)
.def("passes_constellation", &TestSet::passes_constellation, "constellation"_a)
;

py::class_<Problem>(m, "Problem")
.def(py::init<
    const std::vector<std::vector<uint32_t>>&,
    const std::vector<TypeSpecification>&,
    const TestSet&,
    const std::vector<uint32_t>&>(),
    "groups"_a, "type_specifications"_a, "test_set"_a, "test_groups"_a)
.def_property("groups", &Problem::groups, nullptr)
.def_property("type_specifications", &Problem::type_specifications, nullptr)
.def_property("test_set", &Problem::test_set, nullptr)
.def_property("test_groups", &Problem::test_groups, nullptr)
;

py::class_<RandomStateGenerator>(m, "RandomStateGenerator")
.def(py::init<size_t>(), "seed"_a=0)
.def_static("build_random_seed", &RandomStateGenerator::build_random_seed)
.def_property("seed", &RandomStateGenerator::seed, nullptr)
.def_property("random_engine", &RandomStateGenerator::random_engine, nullptr)
.def("generate_random", &RandomStateGenerator::generate_random, "type"_a)
.def("generate_random_valid", &RandomStateGenerator::generate_random_valid, "type"_a, "niteration"_a=1)
.def("leapfrog_distance_2", &RandomStateGenerator::leapfrog_distance_2, "state"_a, "type_specification"_a, "test_set"_a, "niteration"_a)
.def("leapfrog_distance_2_mask", &RandomStateGenerator::leapfrog_distance_2_mask, "state"_a, "type_specification"_a, "test_set"_a, "niteration"_a, "mask"_a, "max_nfeature"_a=0)
.def("improve_constellation", &RandomStateGenerator::improve_constellation, "constellation"_a, "constellation_types"_a, "problem"_a, "niteration"_a)
;

py::class_<ThreadedRandomStateGenerator>(m, "ThreadedRandomStateGenerator")
.def(py::init<const std::vector<RandomStateGenerator>&>(), "generators"_a)
.def_static("build_random_seed", &ThreadedRandomStateGenerator::build_random_seed, "nthread"_a=0)
.def_static("omp_get_max_threads", &ThreadedRandomStateGenerator::omp_get_max_threads)
.def_property("nthread", &ThreadedRandomStateGenerator::nthread, nullptr)
.def_property("generators", &ThreadedRandomStateGenerator::generators, nullptr)
.def("leapfrog_distance_2_mask", &ThreadedRandomStateGenerator::leapfrog_distance_2_mask, "states"_a, "type_specifications"_a, "test_set"_a, "niteration"_a, "masks"_a, "max_nfeature"_a=0)
;

py::class_<HammingStateGenerator>(m, "HammingStateGenerator")
.def_static("generate_distance_2", &HammingStateGenerator::generate_distance_2, "state"_a, "type_specification"_a, "test_set"_a, "nresult_target"_a)
;

}

} // namespace bmw
