import pymysql
import os

def get_db_connection():
    host = os.environ.get('DB_HOST')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    return pymysql.connect(host=host, user=user, password=password, db=db_name)

def list_vpcs_and_subnets(request):
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    create_table_if_not_exists(cursor)

    cursor.close()
    db_connection.close()
    return 'Function execution completed !!!'
