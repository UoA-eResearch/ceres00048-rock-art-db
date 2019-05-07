# Script for creating the schema
The init_db.py script in this directory can be used to create the rock art schema in a local or remote database, and populate it with initial data.

To run the script:
1. Clone this repository:

   `git clone https://github.com/UoA-eResearch/ceres00048-rock-art-db`
2. Install the Python dependencies required to run the script. 

   `pip3 install -r requirements.txt`
3. Run the script:

   ```
   cd schema/
   python3 init_db.py
   ```
   
By default, the script generates a local SQLite database in `schema/rockart.db`. It can generate schema in other SQL dialects, such as Microsoft SQL Server. You can modify line 8 in `init_db.py` by referring to https://docs.sqlalchemy.org/en/13/core/engines.html#microsoft-sql-server.
