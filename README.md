# py-timeout
A python package to enable one to execute a given function with a timeout period. This is intended to work with
blocking, non-async, functions.

## Cloning
To clone the project and the required submodules run:
> git clone --recurse-submodules https://github.com/AndrewEC/py-timeout.git

## Usage

The timeout utility can be used simply by importing the timeout decorator and applying it to a function
like in the example below::

```python
from timeout import timeout

@timeout(3)  # 3 is the number of seconds to wait before the timeout occurs
def perform_action():
    ...
```

**Note**: This decorator was only intended to be used on blocking, non-async, functions.

## Quality Metrics
To run the unit and integration tests simply run the `CreateVenv.ps1` script the run the build script via:
`python build.py`

This build script, in addition to the running the unit and mutation tests, will also generate coverage reports,
install required dependencies, ensure a proper virtual environment is active, generate Sphinx docs, and run Flake8.

Separate mutation and unit test coverage reports will be generated at the following locations:
* Unit Tests - `html/index.html`
* Mutation Tests - `html/index.html`
