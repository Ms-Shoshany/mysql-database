
import re
import json
import mysql.connector
import logging

class DBConnector:
    def __init__(self, creds, database=None):
        self.creds = creds
        self.database = database

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.creds.host,
            user=self.creds.user,
            password=self.creds.password,
            database=self.database,
            port = self.creds.port,
        )
        self.cursor = self.conn.cursor()

    def create_db_if_doest_exist(self, database):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.conn.commit()

    def create_tables_if_doest_exist(self, schemas):
        with open(schemas, 'r') as f:
            tables = json.loads(f.read())
        for table_name, table_schema in tables.items():
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY"
            for key, value in table_schema.items():
                query += f", {key} {value}"
            for key in [key for key in table_schema.keys() if key.endswith("_id")]:
                    referenced_obj = re.search(r'([^_]+)_id$', key).group(1)
                    if self.check_if_table_exists(referenced_obj):
                        query += f", FOREIGN KEY ({key}) REFERENCES {referenced_obj}(id)"
            query += ");"
            self.cursor.execute(query)
            self.conn.commit()

    def check_if_table_exists(self, table):
        query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"
        self.cursor.execute(query, (self.database, table))
        result = self.cursor.fetchone()
        return result[0] > 0
    
    def get_tables_columns(self, table):
        query = f"SHOW COLUMNS FROM {table};"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results:
            results = [result[0] for result in results]
        return results
        
    def write_row(self, table, obj):
        columns = obj.keys()
        values = obj.values()
        columns_str = ", ".join(columns)
        values_str = ", ".join([f"'{v}'" if isinstance(v, str) else f"{v}" for v in values])
        insert_query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"
        self.cursor.execute(insert_query)
        self.conn.commit()
        logging.debug(f"Data inserted successfully into {table}.")
        return self.cursor.lastrowid
    
    def update_row(self, table, id, obj):
        if not obj:
            return
        query = f"UPDATE {table}"
        first = True
        for key, value in obj.items():
            if first:
                query += " SET"
            else:
                query += ", "
            first = False
            query += f" {key} = '{value}' "
        query += f" WHERE id = {id};"
        self.cursor.execute(query)
        self.conn.commit()

    def filter_table(self, table, columns, filter="", conditions={}):
        query = f"SELECT * FROM {table} WHERE "
        first = True
        for key, value in conditions.items():
            if first:
                query += " ("
                first = False
            else:
                query += "AND"
            query += f" {key} = '{value}' "
        if conditions:
            query += ") And ("
        first = True
        for column in columns:
            if first:
                first = False
            else:
                query += " OR "
            query += f"{column} LIKE '%{filter}%'"
        if conditions:
            query += ")"
        query += ";"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results:
            columns = [column[0] for column in self.cursor.description]
            results = [dict(zip(columns, result)) for result in results]
        return results
    
    def get_rows(self, table, conditions={}):
        query = f"SELECT * FROM {table}"
        first = True
        for key, value in conditions.items():
            if first:
                query += " WHERE"
            else:
                query += "AND"
            first = False
            query += f" {key} = '{value}' "
            
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results:
            columns = [column[0] for column in self.cursor.description]
            results = [dict(zip(columns, result)) for result in results]
        return results
    
    def get_row(self, table, conditions={}):
        results = self.get_rows(table, conditions)
        if results:
            return results[0]
        return None
    
    def delete_row(self, table, id):
        query = f"DELETE FROM {table} WHERE id = {id};"
        self.cursor.execute(query)
        self.conn.commit()
        return None

    def close(self):
        """Close the cursor and connection."""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()


    def __enter__(self):
        """Set up the database connection and return the object itself."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection when exiting the context."""
        self.close()
        if exc_type:
            logging.error(f"An error occurred: {exc_val}")
        return True


