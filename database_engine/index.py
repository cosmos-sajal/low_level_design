class Index:
    def __init__(self, data_list, column):
        self.index_name = None
        self.index_dict = {}
        self.column = column
        self.create_index(data_list)
    
    def __str__(self):
        return_val = "---------\n"
        return_val += "Index structure - " + str(self.index_dict)
        return_val += "\n---------"

        return return_val
    
    def __add_to_index(self, value, data_offset):
        if value in self.index_dict:
            self.index_dict[value].append(data_offset)
        else:
            self.index_dict[value] = [data_offset]
    
    def create_index(self, data_list):
        for i in range(0, len(data_list)):
            value = data_list[i][self.column]
            self.__add_to_index(value, i)

    def reindex(self, prev_data_val, new_data_val, position):
        # this implies insertion of data
        if prev_data_val is None:
            self.__add_to_index(new_data_val, position)

            return
        
        position_list = self.index_dict[prev_data_val]
        for i in range(0, len(position_list)):
            if position_list[i] == position:
                self.index_dict[prev_data_val][i] = None
                break

        if new_data_val in self.index_dict:
            self.index_dict[new_data_val].append(position)
        else:
            self.index_dict[new_data_val] = [position]
        
        print(self)
    
    def get_row_pos(self, value):
        if value in self.index_dict:
            return self.index_dict[value]
        else:
            return None
