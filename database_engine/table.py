from columns import Columns
from index import Index


class Table:
    def __init__(self, name, column_list):
        self.id_seq_incrementor = 0
        self.name = name
        self.index_dict = {}
        self.data_list = []
        self.column_list = [{'type': 'int', 'name': 'id'}]
        self.columns = Columns()
        self.__create_columns(column_list)
    
    def __str__(self):
        return_val = "---------\n"
        return_val += f"{self.name} Table\n"
        for i in range(0, len(self.data_list)):
            return_val += str(self.data_list[i]) + "\n"
        return_val += "---------"

        return return_val
    
    def __create_columns(self, column_list):
        for column in column_list:
            column_type, column_name = \
                column['type'], column['name']
            if not self.columns.is_valid_column_type(column_type):
                raise TypeError("Invalid type")
            else:
                self.column_list.append({
                    'type': column_type,
                    'name': column_name
                })
    
    def __get_id_seq(self):
        self.id_seq_incrementor += 1

        return self.id_seq_incrementor
    
    def create_index(self, column):
        if column in self.index_dict:
            raise Exception("Index already exists")
        
        index = Index(self.data_list, column)
        self.index_dict[column] = index
        print(index)
    
    def drop_index(self, column):
        del self.index_dict[column]
    
    def insert(self, *args):
        row_dict = {}
        if len(args) != len(self.column_list) - 1:
            raise Exception(
                    "Number of columns do not match with the input")
        
        for i in range(0, len(args)):
            if not self.columns.is_valid_type(type(args[i])):
                raise TypeError("Invalid type")

            row_dict[self.column_list[i + 1]['name']] = args[i]
        
        row_dict['id'] = self.__get_id_seq()
        self.data_list.append(row_dict)

        # reindex
        for col_name, index in self.index_dict:
            index.reindex(
                None, row_dict[col_name], row_dict['id'])
            self.index_dict[col_name] = index
    
    def update(self, pk_pos, updated_dict):
        for col_name, col_value in updated_dict.items():
            prev_value = self.data_list[pk_pos][col_name]
            self.data_list[pk_pos][col_name] = col_value
            
            if col_name in self.index_dict:
                index = self.index_dict[col_name]
                index.reindex(prev_value, col_value, pk_pos)
    
    def select(self, where_clause_dict):
        result_set_list = []

        if not where_clause_dict:
            return self.data_list

        for col_name, col_val in where_clause_dict.items():
            positions = None
            result_set = {}
            if col_name in self.index_dict:
                positions = \
                    self.index_dict[col_name].get_row_pos(col_val)

            if positions is None:
                for i in range(0, len(data_list)):
                    if data_list[i][col_name] == col_val:
                        result_set.add(i)
            else:
                result_set = set(positions)
            
            result_set_list.append(result_set)

        if len(result_set_list) == 0:
            return []

        final_set = result_set_list[0]
        for i in range(1, len(result_set_list)):
            final_set = final_set.intersection(result_set_list[i])
        
        final_list = []
        position_list = list(final_set)
        for position in position_list:
            if position is not None:
                final_list.append(self.data_list[position])
        
        return final_list
