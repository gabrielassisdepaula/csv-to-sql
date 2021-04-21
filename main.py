def convert_to_sql(csv_file_path, separator):
    global csv_lines
    csv_lines = get_csv_file_lines(csv_file_path)
    create_table(csv_lines, separator)
    insert_data("user", csv_lines, separator)

def get_csv_file_lines(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_file = csv_file.readlines()
    return [line.replace('\n', '') for line in csv_file]
    
def create_table(csv_lines, separator):
    column_names = get_column_names(csv_lines, separator)
    create_table_query = generate_create_table_query("user", column_names)
    write_to_sql_file("user.sql", create_table_query)

def insert_data(table_name, csv_lines, separator):
    insert_values_statements = generate_insert_values_statements(table_name, csv_lines, separator)
    write_to_sql_file("user.sql", insert_values_statements)

def generate_insert_values_statements(table_name, csv_lines, separator):
    query = ''
    data_lines = get_csv_data_lines(csv_lines)
    column_names = get_column_names(csv_lines, separator)

    for line in data_lines:
        query += f'insert into "{table_name}" ('
        query += get_column_names_to_insert_statement(column_names)
        query += 'values('
        query += get_row_values_to_insert_statement(line, separator)

    return query

def get_csv_data_lines(csv_lines):
    return csv_lines[1:]

def get_column_names(csv_lines, separator):
    header_line = csv_lines[0]
    column_names = header_line.split(separator)

    if len(column_names) == 1:
        raise Exception("There is only one column in the csv.")

    return list(map(format_column_name, column_names))

def get_column_names_to_insert_statement(column_names):
    str_return = ''
    for index, column in enumerate(column_names):
        str_return += f'{column}'
        if index+1 == len(column_names):
            str_return += ')'
        else:
            str_return += ','
    
    return str_return

def get_row_values_to_insert_statement(line, separator):
    row_values = line.split(separator)
    str_return = ''
    for index, value in enumerate(row_values):
        if get_sql_column_type(index) == "numeric":
            str_return += f"{value}"
        else:
            str_return += f"'{value}'"

        if index+1 == len(row_values):
            str_return += ');\n'
        else:
            str_return += ','
    
    return str_return

def format_column_name(column_name):
    return column_name.replace(' ', '_').lower()

def generate_create_table_query(table_name, column_names):
    query = f'CREATE TABLE "{table_name}"(\n'

    for index, column in enumerate(column_names):
        query += create_table_column_sql_statement(index, len(column_names), column)
    
    query += ');\n\n'
    return query

def create_table_column_sql_statement(index, total_amount_of_columns, column):
    is_primary_key_column = index == 0
    is_last_line = index == total_amount_of_columns-1

    if is_primary_key_column:
        return f'\t{column} {get_sql_column_type(index)} primary key,\n'

    if is_last_line:
        return f'\t{column} {get_sql_column_type(index)} not null\n'

    return f'\t{column} {get_sql_column_type(index)} not null,\n'

def get_sql_column_type(index):
    first_row_values = csv_lines[1].split(';')
    return convert_to_sql_data_type(first_row_values[index])

def convert_to_sql_data_type(data):
    isText = False

    try:
        float(data)
    except ValueError:
        isText = True
    
    if isText:
        return "text"

    return "numeric"

def write_to_sql_file(file_path, query):
    with open(file_path, 'a') as sql_file:
        sql_file.write(query)

if __name__ == '__main__':
    convert_to_sql("User.csv", ';')
