class SQL():
    def __init__(self, file_name):
        self.table_name = file_name
        self.column_names = None

    def generate_from_csv(self, **kwargs):
        csv_separator = kwargs["separator"]
        csv_header_line = kwargs["header_line"]
        csv_data_lines = kwargs["data_lines"]
        self.create_table(csv_separator, csv_header_line, csv_data_lines)
        self.insert_data(csv_data_lines, csv_separator)
    
    def create_table(self, csv_separator, csv_header_line, csv_data_lines):
        self.column_names = self.get_column_names(csv_header_line, csv_separator)
        create_table_query = self.generate_create_table_query(csv_data_lines, csv_separator)
        self.write_to_file(create_table_query)

    def get_column_names(self, csv_header_line, csv_separator):
        column_names = csv_header_line.split(csv_separator)

        if len(column_names) <= 1:
            raise Exception("You need more than one column.")
        
        return list(map(self.format_column_name, column_names))

    def format_column_name(self, column_name):
        return column_name.replace(' ', '_').lower()

    def generate_create_table_query(self, csv_data_lines, csv_separator):
        query = f'CREATE TABLE "{self.table_name}"(\n'

        for index, column in enumerate(self.column_names):
            query += self.generate_create_table_column_line(index, column, csv_data_lines, csv_separator)
        
        query += ');\n\n'
        return query
    
    def generate_create_table_column_line(self, index, column, csv_data_lines, csv_separator):
        number_of_columns = len(self.column_names)
        is_last_column_line = (index == number_of_columns-1)

        if self.is_primary_key(index):
            return f'\t{column} {self.get_sql_column_type(index, csv_data_lines[0], csv_separator)} primary key,\n'

        if is_last_column_line:
            return f'\t{column} {self.get_sql_column_type(index, csv_data_lines[0], csv_separator)} not null\n'

        return f'\t{column} {self.get_sql_column_type(index, csv_data_lines[0], csv_separator)} not null,\n'

    def is_primary_key(self, column_index):
        return column_index == 0

    def get_sql_column_type(self, column_index, csv_data_line, csv_separator):
        first_row_values = csv_data_line.split(csv_separator)
        return self.convert_to_sql_data_type(first_row_values[column_index])

    def convert_to_sql_data_type(self, data):
        isText = False

        try:
            float(data)
        except ValueError:
            isText = True
        
        if isText:
            return "text"

        return "numeric"

    def insert_data(self, csv_data_lines, csv_separator):
        insert_values_statementes = self.generate_insert_values_statements(csv_data_lines, csv_separator)
        self.write_to_file(insert_values_statementes)
    
    def generate_insert_values_statements(self, csv_data_lines, csv_separator):
        query = ''

        for line in csv_data_lines:
            query += f'insert into "{self.table_name}" ('
            query += self.get_column_names_to_insert_statement()
            query += 'values('
            query += self.get_row_values_to_insert_statement(line, csv_separator)

        return query

    def get_column_names_to_insert_statement(self):
        str_return = ''
        for index, column in enumerate(self.column_names):
            str_return += f'{column}'
            if index+1 == len(self.column_names):
                str_return += ')'
            else:
                str_return += ','
        
        return str_return

    def get_row_values_to_insert_statement(self, csv_line, csv_separator):
        row_values = csv_line.split(csv_separator)
        str_return = ''
        for column_index, value in enumerate(row_values):
            if self.get_sql_column_type(column_index, csv_line, csv_separator) == "numeric":
                str_return += f"{value}"
            else:
                str_return += f"'{value}'"

            if column_index+1 == len(row_values):
                str_return += ');\n'
            else:
                str_return += ','
        
        return str_return

    def write_to_file(self, content):
        file_path = self.table_name + '.sql'
        with open(file_path, 'a') as sql_file:
            sql_file.write(content)