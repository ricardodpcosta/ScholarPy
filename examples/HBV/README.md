# Thomas Hughes example

This folder contains example scripts demonstrating the **ScholarPy** workflow. These examples assume that **ScholarPy** is installed via **pip** and is accessible either as CLI commands (Bash script) or as a Python module (Python script).

---

## Contents

| File         | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `links.txt`  | A TXT file containing an ORCID link (possibly more).            |
| `example.sh` | Bash script demonstrating ScholarPy using CLI commands.         |
| `example.py` | Python script demonstrating ScholarPy using the Python package. |

---

## Usage

### 1. Bash script

Run the workflow directly from the terminal:

```bash
bash example.sh
```

### 2. Python script

Run the workflow programmatically using Python:

```bash
python example.py
```

---

## Customisation

* Replace the link in `links.txt` with your own public scholarly CV link.
* Adjust the remaining function/command arguments in the scripts as necessary.
* Both scripts are configured to save the output files in the current folder.
