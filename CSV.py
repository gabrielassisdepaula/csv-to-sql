from SQL import SQL

class CSV():
    def __init__(self, file_path, separator=','):
        if self.valid_file(file_path):
            self.file_path = file_path
            self.set_file_name()
            self.set_csv_lines(file_path)
            self.set_header_line()
            self.set_data_lines()
            self.separator = separator

    def valid_file(self, file_path):
        if file_path[-3:] == 'csv':
            return True
        raise Exception("Invalid file format.")

    def set_file_name(self):
        path = self.file_path.split('/')
        file = path[-1]
        self.file_name = file.replace('.csv', '').lower()

    def set_csv_lines(self, file_path):
        with open(file_path, 'r') as csv_file:
            csv_file = csv_file.readlines()
        self.csv_lines = [line.replace('\n', '') for line in csv_file]

    def set_header_line(self):
        self.header_line = self.csv_lines[0]

    def set_data_lines(self):
        self.data_lines = self.csv_lines[1:]

    def convert_to_sql(self):
        sql_file = SQL(self.file_name)
        sql_file.generate_from_csv(
            separator = self.separator,
            header_line = self.header_line,
            data_lines = self.data_lines
        )
        #self.create_table(csv_lines, separator)
        #self.insert_data("user", csv_lines, separator)

    
