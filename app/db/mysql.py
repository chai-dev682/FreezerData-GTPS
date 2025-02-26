import pymysql
from app.core.config import settings
from app.schemas.freezer_data import ObjectDB, Manuals, ObjectManual

class MySQLService:
    def __init__(self):
        self.config = {
            "host": settings.DB_HOST,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "db": settings.DB_NAME,
            "port": settings.DB_PORT,
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "connect_timeout": 10,
            "read_timeout": 10,
            "write_timeout": 10
        }

    def _get_connection(self):
        return pymysql.connect(**self.config)

    def initialize(self):
        """Create the ObjectDB, Manuals, ObjectManual table if it doesn't exist"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ObjectDB (
                    id INT PRIMARY KEY,
                    object_id INT,
                    max_working_pressure_bar INT,
                    description TEXT,
                    location TEXT,
                    complex TEXT,
                    building_data TEXT,
                    servicecontract_nr TEXT,
                    sla TEXT,
                    brand TEXT,
                    model TEXT,
                    refrigerant TEXT,
                    refrigerant_filling_kg FLOAT,
                    config_file TEXT
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Manuals (
                    id INT PRIMARY KEY,
                    pdf_file_name TEXT,
                    tech_specification TEXT,
                    manual_structure TEXT
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ObjectManual (
                    id INT PRIMARY KEY,
                    object_id INT,
                    manual_id INT
                )
                """)
            connection.commit()
        finally:
            connection.close()

    def insert_object_db(self, object_db: ObjectDB):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO ObjectDB 
                        (id, object_id, max_working_pressure_bar, description, location, complex, building_data, servicecontract_nr, sla, brand, model, refrigerant, refrigerant_filling_kg, config_file)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    object_db.id,
                    object_db.object_id,
                    object_db.max_working_pressure_bar,
                    object_db.description,
                    object_db.location,
                    object_db.complex,
                    object_db.building_data,
                    object_db.servicecontract_nr,
                    object_db.sla,
                    object_db.brand,
                    object_db.model,
                    object_db.refrigerant,
                    object_db.refrigerant_filling_kg,
                    object_db.config_file
                ))
            connection.commit()
        finally:
            connection.close()

    def insert_manuals(self, manuals: Manuals):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO Manuals 
                        (id, pdf_file_name, tech_specification, manual_structure)
                        VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (
                    manuals.id,
                    manuals.pdf_file_name,
                    manuals.tech_specification,
                    manuals.manual_structure
                ))
            connection.commit()
        finally:
            connection.close()

    def insert_object_manual(self, object_manual: ObjectManual):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO ObjectManual 
                        (id, object_id, manual_id)
                        VALUES (%s, %s, %s)"""
                cursor.execute(sql, (
                    object_manual.id,
                    object_manual.object_id,
                    object_manual.manual_id
                ))
            connection.commit()
        finally:
            connection.close()

    def query(self, sql: str):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        finally:
            connection.close()

mysql_db = MySQLService()