import requests
import json
import mysql.connector
from mysql.connector import errorcode

# Creation a connexion to database
try:
    connexion = mysql.connector.connect(host='127.0.0.1', user='root', passwd='')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
   
my_cursor = connexion.cursor()

# Create database 'Food'
DB_NAME = 'Food'

# Create tables
TABLES = {}
TABLES['Product'] = (

)
TABLES['Category'] = (

)
TABLES['Store'] = (

)

my_cursor = connexion.cursor()
json_data = None

def upload_data():
    api_search = 'https://world.openfoodfacts.org/cgi/search.pl?/get'
    payload = {'search_terms': '',
           'json': 1,
           'page_size': 10,
           'page': 1
          }
    json_data = requests.get(api_search, params=payload).json()
    #taille = len(json_data['products'])
    return json_data