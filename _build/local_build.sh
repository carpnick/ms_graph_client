#!/bin/zsh
set -e

echo "Installing files"
poetry install --no-interaction

echo "Running Stub file checks: stubtest cf_extension_core"
# Helpful to generate original stub files - stubgen src/ -o src/  --include-private
# This wont work until after you placed py.typed into your package directory
stubtest ms_graph_client

echo "Running mypy: mypy src/ tests/ --strict"
mypy src/ tests/ --strict

echo "\nRunning Unit Tests: pytest --cov --cov-report html --cov-report xml --log-cli-level=DEBUG --junit-xml=junit.xml tests/unit"
pytest --cov --cov-report html --cov-report xml --log-cli-level=DEBUG --junit-xml=junit.xml tests/unit

#Moved this later for dev since I care less about formatting and more about functionality
echo "\nRunning black: black src/ tests/ -l 120 --check --extend-exclude \".*.pyi\""
black src/ tests/ -l 120 --check --extend-exclude ".*.pyi"

echo "\nRunning flake8: flake8 --max-line-length 120 src/ tests/"
flake8 --max-line-length 120 src/ tests/


echo "\n Running poetry build: poetry build"
poetry build

echo "\n\nBuild completed successfully"