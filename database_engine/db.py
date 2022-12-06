from abc import ABC, abstractmethod

from table import Table


class DBInterface(ABC):
    @abstractmethod
    def create_table(self, table_name, column_list):
        pass

    @abstractmethod
    def insert_into_db(self, table_name, *args):
        pass

    @abstractmethod
    def update_row(self, table_name, pk_pos, updated_dict):
        pass
    
    def select_rows(self, table_name, where_clause_dict):
        pass

    def create_index(self, table_name, column_list):
        pass

    def drop_index(self, db, table, index_name):
        pass


class NaiveDB(DBInterface):
    def __init__(self, name):
        self.table_dict = {}
        self.name = name
    
    def __str__(self):
        return f"DB created with name {self.name}"
    
    def create_table(self, table_name, column_list):
        if table_name in self.table_dict:
            raise Exception("Table already exists")
        
        table = Table(table_name, column_list)
        self.table_dict[table_name] = table

        print(table)
    
    def insert_into_db(self, table_name, *args):
        self.table_dict[table_name].insert(*args)

        print(self.table_dict[table_name])
    
    def update_row(self, table_name, pk_pos, updated_dict):
        self.table_dict[table_name].update(pk_pos, updated_dict)

        print(self.table_dict[table_name])
    
    def select_rows(self, table_name, where_clause_dict):
        res = self.table_dict[table_name].select(where_clause_dict)
        print("---------")
        print("select query result - ", res)
        print("---------")
    
    def create_index(self, table_name, column):
        self.table_dict[table_name].create_index(column)
    
    def drop_index(self, table_name, column):
        self.table_dict[table_name].drop_index(column)


class DBManager:
    def __init__(self):
        self.db_dict = {}
        self.selected_db = None
    
    def create_db(self, db_name):
        if db_name in self.db_dict:
            raise Exception("DB already exist")

        self.db_dict[db_name] = NaiveDB(db_name)
        print(self.db_dict[db_name])
    
    def select_db(self, db_name):
        if not db_name in self.db_dict:
            raise Exception("DB not found")
            
        self.selected_db = self.db_dict[db_name]
        print(f"{self.selected_db.name} is selected...")
    
    def create_table(self, table_name, column_list):
        self.selected_db.create_table(table_name, column_list)
    
    def insert_into_db(self, table_name, *args):
        self.selected_db.insert_into_db(table_name, *args)
    
    def update_row(self, table_name, pk_pos, updated_dict):
        self.selected_db.update_row(table_name, pk_pos, updated_dict)
    
    def select_rows(self, table_name, where_clause_dict):
        self.selected_db.select_rows(table_name, where_clause_dict)
    
    def create_index(self, table_name, column):
        self.selected_db.create_index(table_name, column)
    
    def drop_index(self, table_name, column):
        self.selected_db.drop_index(table_name, column)
