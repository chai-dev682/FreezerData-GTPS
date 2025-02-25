from typing import List
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
                # TODO: add columns
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS freezer_data (
                    id INT PRIMARY KEY,
                )
                """)
            connection.commit()
        finally:
            connection.close()

    def insert_object_db(self, object_db: ObjectDB):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                # TODO: add columns
                sql = """INSERT INTO freezer_data 
                        (id)
                        VALUES (%s)"""
                cursor.execute(sql, (
                    object_db.id
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