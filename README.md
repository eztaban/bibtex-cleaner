# LaTeX Citation Cleaner

`LaTeX Citation Cleaner` is a tool designed to help clean `.bib` files for LaTeX projects based on the citations used in the `.tex` files.   
The tool will provide a clean `.bib`file as well as an excel file with an overview of unused and used citations.  
The tool expects a single `.bib` file, but can read all `.tex` files in the project. If only some `.tex`files should be considered, these can be specified.

This document describes the CLI option, but the tool can also be used from a [notebook](main.ipynb)

[API documentation.](doc.md)

- [LaTeX Citation Cleaner](#latex-citation-cleaner)
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
  - [Development](#development)
    - [Folder Structure](#folder-structure)
  - [How does it work](#how-does-it-work)
    - [1. Finding entries in the bib file](#1-finding-entries-in-the-bib-file)
      - [1. `r'@(\w+)\{([^,]+),'`](#1-rw)
        - [Full Regex: `@(\w+)\{([^,]+),`](#full-regex-w)
        - [Example Matches:](#example-matches)
    - [2. Finding citations in the tex file](#2-finding-citations-in-the-tex-file)
      - [1. **Regex Pattern**](#1-regex-pattern)
      - [Example:](#example)
      - [2. **Finding Matches**](#2-finding-matches)
      - [Example:](#example-1)
      - [3. **Flattening and Splitting by Commas**](#3-flattening-and-splitting-by-commas)
      - [Example:](#example-2)
      - [4. **Removing Duplicates**](#4-removing-duplicates)
      - [Example:](#example-3)
    - [**Example Input and Output**](#example-input-and-output)
      - [Input:](#input)
      - [Output:](#output)
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

Place folder or zip-file with latex project in folder `input`

Run the CLI tool using Python's `main.py`:

```bash
python main.py [OPTIONS]
```

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

## Development

### Folder Structure

```
project/
├── main.py                 # Entry point for the CLI
├── main.ipynb              # Notebook with same functionality
├── cleanup.py              # CLI cleanup option
├── src/
│   ├── latex_citation_tool.py  # Core functionality
│   ├── argparser.py            # Argument handling
|   ├── cleanup.py              # Clear folders
├── README.md               # Documentation
├── environment_linux.yml   # Dependencies for linux
├── environment_windows.yml # Dependencies for windows
```

## How does it work

The tool relies on regex to find entries in the .bib file and the accompanying citations in the .tex files.  
These entries are compared and unused as well as used entries are identified enabling the creation of a new .bib file with only used citations and a "summary-report" in excel to see which citations were used or unused for manual validation if needed.

The tool expects entries in the .bib file to follow the following pattern:


```bibtex
@publication_type{ID,
  field_A = {Value_A},
  field_B = {Value B},
  ...
}
```

And citations in the .tex file to use the following pattern:
```latex
\cite{ID}, \cite{ID_A, ID_B, ... ID_N}
```

### 1. Finding entries in the bib file

#### 1. `r'@(\w+)\{([^,]+),'`

This pattern is used to match the start of a BibTeX entry and capture key parts of it. Here's the breakdown:

##### Full Regex: `@(\w+)\{([^,]+),`
- **`@`**:
  - Matches the literal `@` character, which marks the start of a BibTeX entry.

- **`(\w+)`**:
  - Captures one or more word characters (letters, digits, or underscores).
  - This typically matches the entry type in BibTeX, such as `article`, `book`, or `misc`.

- **`\{`**:
  - Matches the literal `{` character that begins the entry's content.

- **`([^,]+)`**:
  - Captures one or more characters that are **not a comma**.
  - This is the citation key of the entry, which uniquely identifies it.

- **`,`**:
  - Matches the literal `,` character that separates the citation key from the rest of the entry content.

##### Example Matches:
Given the BibTeX entry:
```bibtex
@article{smith2023,
  author = {John Smith},
  title = {A Great Paper},
}
```

- `@article` matches the entry type (`article`).
- `smith2023` matches the citation key.

### 2. Finding citations in the tex file


#### 1. **Regex Pattern**
```python
pattern = r"\\cite\{([^}]+)\}"
```

- **`\\cite`**:
  - Matches the literal `\cite` command.
  - The double backslash `\\` escapes the backslash, which is a special character in regex.
  
- **`\{`**:
  - Matches the literal `{` that starts the citation block.

- **`([^}]+)`**:
  - Captures one or more characters that are **not** a closing brace `}`.
  - This matches the contents inside `\cite{...}`.

- **`\}`**:
  - Matches the closing brace `}`.

#### Example:
Given `\cite{smith2023, doe2022}`, the regex captures:
```python
'smith2023, doe2022'
```

---

#### 2. **Finding Matches**
```python
matches = re.findall(pattern, stringline)
```

- **`re.findall`**:
  - Finds all non-overlapping matches of the regex in the input string (`stringline`).
  - Returns a list of matched strings.
  
#### Example:
For the input string:
```latex
\cite{smith2023} \cite{doe2022} \cite{smith2023, johnson2021}
```

The result of `matches` is:
```python
['smith2023', 'doe2022', 'smith2023, johnson2021']
```

---

#### 3. **Flattening and Splitting by Commas**

- **Purpose**:
  - Handles cases where multiple citation IDs are provided in a single `\cite` (e.g., `\cite{smith2023, johnson2021}`).
  - Splits each match on commas and removes any surrounding whitespace using `strip()`.

#### Example:
For `matches = ['smith2023', 'doe2022', 'smith2023, johnson2021']`, this produces:
```python
['smith2023', 'doe2022', 'smith2023', 'johnson2021']
```

---

#### 4. **Removing Duplicates**

- **Purpose**:
  - Converts the list to a `set` to automatically remove duplicate citation IDs.
  - Converts the `set` back to a list.

#### Example:
For `flattened_matches = ['smith2023', 'doe2022', 'smith2023', 'johnson2021']`, this produces:
```python
['doe2022', 'johnson2021', 'smith2023']
```


### **Example Input and Output**

#### Input:
```latex
This is a reference \cite{smith2023} and \cite{doe2022}.
Additionally, we cite multiple sources \cite{johnson2021, williams2020}.
To further elaborate, we also use \cite{smith2023, doe2022} again.
```

#### Output:
```python
['doe2022', 'johnson2021', 'smith2023', 'williams2020']
```


## License

This project is licensed under the MIT License.

---

Feel free to adapt further if needed! Let me know if you have additional requirements.