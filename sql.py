"""Module that creates the database and tables
"""
import mysql.connector
from mysql.connector import errorcode
from database import my_cursor, connexion, upload_data
from constants import DATABASE_NAME, data_categories


TABLES = {}

# Create Category table (SQL REQUEST)
TABLES['Category'] = (
    "CREATE TABLE `Category` ("
    "   `id` SMALLINT NOT NULL AUTO_INCREMENT,"
    "   `name` varchar(450) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

# Create Products table (SQL REQUEST)
TABLES['Product'] = (
    "CREATE TABLE `Product` ("
    "  `id` SMALLINT NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(450) NOT NULL UNIQUE,"
    "  `url` varchar(450) NOT NULL,"
    "  `grade` varchar(40) ,"
    "  `id_category` SMALLINT NOT NULL ,"
    "  `store` varchar(540) ,"
    "  PRIMARY KEY (`id`),"
    "   CONSTRAINT  `fk_category_id` FOREIGN KEY (`id_category`)"
    "   REFERENCES `Category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE"

    ") ENGINE=InnoDB")


# Create Favorite table (SQL REQUEST)
TABLES['Favorite'] = (
    "CREATE TABLE `Favorite` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `product` varchar(450) NOT NULL,"
    "   `substitute` varchar(450) NOT NULL,"
    "   `lien` varchar(450) NOT NULL,"
    "   `grade` varchar(4) NOT NULL,"
    "   `id_product_substitute` SMALLINT NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "   CONSTRAINT  `fk_favorite_id` FOREIGN KEY (`id_product_substitute`)"
    "   REFERENCES `Product` (`id`) ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=InnoDB")


# definition of the function that creates the database
def create_database(cursor):
    """Function that creates the database and returns 1 if there is an error
    """
    try:
        cursor.execute(
            f"CREATE DATABASE {DATABASE_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)


def check_database():
    """Method checks if a database is created if not it creates it
    """
    try:
        my_cursor.execute(f"USE {DATABASE_NAME}")
        return False
    except mysql.connector.Error as err:
        print(f"Database {DATABASE_NAME} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(my_cursor)
            print(f"Database {DATABASE_NAME} created successfully.")
            connexion.database = DATABASE_NAME
            return True
        return False


# Function that creates a tables
def data_init():
    """Function that creates the different tables
    """
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            my_cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    # The categories of my table
    categoy_index = []

    for item in data_categories:
        categoy_index.append(item[1])

    categoy_index = tuple(categoy_index)

    # Insert 6 categories in my category table(manually)
    query2 = (
        "INSERT IGNORE INTO Category (id, name) VALUE (%s, %s)"
        )
    for i in data_categories:
        my_cursor.execute(query2, (i[0], i[1]))
        connexion.commit()

    # browse categories and insert data
    for index in range(len(categoy_index)):
        # Upload json file from api
        data_for_insert = upload_data(categoy_index[index], 1)
        # Insert data in Product table
        taille = len(data_for_insert['products'])
        print(f'{categoy_index[index]} - produits: {taille}')
        add_Product = (
            "INSERT IGNORE INTO Product "
            "(name, url, grade, id_category, store)"
            "VALUES (%s,  %s, %s, %s, %s)"
            )
        # The loop that inserts the data into my tables
        for i in range(taille):
            try:
                store = data_for_insert['products'][i]['stores']
                name = data_for_insert['products'][i]['product_name']
                grade = data_for_insert['products'][i]['nutrition_grades_tags'][0]
                url = data_for_insert['products'][i]['url']
                id_category = index+1
            except(KeyError, TypeError):
                continue
            finally:
                food_data_Product = (name, url, grade, id_category, store)
                my_cursor.execute(add_Product, food_data_Product)
                connexion.commit()
