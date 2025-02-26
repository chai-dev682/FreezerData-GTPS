import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.mysql import mysql_db
from app.db.vectordb import vector_db

if __name__ == "__main__":
    manuals = mysql_db.query(f"SELECT id, pdf_file_name FROM Manuals")
    for manual in manuals:
        print(manual)
        vector_db.upsert_manual(manual)