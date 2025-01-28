![bibClean](logo/logo_text_alternate.png)

# bibClean - a LaTeX Citation Cleaner

`bibClean` is a tool designed to help clean `.bib` files for LaTeX projects based on the citations used in the `.tex` files.   
The tool will provide a clean `.bib`file as well as summary file with an overview of unused and used citations.  
The tool expects a single `.bib` file, but can read all `.tex` files in the project. If only some `.tex`files should be considered, these can be specified.

This document describes the CLI option, but the tool can also be used from a [notebook](main.ipynb).

## Additional documentation

[API documentation.](doc/API.md)  
[Development](doc/development.md)  
[How does the tool work?](doc/how_does_it_work.md)  

## Table of contents

- [bibClean - a LaTeX Citation Cleaner](#bibclean---a-latex-citation-cleaner)
  - [Additional documentation](#additional-documentation)
  - [Table of contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command-Line Arguments](#command-line-arguments)
    - [Examples](#examples)
      - [1. Process All `.tex` Files in a Folder](#1-process-all-tex-files-in-a-folder)
      - [2. Process All `.tex` Files in a Zip File](#2-process-all-tex-files-in-a-zip-file)
      - [3. Process Specific `.tex` Files with a `.bib` File (Folder-Based)](#3-process-specific-tex-files-with-a-bib-file-folder-based)
      - [4. Process Specific `.tex` Files with a `.bib` File (Zip-Based)](#4-process-specific-tex-files-with-a-bib-file-zip-based)
    - [Notes](#notes)
  - [License](#license)

---

## Features

- Process **all `.tex` files** in a folder or zip archive.
- Process **specific `.tex` files** with a given `.bib` file.
- Support for both folder-based and zip-based input.
- Temporary unpacking for zip files.
- Automatically assumes `--all_tex` when only `--folder` or `--zip` is specified.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/eztaban/bibtex-cleaner.git
   cd bibtex-cleaner
   ```

2. Install required dependencies:

    > Drop the `--name`-flag to inherit the environment name from the yaml file  
    Get miniconda: [Miniconda](https://docs.anaconda.com/miniconda/install/)

    ```bash
    conda env create -f environment_linux.yaml --name NEW_ENV_NAME
    ``` 

    ```bash
    conda env create -f environment_windows.yaml --name NEW_ENV_NAME
    ```

    - pandas
    - openpyxl
    - python 3.10
    - ipykernel (for jupyter notebook interface)

---

## Usage

- Create folder called `input` at same level as `main.py`
- Place folder or zip-file with latex project in folder `input`
- Run the CLI tool using Python's `main.py`:

```bash
python main.py [OPTIONS]
```

Alternately, use the [notebook](main.ipynb)

### Command-Line Arguments

| Flag          | Description                                                                                   | Required?         |
|---------------|-----------------------------------------------------------------------------------------------|-------------------|
| `--all_tex`   | Process all `.tex` files in the specified location (folder or zip). If `--folder` or `--zip` is specified without `--all_tex`, this is assumed to be true.                           | Optional          |
| `--spec_tex`  | Process specific `.tex` files. Provide a space-separated list of filenames.                   | Optional          |
| `--bib`       | Path to the `.bib` file to be used (required with `--spec_tex`).                              | Optional          |
| `--folder`    | Path to the folder containing `.tex` files (and optionally a `.bib` file).                    | Required (or `--zip`) |
| `--zip`       | Path to the zip file containing `.tex` files (and optionally a `.bib` file).                  | Required (or `--folder`) |

---

### Examples

#### 1. Process All `.tex` Files in a Folder

If only the `--folder` argument is provided, the program assumes `--all_tex`:

```bash
python main.py --folder /path/to/folder
```

Equivalent to:

```bash
python main.py --all_tex --folder /path/to/folder
```

#### 2. Process All `.tex` Files in a Zip File

If only the `--zip` argument is provided, the program assumes `--all_tex`:

```bash
python main.py --zip example.zip
```

Equivalent to:

```bash
python main.py --all_tex --zip example.zip
```

#### 3. Process Specific `.tex` Files with a `.bib` File (Folder-Based)

Process specific `.tex` files `file1.tex` and `file2.tex` with `references.bib` in the folder `/path/to/folder`:

```bash
python main.py --spec_tex file1.tex file2.tex --bib references.bib --folder /path/to/folder
```

#### 4. Process Specific `.tex` Files with a `.bib` File (Zip-Based)

Process specific `.tex` files `file1.tex` and `file2.tex` with `references.bib` in the zip file `example.zip`:

```bash
python main.py --spec_tex file1.tex file2.tex --bib references.bib --zip example.zip
```

---

### Notes

- **Automatic `--all_tex`**: 
  If you provide only `--folder` or `--zip`, the tool will automatically assume `--all_tex` and process all `.tex` files in the specified location.

- **Temporary Folder for Zip Files**: 
  If you provide a zip file, the tool unpacks it into a temporary directory. Ensure you have enough space for unpacking.

- **Error Handling**:
  - If you specify `--spec_tex`, you must also provide `--bib`.
  - Either `--folder` or `--zip` must be specified to locate input files.
  - The tool validates the input to ensure no conflicts.

---

## License

This project is licensed under the MIT License.
