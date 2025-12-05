# Super Simple Stock Market

![Tests](https://github.com/TsanthoshR/Super_Simple_Stock_Market/actions/workflows/tests.yml/badge.svg)

---
A small Python project that implement phase 1 functionality of a Global Beverage Corporation Exchange (GBCE).
This repository contains models for stocks and trades, a simple market implementation (GBCE), test suites,
and a pre-commit configuration with linters and static analysis tools.
This README documents how to set up the development environment, run the application, run and write tests,
use pre-commit hooks, debug common issues, and contribute.

---

## Project overview

The project implements a tiny stock market simulation with the following responsibilities:

\- Stock models (common \& preferred) with dividend-yield and P/E ratio calculation

\- Trade recording and volume-weighted stock price calculation

\- A simple market class (GBCE) that maintains a set of stocks and computes the GBCE All Share Index (geometric mean of stock prices)

\- Unit tests that exercise the core functionality

\- Pre-commit configuration for automated checks (formatters, linters, static analysis, doc validation)

---

## Repository layout

Top-level (important files/folders):

\- `src/` - application package root. Imports in this repository are organized under `src.stockmarket.\*`.

&nbsp; - `stockmarket/` - main package implementing exchange, stock models, exceptions, and helpers

\- `tests/` - unit tests using `unittest`

\- `.pre-commit-config.yaml` - pre-commit hooks and tool configuration

\- `pyproject.toml` - configuration for black, mypy and numpydoc

\- `.flake8` - flake8 configuration

\- `requirements.txt` - runtime or development dependencies (if present)

\- `README.md` - this file

Key modules :

\- `src/stockmarket/stock/models.py` - Stock and Trade models

\- `src/stockmarket/exchange/market.py` - GBCE market and its operations

\- `tests/test_*` - unit tests

---

## Prerequisites

\- Python 3.11 (project tested on Python 3.11)

\- Git

\- Recommended: create and use a virtual environment for development

---

## Setup (Windows PowerShell example)

1\. Create and activate a virtual environment (if not already created):

```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```

2\. Upgrade pip and install dependencies (if `requirements.txt` exists):

```powershell
python -m pip install -U pip

pip install -r requirements.txt

```

4\. Install development tools manually (if not installed through requirements):

```powershell

pip install pre-commit pytest coverage mypy black isort flake8 interrogate ruff

```

5\. Install and enable pre-commit hooks (this will install hooks into `.git/hooks`):

```powershell

pre-commit install

pre-commit install --hook-type commit-msg

```

---

## Running the library and quick checks

You can experiment from Python REPL with the package installed (editable install recommended):

```powershell

py -m src.main

```

---

## Running tests

Using the installed package (recommended):

```powershell

py -m unittest discover -s tests

```

---

## Code style, linters and pre-commit hooks

This repository uses pre-commit to run several checks automatically before commits. The configured tools include (but may vary):

\- black (code formatter)

\- isort (import sorter)

\- ruff / flake8 (linting)

\- mypy (static typing)

\- numpydoc / interrogate (docstring validation \& coverage)

\- docformatter (docstring formatting)

\- conventional commit message check

Run all hooks locally against all files (useful when changing configurations):

```powershell

pre-commit run --all-files -v

```

If a hook fails, read the hook output to see exact reasons; you can run the failing tool directly for faster iteration. Example:

```powershell

black --check --config pyproject.toml .

ruff check .

flake8 --config .flake8 .

mypy ./src/

mypy ./tests/

```

---

## Documentation and docstring validation

This project uses numpydoc/interrogate to validate docstrings and measure docstring coverage.

\- To run docstring validation:

```powershell

pre-commit run numpydoc-validation --all-files -v

```

\- To measure docstring coverage (interrogate):

```powershell

interrogate --fail-under=80 --verbose

```

Add docstrings in numpydoc style (Parameters / Returns sections) for public API functions and classes.

---

## Coverage

Run tests under coverage and generate a report:

```powershell

coverage run -m unittest discover -s tests

coverage report -m

coverage html  # creates htmlcov/ index.html

```
