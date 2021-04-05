'''
To use this script:

1. Create a .env enviroment file in the current directory:

MYSQL_HOST=xxxxxx.xxxxx.xxxxxx
MYSQL_PORT=3306
MYSQL_USER=xxxxx
MYSQL_PASSWORD=xxxxx
MYSQL_DATABASE=xxxxx

2. Make sure to install dependent packages:

$ pip install python-dotenv
$ pip install sqlalchemy
$ pip install mysql-connector
$ pip install pymysql

'''

# import required modules
import os, sys
from dotenv import load_dotenv
import pymysql
import sqlalchemy as sa
import mysql.connector
import pandas as pd

def env(file = '.env'):
    """
    Load os environment variables using `python-dotenv`
    See: https://pypi.org/project/python-dotenv/
    """
    try:
        # load environment variables using `python-dotenv`
        load_dotenv(file)

        # connection-related variables (hoisted!)
        global host, port, user, password, database, connString

        # set variables to values stored in newly-populated environment variables
        host = os.getenv('MYSQL_HOST')
        port = int(os.getenv('MYSQL_PORT'))
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DATABASE')

        # build connect string (needed if using sqlalchemy)
        connString = "mysql+pymysql://%s:%s@%s:%s/%s" % (user, password, host, port, database)
        print("Environment loaded...")
    except:
        print("Error preparing environment", sys.exc_info()[0])
        # uncomment to see full stack trace
        # raise
        print('exiting...')
        sys.exit(1)
        
def getPyConnection():
    """
    See: https://pymysql.readthedocs.io/en/latest/

    Returns
    -------
    connection
       Obtained from the pymysql MySQL client library
    """
    try:
        conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database)
        print('Establishing connection to %s@%s:%s\n' % (database, host, str(port)))
        return conn
    except: 
        print("Unable to connect to database using pymysql", sys.exc_info()[0])
        # uncomment to see full stack trace
        # raise
        print('exiting...')
        sys.exit(1)

def getSaConnection(echo = False):
    """
    See: https://docs.sqlalchemy.org/en/14/

    Parameters
    ----------
    echo : bool, default False
       Whether to enable sa logging/debugging

    Returns
    -------
    connection (object instance)
       Obtained from the SQLAlchemy MySQL client library

    """
    try:
        # uncomment to verify connect string used by sa
        # print('sqlalchemy connect string\n%s' % connString)
        # pass in echo=True to debug
        cnx = sa.create_engine(connString, echo=echo)
        print('Establishing connection to %s@%s:%s' % (database, host, str(port)))
        return cnx
    except:
        print("Unable to create sqlalchemy engine (check credentials)", sys.exc_info()[0])
        # uncomment below to see full stack trace
        # raise
        print('exiting...')
        sys.exit(1)

def testConnection(conn):
    """    
    Parameters
    ----------
    conn : connection (object instane)
        If using SQLAlchemy, you must pass raw connection, e.g., `conn.raw_connection()`

    Returns
    -------
    boolean
       Result of test database query
    """
    try:
        with conn.cursor() as curr:
            curr.execute("SELECT 'Hello, World!'")
            status = curr.fetchone()
            return True
    except:
        return False
    finally:
        curr.close()

# main program loop
env('.env')
conn = getSaConnection(False)
if (testConnection(conn.raw_connection())):
    print('Connection established using SQLAlchemy...\n')
    
    # https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
    print('Loading all the pets (from csv)\n')
    pets_from_csv_df = pd.read_csv("pets.csv")
    print(pets_from_csv_df)
    
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    print('\nInserting all the pets (into db)\n')
    pets_from_csv_df.to_sql('pets', con=conn, index=False, if_exists='replace')

    # https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html
    print('Selecting all the pets (from db)\n')
    pets_from_db_df = pd.read_sql_query("SELECT * FROM pets", con=conn)
    print(pets_from_db_df)

