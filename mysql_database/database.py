import os
import json

from .db_connector import DBConnector

class DatabaseCreds:
    def __init__(self, host, user, password, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.port = port


class Database:
    def __init__(self, name, creds, schemas_path="schemas"):
        self.name = name
        self.schemas = os.path.join(f"{schemas_path}", f"{name}.json")
        self.creds = creds
        self.init()

    def init(self):
        with DBConnector(self.creds) as db:
            db.create_db_if_doest_exist(self.name)
        with DBConnector(self.creds, self.name) as db:
            db.create_tables_if_doest_exist(self.schemas)

    def add_object(self, tabl_name, data):
        with DBConnector(self.creds, self.name) as db:
            id = db.write_row(tabl_name, data)
            return id

    def get_list_of_objects(self, tabl_name, conditions={}, as_dict=False):
        objs = []
        with DBConnector(self.creds, self.name) as db:
            rows = db.get_rows(tabl_name, conditions)
        if as_dict:
            return rows
        command_str = self.create_class(tabl_name)
        for row in rows:
            exec(f"{command_str}\nobjs.append({tabl_name.title()}(row))")
        return objs
    
    def get_filtered_list_of_objects(self, tabl_name, filter="", include_columns=[], exclude_columns=[], conditions={}, as_dict=False):
        objs = []
        with DBConnector(self.creds, self.name) as db:
            if include_columns:
                columns = include_columns
            else:
                columns = db.get_tables_columns(tabl_name)
                exclude_columns.append("id")
                for column in exclude_columns:
                    if column in columns:
                        columns.remove(column)
            rows = db.filter_table(tabl_name, columns, filter, conditions)
        if as_dict:
            return rows
        command_str = self.create_class(tabl_name)
        for row in rows:
            exec(f"{command_str}\nobjs.append({tabl_name.title()}(row))")
        return objs

    def get_object_by_id(self, tabl_name, id, as_dict=False):
        with DBConnector(self.creds, self.name) as db:
            row = db.get_row(tabl_name, {"id": id})
        if as_dict:
            return row
        if row:
            return self.get_class(tabl_name, row)
        return row
    
    def update_object(self, tabl_name, id, data):
        with DBConnector(self.creds, self.name) as db:
            row = db.update_row(tabl_name, id, data)

    def delete_object(self, tabl_name, id):
        with DBConnector(self.creds, self.name) as db:
            row = db.delete_row(tabl_name, id)


    def create_class(self, class_name):
        class_name = class_name
        command_str = f"class {class_name}:\n\t"
        command_str += f"def __init__(self, data):\n\t\t"
        with open(f"{self.schemas}", 'r') as f:
            object_schema = json.loads(f.read())[class_name]
        command_str += f"self.id = data[\"id\"]\n\t\t"
        for attr in object_schema.keys():
            command_str += f"self.{attr} = data[\"{attr}\"] if \"{attr}\" in data else None\n\t\t"
        return command_str
        

    def get_class(self, class_name, data):
        obj = []
        command_str = self.create_class(class_name)
        exec(f"{command_str}\nobj.append({class_name}(data))")
        return obj[0]
    