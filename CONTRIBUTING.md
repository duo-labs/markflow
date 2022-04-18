# Contributing to MarkFlow

The following are the contributing guidelines when making changes to this project.

Development depends on the installation of **make**, for coordinating execution of the
underlying tools, **poetry**, for managing our **Python** environments and the
**MarkFlow** package itself, and the supported versions of **Python** (current, 3.6,
3.7, 3.8, and 3.9). You can generally get away with only having one version of
**Python** installed and testing against that. The GitHub builds will validate your
changes against all versions of **Python** anyway.

## Making Changes

([Step 0: Checkout the documentation on the implementation of the tool.](
IMPLEMENTATION.md))

To check to see if your submission is buildable, simply run `make`. If everything
passes, you are good to go on to [Submitting Changes](#submitting-changes). To
understand what that's doing, though, read on.

### Running Tools

All tools that are available in the poetry environment (including **MarkFlow**) can
easily be added to your command line as the commands themselves by running
`. poetry-aliases.sh`. An additional alias, `markflow-markflow`, is also provided to
easily run **MarkFlow** against non-test files.

### Running Audits

We run checks against every commit to ensure all files follow standards we enforce. The
audits we run are as follows:

```shell
# Ensure all Markdown files would not be reformatted by us :)
make markflow
# Ensure all python files would not be reformatted by black
make black
# Ensure our import are all sorted
make isort
# Ensure all pythons follow a few other rules enforced by flake8
make flake
# Run all of the above. Every command will be run regardless of the others failing.
make audits
```

The poetry environment comes with [**black**][black], and of course **MarkFlow**, so you
can quickly run the tools with `poetry run black` or `poetry run markflow` or just drop
into a shell with them by running `poetry shell`.

[black]: https://black.readthedocs.io/en/latest/

### Running Tests

We test our code through unit and system tests that are run by [**pytest**][pytest] and
strict type checking enforced via [**mypy**][mypy]. The commands to run them are as
follows:

```shell
# Run tests in /tests
make pytests
# Run mypy against the markflow library
make mypy_lib
# Run mypy against our tests
make mypy_tests
# Run all of the above in order, exiting on the first failure.
make tests
```

Why do we exit on first failure unlike audits? Tests are noisier and this makes the
failures more obvious. In most cases the audits are unlikely to fill up your screen, but
even then.

[mypy]: http://mypy-lang.org/
[pytest]: https://docs.pytest.org/en/latest/

### Submitting Changes

Once you've made all your changes, create a [pull request][pr]. Someone will be with you
shortly.

If you are correcting a bug you've seen when processing a **Markdown** file, add it and
the expected output to `tests/files`. In the folder, inputs and outputs are matched up
based on their leading numeric. So, `0010_in_tests.md`'s expected output is
`0010_out_tests.md`. The [README has a section on anonymizing text](README.md#issues) if
you're worried about leaking sensitive information.

[pr]: https://github.com/duo-labs/markflow/pulls

## Proposing Changes

If you want to propose a rule change, like making inline code blocks split across lines,
feel free to open an [issue][issues].

[issues]: https://github.com/duo-labs/markflow/issues

# Duplicating CI Locally

The build in CI simply runs the make commands in the container defined by the root
`Dockerfile`. You'll of course need [**docker**][docker]. Once you do, to build the
image run:

```shell
make container
```

To run commands in the container, you'll need to mount our source. The following should
do the trick when run from the project's directory:

```shell
docker run -v "`pwd`:/src" -w /src markflow_builder make
# Build the wheel
docker run -v "`pwd`:/src" -w /src markflow_builder make package
```

[docker]: https://www.docker.com/
