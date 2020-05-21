![Master Branch Validation](https://github.com/pkuehne/grant/workflows/Master%20Branch%20Validation/badge.svg?branch=master)

# Grant - The Genealogical Research AssistaNT

Grant is a tool for genealogists to organize their research. It is based on the idea of [Research Logs](https://www.familysearch.org/wiki/en/Research_Logs), where each ancestor (or any family member really) is recorded with the sources that have been searched and the result of those searches along with any documents created.

Try try it out, head to the [Releases](https://github.com/pkuehne/grant/releases) page.

## Features

- Store your research in a YAML file - no proprietary lock-in and easy enough to read with notepad
- Divides research up into Plans each with multiple Tasks to track specific sources
- Filter Plans/Tasks by keywords, status, etc

## Coming Soon

- Link to your gedcom file to link Plans to individual/families/locations/etc
- Filter Plans/Tasks by linked individuals/families/locations/etc
- Keep track of Correspondence
- Store your research as a Note inside your gedcom file and never lose it
- Print the research logs for hard-copy storage

# Development

If you are interested in running the source code directly, here are some handy tips:

- To run the build: `python main.py`
- To run the tests: `python -m pytest tests`
- To generate the `resources.py` file: `pyrcc5 grant.qrc -o resources.py`
- To create an executable: `pyinstaller --onefile --windowed main.py`
