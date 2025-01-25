# LaTeX Citation Cleaner API Reference

## Overview

The LaTeX Citation Cleaner is a Python tool designed to process `.tex` and `.bib` files for cleaning and managing LaTeX citations. The tool supports both folder-based and zip-based workflows and provides utilities for analyzing and exporting citation data.

[Main Readme](README.md)  
[Main Notebook](main.ipynb)

- [LaTeX Citation Cleaner API Reference](#latex-citation-cleaner-api-reference)
  - [Overview](#overview)
  - [Classes](#classes)
    - [`LatexCitationCleaner`](#latexcitationcleaner)
      - [Attributes](#attributes)
      - [Methods](#methods)
        - [`specific_files(dot_bib_location: str, dot_tex_location: Union[List[str], str])`](#specific_filesdot_bib_location-str-dot_tex_location-unionliststr-str)
        - [`specific_files_in_zip(zip: str, dot_bib_location: str, dot_tex_location: Union[List[str], str])`](#specific_files_in_zipzip-str-dot_bib_location-str-dot_tex_location-unionliststr-str)
        - [`all_tex_in_folder(folder: str, bib_file: str = None)`](#all_tex_in_folderfolder-str-bib_file-str--none)
        - [`all_tex_in_zip(zip: str, bib_file: str = None)`](#all_tex_in_zipzip-str-bib_file-str--none)
        - [`load()`](#load)
        - [`analyze()`](#analyze)
        - [`to_excel(filename: str = None) -> pd.DataFrame`](#to_excelfilename-str--none---pddataframe)
        - [`make_clean_bib(bib_name: str = None)`](#make_clean_bibbib_name-str--none)
        - [`read_tex_file(filepath: str) -> str`](#read_tex_filefilepath-str---str)
        - [`read_bib_file(filepath: str) -> str`](#read_bib_filefilepath-str---str)
        - [`find_unique_citation_keys(stringline: str) -> List[str]`](#find_unique_citation_keysstringline-str---liststr)
        - [`find_unique_cites(stringline: str) -> List[str]`](#find_unique_citesstringline-str---liststr)
        - [`export_citations_to_excel(all_references: List[str], used_citations: List[str], filename: str = "citations_report.xlsx") -> pd.DataFrame`](#export_citations_to_excelall_references-liststr-used_citations-liststr-filename-str--citations_reportxlsx---pddataframe)
        - [`filter_bib_entries(bib_content: str, used_citations: list, output_filename: str = "filtered_biblio.bib")`](#filter_bib_entriesbib_content-str-used_citations-list-output_filename-str--filtered_bibliobib)
        - [`get_tex_files_in_folder() -> List[str]`](#get_tex_files_in_folder---liststr)
        - [`get_biblio_in_folder() -> str`](#get_biblio_in_folder---str)
        - [`unpack_zip(zip_file: str, target_folder: str = "tmp") -> str`](#unpack_zipzip_file-str-target_folder-str--tmp---str)
        - [`clear_folder(folder: str)`](#clear_folderfolder-str)
    - [`CLILatexCitationCleaner`](#clilatexcitationcleaner)
      - [Methods](#methods-1)
        - [`autorun()`](#autorun)
        - [`process_all_tex_in_folder(folder: str)`](#process_all_tex_in_folderfolder-str)
        - [`process_all_tex_in_zip(zip_file: str)`](#process_all_tex_in_zipzip_file-str)
        - [`process_specific_tex_in_folder(tex_files: List[str], bib_file: str, folder: str)`](#process_specific_tex_in_foldertex_files-liststr-bib_file-str-folder-str)
        - [`process_specific_tex_in_zip(tex_files: List[str], bib_file: str, zip_file: str)`](#process_specific_tex_in_ziptex_files-liststr-bib_file-str-zip_file-str)


---

## Classes

### `LatexCitationCleaner`

This is the base class that provides core functionality for processing `.tex` and `.bib` files.  
This version of the tool is the base and the one the notebook interacts with.  

#### Attributes
- `tex_locations`: List of paths to `.tex` files to process.
- `bib_locations`: Path to the `.bib` file.
- `tex_content`: List of contents of `.tex` files.
- `bib_content`: Content of the `.bib` file.
- `cites`: List of citation IDs found in `.tex` files.
- `cite_keys`: List of citation keys found in the `.bib` file.
- `folder`: Path to the folder being processed.

#### Methods

##### `specific_files(dot_bib_location: str, dot_tex_location: Union[List[str], str])`
Loads specific `.tex` and `.bib` file paths to analyze.

- **Arguments**:
  - `dot_bib_location`: Path to the `.bib` file.
  - `dot_tex_location`: Path(s) to the `.tex` file(s).

---

##### `specific_files_in_zip(zip: str, dot_bib_location: str, dot_tex_location: Union[List[str], str])`
Unpacks a zip file and loads specific `.tex` and `.bib` files for analysis.

- **Arguments**:
  - `zip`: Path to the zip file.
  - `dot_bib_location`: Path to the `.bib` file inside the zip.
  - `dot_tex_location`: Path(s) to `.tex` files inside the zip.

---

##### `all_tex_in_folder(folder: str, bib_file: str = None)`
Loads all `.tex` files in the specified folder. If no `.bib` file is specified, the tool automatically detects one.

- **Arguments**:
  - `folder`: Path to the folder containing the `.tex` files.
  - `bib_file`: Optional path to a `.bib` file.

---

##### `all_tex_in_zip(zip: str, bib_file: str = None)`
Unpacks a zip file and processes all `.tex` files inside it. Optionally detects a `.bib` file.

- **Arguments**:
  - `zip`: Path to the zip file.
  - `bib_file`: Optional path to a `.bib` file inside the zip.

---

##### `load()`
Loads the content of all `.tex` files and the `.bib` file specified.

---

##### `analyze()`
Analyzes citations:
- Extracts unique citations from `.tex` files.
- Extracts unique keys from the `.bib` file.

---

##### `to_excel(filename: str = None) -> pd.DataFrame`
Exports an overview of unused and used citations to an Excel file and returns the same as a Pandas DataFrame.

- **Arguments**:
  - `filename`: Optional filename for the Excel file.

- **Returns**: Pandas DataFrame containing used and unused citations.

---

##### `make_clean_bib(bib_name: str = None)`
Creates a new `.bib` file containing only citations used in the `.tex` files.

- **Arguments**:
  - `bib_name`: Optional name for the new `.bib` file.

---

##### `read_tex_file(filepath: str) -> str`
Reads and returns the content of a `.tex` file.

---

##### `read_bib_file(filepath: str) -> str`
Reads and returns the content of a `.bib` file.

---

##### `find_unique_citation_keys(stringline: str) -> List[str]`
Finds unique citation keys in the provided `.bib` content.

- **Arguments**:
  - `stringline`: Content of the `.bib` file.

- **Returns**: List of unique citation keys.

---

##### `find_unique_cites(stringline: str) -> List[str]`
Finds unique citations in the provided `.tex` content.

- **Arguments**:
  - `stringline`: Content of the `.tex` file.

- **Returns**: List of unique citations.

---

##### `export_citations_to_excel(all_references: List[str], used_citations: List[str], filename: str = "citations_report.xlsx") -> pd.DataFrame`
Creates and exports an Excel file summarizing used and unused citations.

- **Arguments**:
  - `all_references`: List of all citation keys in the `.bib` file.
  - `used_citations`: List of citation IDs found in `.tex` files.
  - `filename`: Name of the output Excel file.

- **Returns**: Pandas DataFrame summarizing the citations.

---

##### `filter_bib_entries(bib_content: str, used_citations: list, output_filename: str = "filtered_biblio.bib")`
Filters unused citations from the `.bib` file and saves a cleaned `.bib` file.

- **Arguments**:
  - `bib_content`: Content of the `.bib` file.
  - `used_citations`: List of citation IDs used in `.tex` files.
  - `output_filename`: Name of the cleaned `.bib` file.

---

##### `get_tex_files_in_folder() -> List[str]`
Finds and returns all `.tex` files in the specified folder.

---

##### `get_biblio_in_folder() -> str`
Finds and returns the single `.bib` file in the specified folder.

---

##### `unpack_zip(zip_file: str, target_folder: str = "tmp") -> str`
Unpacks a zip file into the specified folder and returns the folder path.

- **Arguments**:
  - `zip_file`: Path to the zip file.
  - `target_folder`: Folder to unpack the contents.

---

##### `clear_folder(folder: str)`
Deletes the contents of a folder without removing the folder itself.

---

### `CLILatexCitationCleaner`

A CLI-specific implementation of `LatexCitationCleaner` with convenience methods for handling CLI arguments and workflows.

#### Methods

##### `autorun()`
Automatically runs the full pipeline: loading, analyzing, exporting, and cleaning.

---

##### `process_all_tex_in_folder(folder: str)`
Processes all `.tex` files in a folder.

---

##### `process_all_tex_in_zip(zip_file: str)`
Processes all `.tex` files in a zip file.

---

##### `process_specific_tex_in_folder(tex_files: List[str], bib_file: str, folder: str)`
Processes specific `.tex` files with a `.bib` file in a folder.

---

##### `process_specific_tex_in_zip(tex_files: List[str], bib_file: str, zip_file: str)`
Processes specific `.tex` files with a `.bib` file in a zip file.
