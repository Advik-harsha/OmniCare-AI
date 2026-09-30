# OmniCare AI — Continuous Integration & Automated Quality Gates
### Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026

OmniCare AI includes an automated verification pipeline designed for both local developer execution and GitHub Actions CI.

## 1. Local Automated Execution
Run the complete suite across all 10 quality gates from any terminal:
```powershell
# Master Quality Gates Runner
python verify_all.py

# 35-Gate API & Negative Testing Suite
python backend/test_endpoints.py
```

## 2. GitHub Actions Workflow Configuration
To enable GitHub Actions in your repository, place the following workflow configuration in `.github/workflows/ci.yml`:

```yaml
name: OmniCare AI Continuous Integration & Quality Gates

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  quality-gates:
    name: OmniCare AI Quality & Verification Gates
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ ubuntu-latest, windows-latest ]
        python-version: [ "3.10", "3.11" ]

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Gate 1 — Python Bytecode Compilation
      run: |
        python -m compileall backend

    - name: Gate 2 — 35-Gate Backend API Endpoint & Negative Verification
      run: |
        python backend/test_endpoints.py

    - name: Gate 3 — Master Quality Gate Suite (All 10 Verification Pillars)
      run: |
        python verify_all.py
```

> **Note on GitHub Tokens:** Pushing files to `.github/workflows/` requires a Personal Access Token with the `workflow` permission enabled in GitHub Developer Settings.
