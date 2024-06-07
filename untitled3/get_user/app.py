import json
import os
import mysql.connector


def lambda_handler(event, context):
    # Obtener variables de entorno
    db_host = os.environ['DBHOST']
    db_user = os.environ['DBUSER']
    db_password = os.environ['DBPASSWORD']
    db_name = os.environ['DBDATABASE']

    # Conexión a la base de datos
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = connection.cursor()

        sql = "SELECT * FROM personas"
        cursor.execute(sql)
        users = cursor.fetchall()

        if users:
            user_list = []
            for user in users:
                user_dict = {
                    'id': user[0],
                    'nombre': user[1],
                    'apellido': user[2],
                    'edad': user[3]
                }
                user_list.append(user_dict)

            return {
                'statusCode': 200,
                'body': json.dumps(user_list),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No users found'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
