Navigate to eeCarbonVisualization3 in VS Code, then create a virtual environment by opening a terminal and typing: 
-
py -3 -m venv .venv

Hit Ctrl+Shift+P to open the command pallete and select:
-
Python: Select Interpreter

.venv 

Hit Ctrl+Shift+` (` is the same key as ~) and activate .venv
-
Type the following into the terminal:
-
pip install -r requirements.txt

python manage.py makemigrations (If it says it detects no changes, that's fine (maybe.))

python manage.py migrate (If it says no migrations to apply, that's fine (maybe.) Check if the file db.sqlite3 was created.)


Make sure you have the KSSL sqlite file (it's called ncss_labdata.sqlite) downloaded, and put it in the same folder as manage.py.
-
Type the following into the terminal:
-
python manage.py standards

python manage.py fillDatabase "RaCA_XL, KSSL_SQL"


Press F5 and run the program! Hopefully, it should land you on a map of the United States!

AS FOR SYNONYMS:
--
Check base/SynonymBook.xlsx for more. The "Main" page is where the variables from each of the databases is associated with a Standard, the "Variable Segregation" is where we define the urls and/or tables we get data from, and "Glossary" is where Standards are defined.

