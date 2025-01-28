# How does it work

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

- [How does it work](#how-does-it-work)
  - [1. Finding entries in the bib file](#1-finding-entries-in-the-bib-file)
    - [1. The Regex pattern](#1-the-regex-pattern)
      - [Example Matches](#example-matches)
    - [2. Finding citations in the tex file](#2-finding-citations-in-the-tex-file)
      - [1. **Regex Pattern**](#1-regex-pattern)
        - [Example](#example)
      - [2. **Finding Matches**](#2-finding-matches)
        - [Example](#example-1)
      - [3. **Flattening and Splitting by Commas**](#3-flattening-and-splitting-by-commas)
        - [Example](#example-2)
      - [4. **Removing Duplicates**](#4-removing-duplicates)
        - [Example](#example-3)
    - [**Example Input and Output**](#example-input-and-output)
      - [Input](#input)
      - [Output](#output)

## 1. Finding entries in the bib file

### 1. The Regex pattern

This pattern is used to match the start of a BibTeX entry and capture key parts of it. Here's the breakdown:  

>`@(\w+)\{([^,]+),`  

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

#### Example Matches

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

##### Example

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
  
##### Example

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

##### Example

For `matches = ['smith2023', 'doe2022', 'smith2023, johnson2021']`, this produces:

```python
['smith2023', 'doe2022', 'smith2023', 'johnson2021']
```

---

#### 4. **Removing Duplicates**

- **Purpose**:
  - Converts the list to a `set` to automatically remove duplicate citation IDs.
  - Converts the `set` back to a list.

##### Example

For `flattened_matches = ['smith2023', 'doe2022', 'smith2023', 'johnson2021']`, this produces:

```python
['doe2022', 'johnson2021', 'smith2023']
```

### **Example Input and Output**

#### Input

```latex
This is a reference \cite{smith2023} and \cite{doe2022}.
Additionally, we cite multiple sources \cite{johnson2021, williams2020}.
To further elaborate, we also use \cite{smith2023, doe2022} again.
```

#### Output

```python
['doe2022', 'johnson2021', 'smith2023', 'williams2020']
```
