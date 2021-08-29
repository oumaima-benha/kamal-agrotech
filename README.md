This is a simple product managment application writtern in Python using QT and SQLite

## Getting started

```c
//clone the repo
git clone github.com/oumaima-benha/kamal-grotech.git

//install the virtual environment
python -m venv venv

//activate the virtual environment
source venv/Scripts/activate

//install needed packages
pip install requirments.txt

//initialize the database
python initdb.py

//run the application
python main.py
```

## Re-Generate the UI code

```
pyuic5 ui.ui -o ui.py
```