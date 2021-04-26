from CSV import CSV

users = CSV("User.csv", ';')
users.convert_to_sql()

#if __name__ == '__main__':
#    convert_to_sql("User.csv", ';')
