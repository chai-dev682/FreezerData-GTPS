import csv
from typing import BinaryIO
import chardet
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.mysql import mysql_db
from app.schemas.freezer_data import ObjectDB, Manuals, ObjectManual

def process_csv(file: BinaryIO, db_name: str):
    # Detect encoding
    raw_data = file.read()
    file.seek(0)  # Reset file pointer
    encoding = chardet.detect(raw_data)['encoding']

    # Read CSV
    csv_data = csv.reader(file.read().decode(encoding).splitlines())
    next(csv_data)  # Skip header

    if db_name == "object_db":
        for row in csv_data:
            obj = ObjectDB(
                id=int(row[0]),
                object_id=int(row[1]),
                max_working_pressure_bar=int(row[2]),
                description=row[3],
                location=row[4],
                complex=row[5],
                building_data=row[6],
                servicecontract_nr=row[7],
                sla=row[8],
                brand=row[9],
                model=row[10],
                refrigerant=row[11],
                refrigerant_filling_kg=float(row[12]),
                config_file=row[13]
            )
            
            mysql_db.insert_object_db(obj)
    elif db_name == "manuals":
        for row in csv_data:
            manual = Manuals(
                id=int(row[0]),
                pdf_file_name=row[1],
                # tech_specification=row[2],
                # manual_structure=row[3]
            )
            
            mysql_db.insert_manuals(manual)
    elif db_name == "object_manual":
        for row in csv_data:
            obj_manual = ObjectManual(
                id=int(row[0]),
                object_id=int(row[1]),
                manual_id=int(row[2]),
            )
            
            mysql_db.insert_object_manual(obj_manual)

if __name__ == "__main__":
    mysql_db.initialize()
    process_csv(open("dataset/ObjectDB.csv", "rb"), "object_db")
    process_csv(open("dataset/Manuals.csv", "rb"), "manuals")
    process_csv(open("dataset/ObjectID_manual.csv", "rb"), "object_manual")
