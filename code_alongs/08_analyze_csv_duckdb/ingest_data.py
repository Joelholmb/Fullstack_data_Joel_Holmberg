import duckdb
from pathlib import Path

path_db = Path(__file__).parent/"social_media.db"
path_csv = Path(__file__).parent/"social_media_yt.csv"

with duckdb.connect(path_db) as db:
    q = db.execute(f"""
        CREATE TABLE youtube AS (
SELECT 
    *
FROM  
    read_csv_auto('{path_csv}'));
    """).fetchall()

    print(q)