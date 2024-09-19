from database import Database
from constants import CLEANED_DATA_PATH, DATABASE_PATH

def ingest_csv_data_to_duckdb():
    """Ingest cleaned CSV data into DuckDB database"""
    # This part of the code creates a mapping to replace special characters (å, ä, ö) in filenames with standard characters (a, o). 
    # This ensures that filenames are compatible with the database schema and table names.
    translation_table = str.maketrans({"å": "a", "ä": "a", "ö": "o"})

    # Iterate over each directory in CLEANED_DATA_PATH
    for directory_path in CLEANED_DATA_PATH.glob("*"):
        # Generate schema name from directory name with special characters replaced
        schema_name = directory_path.name.lower().translate(translation_table)
        
        # Iterate over each CSV file in the directory
        for csv_path in directory_path.glob("*"):
            # Generate table name from CSV file name with special characters replaced
            table_name = csv_path.name.lower().split(".")[0].translate(translation_table)

            # Connect to the database and execute queries
            with Database(DATABASE_PATH) as db:
                # Create schema if it does not exist
                db.query(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
                # Create table if it does not exist and populate it with data from CSV file
                db.query(
                    f"""
                        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} AS
                        SELECT * FROM read_csv_auto('{csv_path}');
                        """
                )

if __name__ == '__main__':
    
    ingest_csv_data_to_duckdb()

# When I ran the code, it imported cleaned CSV files into a DuckDB database. 
# The script replaced Swedish special characters in filenames with standard letters to ensure compatibility.
# It created schemas and tables in the database based on directory and file names and loaded the CSV data into these tables.
# Python also generated a __pycache__ directory with compiled bytecode files