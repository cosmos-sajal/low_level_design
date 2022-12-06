class Columns:
    def __init__(self):
        self.valid_columns = {
            'int': {
                'type': int
            },
            'str': {
                'type': str
            }
        }
    
    def is_valid_column_type(self, column_type_name):
        return column_type_name in self.valid_columns
    
    def is_valid_type(self, type_passed):
        for key, value in self.valid_columns.items():
            if value['type'] == type_passed:
                return True
        
        return False
