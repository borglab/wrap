#include <pybind11/pybind11.h>
{includes}
{boost_class_export}
namespace py = pybind11;
{submodules}
{declaration_module_def} {{
{wrapped_declarations}
}}
{binding_module_def} {{
{wrapped_bindings}
}}
{module_def} {{
{module_init}
}}
