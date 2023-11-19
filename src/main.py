import googleapiclient.discovery
import google.auth
import pymysql
import os

def get_db_connection():
    host = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    unix_socket = f'/cloudsql/{host}'

    return pymysql.connect(user=user, password=password, unix_socket=unix_socket, db=db_name)

def create_table_if_not_exists(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS network_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        resource_type VARCHAR(255),
        name VARCHAR(255),
        creation_timestamp DATETIME
    )
    """
    cursor.execute(create_table_query)

def query_gcp_vpcs_and_subnets():
    credentials, project = google.auth.default()
    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    # Query VPCs
    vpcs_request = service.networks().list(project=project)
    vpcs_response = vpcs_request.execute()
    vpcs = vpcs_response.get('items', [])

    # Query Subnets
    subnets_request = service.subnetworks().list(project=project, region='your-region')
    subnets_response = subnets_request.execute()
    subnets = subnets_response.get('items', [])

    return vpcs, subnets

def list_vpcs_and_subnets(request):
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    create_table_if_not_exists(cursor)
    vpcs, subnets = query_gcp_vpcs_and_subnets()

    vpcs_str = "\n".join([f"VPC Name: {vpc['name']}, Creation Timestamp: {vpc['creationTimestamp']}" for vpc in vpcs])
    subnets_str = "\n".join([f"Subnet Name: {subnet['name']}, Region: {subnet['region']}" for subnet in subnets])

    # save_to_database(cursor, vpcs, subnets)

    cursor.close()
    db_connection.close()
    return f"VPCs:\n{vpcs_str}\n-------------\nSUBNETS:\n{subnets_str}\n\n------------\nFunction execution completed !!!"
