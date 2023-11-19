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
        vpc VARCHAR(255) DEFAULT NULL,
        region VARCHAR(255) DEFAULT NULL,
        creation_timestamp DATETIME
    )
    """
    cursor.execute(create_table_query)

def query_gcp_vpcs_and_subnets():
    credentials, project = google.auth.default()
    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    # Query all regions
    regions_request = service.regions().list(project=project)
    regions_response = regions_request.execute()
    regions = regions_response.get('items', [])

    # Query VPCs
    vpcs_request = service.networks().list(project=project)
    vpcs_response = vpcs_request.execute()
    vpcs = vpcs_response.get('items', [])
    vpc_map = {vpc['selfLink']: vpc['name'] for vpc in vpcs}

    all_subnets = []
    for region in regions:
        region_name = region['name']

        subnets_request = service.subnetworks().list(project=project, region=region_name)
        subnets_response = subnets_request.execute()
        subnets = subnets_response.get('items', [])

        for subnet in subnets:
            subnet_vpc_name = vpc_map.get(subnet['network'])
            subnet_info = {
                "name": subnet['name'],
                "vpc": subnet_vpc_name,
                "region": region_name
            }
            all_subnets.append(subnet_info)

    return vpcs, all_subnets

def format_as_html(vpcs, all_subnets):
    html_output = "<html><body>"
    html_output += "<h1>VPCs and Subnets</h1>"

    for vpc in vpcs:
        html_output += f"<h2>VPC: {vpc['name']}</h2>"
        html_output += "<ul>"

        for subnet in all_subnets:
            if subnet['vpc'] == vpc['name']:
                html_output += f"<li>Subnet: {subnet['name']} in {subnet['region']}</li>"

        html_output += "</ul>"

    html_output += "</body></html>"

    return html_output

def save_to_database(cursor, vpcs, all_subnets):
    cursor.execute("DELETE FROM network_info")

    for vpc in vpcs:
        cursor.execute("""
            INSERT INTO network_info (resource_type, name, creation_timestamp)
            VALUES (%s, %s, %s)
            """, ('vpc', vpc['name'], vpc['creationTimestamp']))

    for subnet in all_subnets:
        cursor.execute("""
            INSERT INTO network_info (resource_type, name, vpc, region, creation_timestamp)
            VALUES (%s, %s, %s, %s, NULL)
            """, ('subnet', subnet['name'], subnet['vpc'], subnet['region']))

    cursor.connection.commit()

def list_vpcs_and_subnets(request):
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    create_table_if_not_exists(cursor)

    vpcs, all_subnets = query_gcp_vpcs_and_subnets()
    save_to_database(cursor, vpcs, all_subnets)
    
    html_output = format_as_html(vpcs, all_subnets)

    cursor.close()
    db_connection.close()

    return html_output
