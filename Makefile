all: audits tests

# --- ENVIRONMENT MANAGEMENT ---
.PHONY: clean

clean:
	git clean -fdX
	# poetry returns a non-zero exit status if the virtualenv doesn't exist so we ignore
	# errors.
	-poetry env remove 3.6
	-poetry env remove 3.7
	-poetry env remove 3.8
	-poetry env remove 3.9


.PHONY: clean _venv _venv_3.6 _venv_3.7 _venv_3.8 _venv_3.9 venvs
venvs: _venv_3.6 _venv_3.7 _venv_3.8 _venv_3.9

_venv:
	poetry env use ${PYTHON_VERSION}
	poetry install

_venv_3.6:
	PYTHON_VERSION=3.6 $(MAKE) _venv

_venv_3.7:
	PYTHON_VERSION=3.7 $(MAKE) _venv

_venv_3.8:
	PYTHON_VERSION=3.8 $(MAKE) _venv

_venv_3.9:
	PYTHON_VERSION=3.9 $(MAKE) _venv


# --- AUDITS ---
.PHONY: audits black flake8 isort markflow

# Runs all of our audits regardless of if any fail so we can get all relevant issues
audits:
	@status=0; \
	for target in black flake8 isort markflow; do \
		$(MAKE) $${target}; \
		status=$$(($$status + $$?)); \
		echo ""; \
	done; \
	if [ $$status -eq 0 ]; then \
	    echo "All Audits Succeeded!"; \
	else \
		echo "Some audits failed. :("; \
	fi; \
	exit $$status

black: _venv_3.8
	@echo Running $@ audit...
	git ls-files | egrep '.*\.pyi?$$' | xargs poetry run black --check
	@echo Success!

# pyi files provide type stubbing and can look weird to flake8, so we filter them out
flake8: _venv_3.8
	@echo Running $@ audit...
	git ls-files | egrep '.*\.py$$' | xargs poetry run flake8
	@echo Success!

isort: _venv_3.8
	@echo Running $@ audit...
	git ls-files | egrep '.*\.pyi?$$' | xargs poetry run isort --profile=black --check
	@echo Success!

markflow: _venv_3.8
	@echo Running $@ audit...
	git ls-files | egrep ".md$$" | grep -v "tests/" | xargs poetry run markflow --check
	@echo Success!

# --- TESTS ---
.PHONY: tests tests_3.6 tests_3.7 tests_3.8 tests_3.9
tests: utests mypy ensure_deps
tests_3.6: utests_3.6 ensure_deps_3.6
tests_3.7: utests_3.7 ensure_deps_3.7
tests_3.8: utests_3.8 mypy ensure_deps_3.8
tests_3.9: utests_3.9 ensure_deps_3.9

# Ensure dependencies are properly specified
.PHONY: ensure_deps _ensure_deps ensure_deps_3.6 ensure_deps_3.7 ensure_deps_3.8 ensure_deps_3.9
ensure_deps: ensure_deps_3.6 ensure_deps_3.7 ensure_deps_3.8 ensure_deps_3.9

_ensure_deps:
	# Ensure dependencies markflow needs didn't sneak into dev dependencies
	poetry env use ${PYTHON_VERSION}
	poetry install --no-dev
	echo -e "Hello\n--" | poetry run markflow

ensure_deps_3.6:
	PYTHON_VERSION=3.6 $(MAKE) _ensure_deps

ensure_deps_3.7:
	PYTHON_VERSION=3.7 $(MAKE) _ensure_deps

ensure_deps_3.8:
	PYTHON_VERSION=3.8 $(MAKE) _ensure_deps

ensure_deps_3.9:
	PYTHON_VERSION=3.9 $(MAKE) _ensure_deps

# MyPy
.PHONY: mypy mypy_lib mypy_tests
mypy: mypy_lib mypy_tests

mypy_lib: _venv_3.8
	# --implicity-reexport means that we don't have to explicitly tell mypy about our
	# modules' members via a `__all__`
	poetry env use 3.8
	MYPYPATH=$(CURDIR)/stubs poetry run mypy --strict --implicit-reexport markflow

mypy_tests: _venv_3.8
	# --implicity-reexport means that we don't have to explicitly tell mypy about our
	# modules' members via a `__all__`
	poetry env use 3.8
	MYPYPATH=$(CURDIR)/stubs poetry run mypy --strict --implicit-reexport tests

# Unit Tests
# Bit of  a misnomer since `test_files.py` is more of a system/integration test
.PHONY: utests _utests utests_3.6 utests_3.7 utests_3.8 utests_3.9
utests: utests_3.6 utests_3.7 utests_3.8 utests_3.9

_utests:
	poetry env use ${PYTHON_VERSION}
	cd $(CURDIR)/tests && poetry run pytest --cov=markflow --cov-report=term \
		--cov-report=html --junit-xml=junit.xml
	@echo For more detailed information, see $(CURDIR)/tests/htmlcov/index.html

utests_3.6: _venv_3.6
	PYTHON_VERSION=3.6 $(MAKE) _utests

utests_3.7: _venv_3.7
	PYTHON_VERSION=3.7 $(MAKE) _utests

utests_3.8: _venv_3.8
	PYTHON_VERSION=3.8 $(MAKE) _utests

utests_3.9: _venv_3.9
	PYTHON_VERSION=3.9 $(MAKE) _utests

# --- EXPORTING ---
.PHONY: package

package:
	poetry build

# --- CI CONTAINER ---
.PHONY: container

container:
	docker build . -t markflow_builder
