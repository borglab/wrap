if(GTWRAP_PYTHON_PACKAGE_DIR)
  # packaged
  set(GTWRAP_PACKAGE_DIR "${GTWRAP_PYTHON_PACKAGE_DIR}")
else()
  set(GTWRAP_PACKAGE_DIR ${CMAKE_CURRENT_LIST_DIR}/..)
endif()

# Installed packages set these before including this module. Source-tree users
# need no separate script assignments.
if(NOT PYBIND_WRAP_SCRIPT)
  set(PYBIND_WRAP_SCRIPT "${CMAKE_CURRENT_LIST_DIR}/../scripts/pybind_wrap.py")
endif()
if(NOT PYBIND_SERIALIZATION_SCRIPT)
  set(PYBIND_SERIALIZATION_SCRIPT "${CMAKE_CURRENT_LIST_DIR}/../scripts/pybind_serialization.py")
endif()
file(GLOB_RECURSE GTWRAP_GENERATOR_SOURCES CONFIGURE_DEPENDS
     "${GTWRAP_PACKAGE_DIR}/gtwrap/*.py")

# Create one shared archive owner. Callers supply the complete polymorphic
# type family and use SERIALIZATION_LIBRARY in every participating pybind_wrap.
function(pybind_add_serialization_library target)
  cmake_parse_arguments(REG "" "BOOST_SERIALIZATION_TARGET"
    "INTERFACES;HEADERS;LINK_LIBRARIES;NAMESPACE_PREFIXES;IGNORE_CLASSES" ${ARGN})
  if(REG_UNPARSED_ARGUMENTS OR REG_KEYWORDS_MISSING_VALUES)
    message(FATAL_ERROR "Invalid pybind_add_serialization_library arguments")
  endif()
  if(NOT REG_INTERFACES OR NOT REG_HEADERS)
    message(FATAL_ERROR "A serialization library requires INTERFACES and HEADERS")
  endif()
  if(NOT target MATCHES "^[A-Za-z0-9_-]+$")
    message(FATAL_ERROR "Serialization target names may contain letters, digits, _ and -")
  endif()
  if(NOT REG_BOOST_SERIALIZATION_TARGET)
    set(REG_BOOST_SERIALIZATION_TARGET Boost::serialization)
  endif()
  if(NOT TARGET ${REG_BOOST_SERIALIZATION_TARGET})
    message(FATAL_ERROR "Provide an existing Boost.Serialization target")
  endif()
  set(directory "${CMAKE_CURRENT_BINARY_DIR}/gtwrap_serialization/${target}")
  set(arguments --name "${target}" --out-dir "${directory}")
  set(interfaces "")
  foreach(interface IN LISTS REG_INTERFACES)
    get_filename_component(interface "${interface}" ABSOLUTE BASE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
    list(APPEND interfaces "${interface}")
    list(APPEND arguments --src "${interface}")
  endforeach()
  foreach(header IN LISTS REG_HEADERS)
    list(APPEND arguments --include "${header}")
  endforeach()
  foreach(prefix IN LISTS REG_NAMESPACE_PREFIXES)
    list(APPEND arguments --namespace-prefix "${prefix}")
  endforeach()
  foreach(type IN LISTS REG_IGNORE_CLASSES)
    list(APPEND arguments --ignore "${type}")
  endforeach()
  if(UNIX)
    set(separator ":")
  else()
    set(separator ";")
  endif()
  set(outputs "")
  foreach(suffix .h _keys.h .cpp .json .map .exports)
    list(APPEND outputs "${directory}/${target}${suffix}")
  endforeach()
  add_custom_command(OUTPUT ${outputs}
    COMMAND ${CMAKE_COMMAND} -E env
      "PYTHONPATH=${GTWRAP_PACKAGE_DIR}${separator}$ENV{PYTHONPATH}"
      "${PYTHON_EXECUTABLE}" "${PYBIND_SERIALIZATION_SCRIPT}" ${arguments}
    DEPENDS ${interfaces} "${PYBIND_SERIALIZATION_SCRIPT}" ${GTWRAP_GENERATOR_SOURCES}
    VERBATIM)
  add_custom_target(${target}_generate DEPENDS ${outputs})
  add_library(${target} SHARED "${directory}/${target}.cpp")
  add_dependencies(${target} ${target}_generate)
  target_compile_features(${target} PUBLIC cxx_std_17)
  target_link_libraries(${target} PRIVATE ${REG_BOOST_SERIALIZATION_TARGET}
                                PUBLIC ${REG_LINK_LIBRARIES})
  target_include_directories(${target} PUBLIC "$<BUILD_INTERFACE:${directory}>")
  set_target_properties(${target} PROPERTIES
    CXX_VISIBILITY_PRESET hidden VISIBILITY_INLINES_HIDDEN ON
    WINDOWS_EXPORT_ALL_SYMBOLS OFF
    GTWRAP_SERIALIZATION_MANIFEST "${directory}/${target}.json")
  if(APPLE)
    # Match pybind_wrap's cross-DSO RTTI behavior for header-defined types.
    target_compile_options(${target} PRIVATE -fvisibility-ms-compat)
    target_link_options(${target} PRIVATE "LINKER:-exported_symbols_list,${directory}/${target}.exports")
    set_property(TARGET ${target} APPEND PROPERTY LINK_DEPENDS "${directory}/${target}.exports")
  elseif(UNIX)
    target_link_options(${target} PRIVATE "LINKER:--version-script=${directory}/${target}.map")
    set_property(TARGET ${target} APPEND PROPERTY LINK_DEPENDS "${directory}/${target}.map")
  endif()
endfunction()

# Get the Python version
include(GtwrapUtils)
message(STATUS "Checking Python Version")
gtwrap_get_python_version(${WRAP_PYTHON_VERSION})

message(STATUS "Setting Python version for wrapper")
set(PYBIND11_PYTHON_VERSION ${WRAP_PYTHON_VERSION})

if(GTWRAP_ADD_DOCSTRINGS)
  set(GTWRAP_PYTHON_DOCS_SOURCE "${CMAKE_SOURCE_DIR}/xml")
  message(STATUS "Python docstring generation is on. XML source: '${GTWRAP_PYTHON_DOCS_SOURCE}'")
else()
  message(STATUS "Python docstring generation is off.")
  set(GTWRAP_PYTHON_DOCS_SOURCE "")
endif()

# User-friendly Pybind11 wrapping and installing function. Builds a Pybind11
# module from the provided interface_headers. For example, for the interface
# header gtsam.h, this will build the wrap module 'gtsam_py.cc'.
#
# Arguments:
# ~~~
# target: The Make target
# interface_headers:  List of paths to the wrapper interface definition files. The top level interface file should be first.
# generated_cpp: The name of the cpp file which is generated from the tpl file.
# module_name: The name of the Python module to use.
# top_namespace: The C++ namespace under which the code to be wrapped exists.
# ignore_classes: CMake list of classes to ignore from wrapping.
# install_path: Destination to install the library.
# module_template: The template file (.tpl) from which to generate the Pybind11 module.
# libs: Libraries to link with.
# dependencies: Dependencies which need to be built before the wrapper.
# use_boost_serialization (optional): Flag indicating whether to include Boost.
function(
  pybind_wrap
  target
  interface_headers
  generated_cpp
  module_name
  top_namespace
  ignore_classes
  module_template
  libs
  dependencies)
  set(ExtraMacroArgs ${ARGN})
  set(USE_BOOST_SERIALIZATION OFF)
  if(ExtraMacroArgs)
    list(POP_FRONT ExtraMacroArgs USE_BOOST_SERIALIZATION)
  endif()
  cmake_parse_arguments(WRAP "" "SERIALIZATION_LIBRARY" "" ${ExtraMacroArgs})
  if(WRAP_UNPARSED_ARGUMENTS OR WRAP_KEYWORDS_MISSING_VALUES)
    message(FATAL_ERROR "Invalid pybind_wrap optional arguments")
  endif()
  set(_serialization_args "")
  set(_serialization_depends "")
  if(WRAP_SERIALIZATION_LIBRARY)
    if(NOT USE_BOOST_SERIALIZATION)
      message(FATAL_ERROR "SERIALIZATION_LIBRARY requires serialization enabled")
    endif()
    if(NOT TARGET ${WRAP_SERIALIZATION_LIBRARY})
      message(FATAL_ERROR "Unknown serialization library ${WRAP_SERIALIZATION_LIBRARY}")
    endif()
    get_target_property(_manifest ${WRAP_SERIALIZATION_LIBRARY} GTWRAP_SERIALIZATION_MANIFEST)
    if(NOT _manifest)
      message(FATAL_ERROR "Target was not created by pybind_add_serialization_library")
    endif()
    set(_serialization_args --serialization-manifest "${_manifest}")
    set(_serialization_depends "${_manifest}" ${WRAP_SERIALIZATION_LIBRARY}_generate)
  endif()
  if(USE_BOOST_SERIALIZATION)
    set(_WRAP_BOOST_ARG "--use-boost-serialization")
  else(USE_BOOST_SERIALIZATION)
    set(_WRAP_BOOST_ARG "")
  endif(USE_BOOST_SERIALIZATION)

  if(UNIX)
    set(GTWRAP_PATH_SEPARATOR ":")
  else()
    set(GTWRAP_PATH_SEPARATOR ";")
  endif()

  # Create a copy of interface_headers so we can freely manipulate it
  set(interface_files ${interface_headers})

  # Pop the main interface file so that interface_files has only submodules.
  list(POP_FRONT interface_files main_interface)

  # Convert .i file names to .cpp file names.
  foreach(interface_file ${interface_files})
    # This block gets the interface file name and does the replacement
    get_filename_component(interface ${interface_file} NAME_WLE)
    set(cpp_file "${interface}.cpp")
    list(APPEND cpp_files ${cpp_file})

    # Wrap the specific interface header
    # This is done so that we can create CMake dependencies in such a way so that when changing a single .i file,
    # the others don't need to be regenerated.
    # NOTE: We have to use `add_custom_command` so set the dependencies correctly.
    # https://stackoverflow.com/questions/40032593/cmake-does-not-rebuild-dependent-after-prerequisite-changes
    add_custom_command(
      OUTPUT ${cpp_file}
      COMMAND
        ${CMAKE_COMMAND} -E env
        "PYTHONPATH=${GTWRAP_PACKAGE_DIR}${GTWRAP_PATH_SEPARATOR}$ENV{PYTHONPATH}"
        ${PYTHON_EXECUTABLE} ${PYBIND_WRAP_SCRIPT} --src "${interface_file}"
          --out "${cpp_file}"  --module_name ${module_name}
          --top_module_namespaces "${top_namespace}" --ignore ${ignore_classes}
          --template ${module_template} --is_submodule ${_WRAP_BOOST_ARG}
          --xml_source "${GTWRAP_PYTHON_DOCS_SOURCE}" ${_serialization_args}
      DEPENDS ${_serialization_depends} ${GTWRAP_GENERATOR_SOURCES} "${PYBIND_WRAP_SCRIPT}" "${interface_file}" ${module_template} "${module_name}/specializations/${interface}.h" "${module_name}/preamble/${interface}.h"
      VERBATIM)

  endforeach()

  get_filename_component(main_interface_name ${main_interface} NAME_WLE)
  set(main_cpp_file "${main_interface_name}.cpp")
  list(PREPEND cpp_files ${main_cpp_file})

  add_custom_command(
    OUTPUT ${main_cpp_file}
    COMMAND
      ${CMAKE_COMMAND} -E env
      "PYTHONPATH=${GTWRAP_PACKAGE_DIR}${GTWRAP_PATH_SEPARATOR}$ENV{PYTHONPATH}"
      ${PYTHON_EXECUTABLE} ${PYBIND_WRAP_SCRIPT} --src "${interface_headers}"
      --out "${generated_cpp}" --module_name ${module_name}
      --top_module_namespaces "${top_namespace}" --ignore ${ignore_classes}
      --template ${module_template} ${_WRAP_BOOST_ARG}
      --xml_source "${GTWRAP_PYTHON_DOCS_SOURCE}" ${_serialization_args}
    DEPENDS ${_serialization_depends} ${GTWRAP_GENERATOR_SOURCES} "${PYBIND_WRAP_SCRIPT}" "${main_interface}" ${module_template} "${module_name}/specializations/${main_interface_name}.h" "${module_name}/specializations/${main_interface_name}.h"
    VERBATIM)

    add_custom_target(pybind_wrap_${module_name} DEPENDS ${cpp_files})

  pybind11_add_module(${target} "${cpp_files}")

  if(APPLE)
    # `type_info` objects will become "weak private external" if the templated
    # class is initialized implicitly even if we explicitly export them with
    # `WRAP_EXPORT`. If that happens, the `type_info` for the same templated
    # class will diverge between shared libraries, causing `dynamic_cast` to
    # fail. This is mitigated by telling Clang to mimic the MSVC behavior. See
    # https://developer.apple.com/library/archive/technotes/tn2185/_index.html#//apple_ref/doc/uid/DTS10004200-CH1-SUBSECTION2
    # https://github.com/CppMicroServices/CppMicroServices/pull/82/files
    # https://www.russellmcc.com/posts/2013-08-03-rtti.html
    target_compile_options(${target} PRIVATE "-fvisibility-ms-compat")
  endif()

  add_dependencies(${target} pybind_wrap_${module_name})
  if(WRAP_SERIALIZATION_LIBRARY)
    target_link_libraries(${target} PRIVATE ${WRAP_SERIALIZATION_LIBRARY})
    add_dependencies(${target} ${WRAP_SERIALIZATION_LIBRARY}_generate)
  endif()

  if(NOT "${libs}" STREQUAL "")
    target_link_libraries(${target} PRIVATE "${libs}")
  endif()
  if(NOT "${dependencies}" STREQUAL "")
    add_dependencies(${target} ${dependencies})
  endif()
endfunction()

# Helper function to install python scripts and handle multiple build types
# where the scripts should be installed to all build type toolboxes
#
# Arguments:
# ~~~
# source_directory: The source directory to be installed. "The last component
#     of each directory name is appended to the destination directory but a
#     trailing slash may be used to avoid this because it leaves the last
#     component empty."
#     (https://cmake.org/cmake/help/v3.3/command/install.html?highlight=install#installing-directories)
# dest_directory: The destination directory to install to.
# patterns: list of file patterns to install
# ~~~
function(install_python_scripts source_directory dest_directory patterns)
  set(patterns_args "")
  set(exclude_patterns "")

  foreach(pattern ${patterns})
    list(APPEND patterns_args PATTERN "${pattern}")
  endforeach()
  if(WRAP_BUILD_TYPE_POSTFIXES)
    foreach(build_type ${CMAKE_CONFIGURATION_TYPES})
      string(TOUPPER "${build_type}" build_type_upper)
      if(${build_type_upper} STREQUAL "RELEASE")
        set(build_type_tag "") # Don't create release mode tag on installed
                               # directory
      else()
        set(build_type_tag "")
      endif()
      # Split up filename to strip trailing '/' in GTSAM_PY_INSTALL_PATH if
      # there is one
      get_filename_component(location "${dest_directory}" PATH)
      get_filename_component(name "${dest_directory}" NAME)
      install(
        DIRECTORY "${source_directory}"
        DESTINATION "${location}/${name}${build_type_tag}"
        CONFIGURATIONS "${build_type}"
        FILES_MATCHING ${patterns_args}
        PATTERN "${exclude_patterns}" EXCLUDE)
    endforeach()
  else()
    install(
      DIRECTORY "${source_directory}"
      DESTINATION "${dest_directory}"
      FILES_MATCHING ${patterns_args}
      PATTERN "${exclude_patterns}" EXCLUDE)
  endif()

endfunction()

# Helper function to install specific files and handle multiple build types
# where the scripts should be installed to all build type toolboxes
#
# Arguments:
# ~~~
# source_files: The source files to be installed.
# dest_directory: The destination directory to install to.
function(install_python_files source_files dest_directory)

  if(WRAP_BUILD_TYPE_POSTFIXES)
    foreach(build_type ${CMAKE_CONFIGURATION_TYPES})
      string(TOUPPER "${build_type}" build_type_upper)
      set(build_type_tag "")
      # Split up filename to strip trailing '/' in WRAP_PY_INSTALL_PATH if there
      # is one
      get_filename_component(location "${dest_directory}" PATH)
      get_filename_component(name "${dest_directory}" NAME)
      install(
        FILES "${source_files}"
        DESTINATION "${location}/${name}${build_type_tag}"
        CONFIGURATIONS "${build_type}")
    endforeach()
  else()
    install(FILES "${source_files}" DESTINATION "${dest_directory}")
  endif()

endfunction()

# ~~~
# Copy over the directory from source_folder to dest_foler
# ~~~
function(copy_directory source_folder dest_folder)
  if(${source_folder} STREQUAL ${dest_folder})
    return()
  endif()

  file(
    GLOB files
    LIST_DIRECTORIES true
    RELATIVE "${source_folder}"
    "${source_folder}/*")
  foreach(path_file ${files})
    get_filename_component(folder ${path_file} PATH)
    get_filename_component(ext ${path_file} EXT)
    set(ignored_ext ".tpl" ".h")
    list(FIND ignored_ext "${ext}" _index)
    if(${_index} GREATER -1)
      continue()
    endif()
    # Create REAL folder
    file(MAKE_DIRECTORY "${dest_folder}")

    # Delete if it exists
    file(REMOVE "${dest_folder}/${path_file}")

    # Get OS dependent path to use in copy
    file(TO_NATIVE_PATH "${source_folder}/${path_file}" target)

    file(COPY ${target} DESTINATION ${dest_folder})

  endforeach(path_file)
endfunction(copy_directory)
