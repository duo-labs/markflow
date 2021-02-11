alias black="poetry run black"
alias flake8="poetry run flake8"
alias isort="poetry run isort --profile=black"
alias markflow="poetry run markflow"
alias mypy="poetry run mypy"
alias pytest="poetry run pytest"
alias python="poetry run python"

# Alias for running MarkFlow on our files that avoids clobbering out tests.
alias markflow-markflow='git ls-files | egrep ".md\$\$" | grep -v "tests/" | xargs poetry run markflow --check'
