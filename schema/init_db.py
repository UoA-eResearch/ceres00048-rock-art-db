import schema
import sqlalchemy as sql

import os
import glob
import csv

engine = sql.create_engine('sqlite:///rockart.db')

# Create the tables in the database
schema.metadata.create_all(engine)
stmts = []

# Initialise database with data from table files
table_files = glob.glob('initial-data/*.csv')
for path in table_files:
    print('Processing table data from ',path)
    table_name = os.path.basename(path).split('.')[0]
    with open(path, newline='') as table_file:
        reader = csv.DictReader(table_file,delimiter=',',quotechar='"')
        entries = list(reader)
        table = schema.metadata.tables[table_name]
        if table is not None:
            # If the a table that corresponds with a table file exists, create an insert statement. 
            stmts.append(sql.insert(table,values=entries))


connection = engine.connect()
transaction = connection.begin()
try:
    # Add table data for each table
    for stmt in stmts:
        connection.execute(stmt)
    transaction.commit()
except:
    transaction.rollback()
    print("An error occurred while adding initial table data.")
    raise

connection.close()
