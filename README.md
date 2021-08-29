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

```c
// re-generate the UI
pyuic5 ui.ui -o ui.py

// re-run the application
python main.py
```

## Git

```c
//to check the status
git status

//to add files to change set
git add file1 file2 

//to commit locally the changes
git commit -m "mesage to track history"

//to push the changes remotly
git push
```