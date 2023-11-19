import pymysql
import os

def get_db_connection():
    host = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    unix_socket = f'/cloudsql/{host}'

    return pymysql.connect(user=user, password=password, unix_socket=unix_socket, db=db_name)

def list_vpcs_and_subnets(request):
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    # create_table_if_not_exists(cursor)
    # vpcs, subnets = query_gcp_vpcs_and_subnets()
    # save_to_database(cursor, vpcs, subnets)

    cursor.close()
    db_connection.close()
    return 'Function execution completed !!!'
