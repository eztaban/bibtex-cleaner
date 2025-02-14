# Development

[Home](../README.md)

There is no current structure around development.  
This is a tool I have developed for my own usecase.  

## Folder Structure

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

## Future aspirations

* Publish as a flatpak

## How to run tests

Tests have been made to run with `pytest`.  

To run individual tests:

```python
pytest tests/name_of_test.py
```

To rund all tests at once:  

```python
pytest tests/
```

For additional context when tests are run:  

```
pytest tests/ -v
```
