from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import mysql.connector as mysqlConnector
from mysql.connector import Error
import json
from collections import OrderedDict

app = Flask(__name__)
api = Api(app)


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysqlConnector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connected")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error '{err}'")


def createArray(connection, query):
    results = read_query(connection, query)
    array = []
    for row in results:
        array.append({'id': row[0],
                      'name': row[1],
                      'type': row[2],
                      'cargo': row[3],
                      'cost': row[4],
                      'flight': row[5],
                      'delivery': row[6],
                      'exp': row[7],
                      'mastery': row[8],
                      })
    connection.close()
    return array


@app.route('/planes')
def getPlanes():
    connection = create_db_connection('localhost', 'root', '', 'skyrama')
    query = 'SELECT * FROM planes'
    array = createArray(connection, query)
    return json.dumps({'count': len(array),
                       'planes': array},
                      indent=4)


if __name__ == '__main__':
    app.run(debug=True)
