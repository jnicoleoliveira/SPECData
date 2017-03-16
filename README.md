# SPECdata

## Summary
SPECdata is an interactive analysis tool that given an experiment spectrum, will
rapidly assign known species (i.e. precursors, contaminants). The software
includes many other features that allow a user to interact with their data,
accept or decline assignments, and export or save their data. Using SQLite,
this software stores both catalog, and experiment data, and provides an easy
to use GUI for database management.


## Requirements
* Python 2.7
* PyQT4
* sqlite3

## Installation
    >> export PYTHONPATH=$PYTHONPATH:ProjectDirectoryPath
    >> cd init
    >> python setup.py build
    >> python setup.py install
    >> python init.py
    
## Running SPECData Application
    >> python app.py
    
![alt text](https://zenodo.org/badge/62144661.svg " DOI ")

