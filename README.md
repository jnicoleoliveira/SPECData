# SPECdata

## Summary
SPECdata is an interactive analysis tool that given an experiment spectrum, will
rapidly assign known species (i.e. precursors, contaminants). The software
includes many other features that allow a user to interact with their data,
accept or decline assignments, and export or save their data. Using SQLite,
this software stores both catalog, and experiment data, and provides an easy
to use GUI for database management.


## Installation
    >> cd init
    >> python setup.py build
    >> python setup.py install
    >> python init.py

## Running SPECData Application
    >> python app.py

## Common Setup Errors
######Add ProjectDirectory to PYTHONPATH
    export PYTHONPATH=$PYTHONPATH:ProjectDirectoryPath
----------------------------------------------------------
    ImportError: No module named backend_qt4agg
#####Install missing matplotlib qt4 backend
    >> sudo apt-get install python-matplotlib-qt4
##### Adjust Matplotlib Configuration
###### Get the Matplotlib config file path
    >> python
    >> import matplotlib
    >> matplotlib.matplotlib_fname()
    u'/usr/lib64/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc'
######Change the backend of the config file to qt4agg
    >> vi /usr/lib64/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc
######Change the line to :
    backend : qt4agg
[Source: StackOverflow] (http://stackoverflow.com/a/20583922)


