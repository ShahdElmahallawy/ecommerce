# Test Commands

## Run tests

```sh
pytest
```

## Run tests in parallel

```sh
pytest -n auto
```

## Run tests and stop on first failure

```sh
pytest -x
```

## Run tests and enter PDB on first failure

```sh
pytest --pdb
```

## Run tests and generate html report

```sh
pytest -n auto --cov-report html --cov-config=.coveragerc --cov=api api/tests/
```

## Run tests and generate xml and txt report

```sh
pytest --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov-config=.coveragerc --cov=api api/tests/ | tee pytest-coverage.txt
```

> Used in Github Action to generate reports

## Check coverage

```sh
coverage report --fail-under=80
```

> Fail if coverage is less than 80%
