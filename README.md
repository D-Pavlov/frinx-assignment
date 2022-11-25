# Frinx Home Assignment

This program extracts Interface configurations from a JSON config file and persists them in a Postgres database according to the [assignment](./Python_home_assignment_2021.docx)

## Requirements:

- Python 3.9+
- Postgres 12+
- sqlachemy
- pytest

## How to run:

1. have a postgres DB running
2. configure `.env` according to `.env.example` and your DB credentials
3. install requirements (in virtualenv, of course)

   ```pip
   pip install -r requirements.txt
   ```
4. run the script

   ```
   python src/assignment.py
   ```
5. inspect the DB to see the results
6. optionally clean the DB

   ```
   python src/clean_db.py
   ```

## Limitations:

1. the program supports parsing only "Cisco-IOS-XE-native" interfaces
2. the sanity check on DB is not completely finished - works well with empty DB though
3. the program offers no solution for duplicate interface names, if the program is run multiple times - please drop the table before running again
4. the function for persisting the parsed data to DB is not covered by tests yet
