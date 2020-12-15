# Utilities to help with wrapping.

# Set the Python version for the wrapper and set the paths to the executable and
# include/library directories. WRAP_PYTHON_VERSION can be "Default" or a
# specific major.minor version.
function(gtwrap_get_python_version WRAP_PYTHON_VERSION)
  # Unset these cached variables to avoid surprises when the python in the
  # current environment are different from the cached!
  unset(Python_EXECUTABLE CACHE)
  unset(Python_INCLUDE_DIRS CACHE)
  unset(Python_VERSION_MAJOR CACHE)
  unset(Python_VERSION_MINOR CACHE)

  # Allow override
  if(${WRAP_PYTHON_VERSION} STREQUAL "Default")
    # Check for Python3 or Python2 in order
    find_package(Python COMPONENTS Interpreter Development)

    set(WRAP_PYTHON_VERSION
        "${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}"
        CACHE STRING "The version of Python to build the wrappers against."
              FORCE)

    # message("========= ${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}")
    # message("========= WRAP_PYTHON_VERSION=${WRAP_PYTHON_VERSION}")
    # message("========= Python_EXECUTABLE=${Python_EXECUTABLE}")

  else()
    find_package(
      Python ${WRAP_PYTHON_VERSION}
      COMPONENTS Interpreter Development
      EXACT REQUIRED)
  endif()

  set(WRAP_PYTHON_VERSION
      ${WRAP_PYTHON_VERSION}
      PARENT_SCOPE)
  set(Python_FOUND
      ${Python_FOUND}
      PARENT_SCOPE)
  set(Python_EXECUTABLE
      ${Python_EXECUTABLE}
      PARENT_SCOPE)
  set(Python_INCLUDE_DIRS
      ${Python_INCLUDE_DIRS}
      PARENT_SCOPE)
  set(Python_LIBRARY_DIRS
      ${Python_LIBRARY_DIRS}
      PARENT_SCOPE)

endfunction()
