# GENE - The genealogical research assistant

Gene is a tool for genealogists to organize their research. At its heart it is a todo app, like many others, but what sets Gene appart is that it is explicitly designed for genealogists. It can read and interact with gedcom files for example. Allowing you to link your research tasks to individuals, families, locations in your gedcom file. Search for all tasks associated with a particular individual and track your correspondence with archives or other researchers. Gene does all this without forcing you to adopt some proprietary file format. Each research file is stored in YAML, an easy-to-read, fully open file format. There is no lock-in with Gene.

## Features

- Stores your research in a YAML file - no proprietary lock-in and easy enough to read with notepad
- Divides research up into Plans each with multiple Tasks to track smaller items

## Coming Soon

- Filter Plans/Tasks by keywords, status, etc
- Link to your gedcom file to link Plans to individual/families/locations/etc
- Filter Plans/Tasks by linked individuals/families/locations/etc
- Keep track of Correspondence
- Store your research as a Note inside your gedcom file and never lose it

# Development

If you are interested in running the source code directly, here are some handy tips:

- To run the build: `python main.py`
- To run the tests: `python -m pytest tests`
- To generate the `resources.py` file: `pyrcc5 gene.qrc -o resources.py`
- To create an executable: `pyinstaller --onefile --windowed --name gene main.py`
