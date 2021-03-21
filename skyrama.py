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
        flight = makeFlightTime(row[5])
        array.append({'id': row[0],
                      'name': row[1],
                      'type': row[2],
                      'cargo': row[3],
                      'cost': row[4],
                      'flight': flight,
                      'delivery': row[6],
                      'exp': row[7],
                      'mastery': row[8],
                      })
    connection.close()
    return array


def getFlightTime(time):
    times = time.split(":")
    if int(times[1]) > 60 or int(times[0]) > 24 or int(times[1]) < 0 or int(times[0]) < 0:
        return False
    hour = int(times[0]) * 3600
    minute = int(times[1]) * 60
    return hour + minute


def makeFlightTime(time):
    hour = int(time / 3600)
    minutes = int((time % 3600) / 60)
    return f"{hour}:{minutes}"


@app.route('/planes/all')
def getPlanes():
    connection = create_db_connection('localhost', 'root', '', 'skyrama')
    query = 'SELECT * FROM planes'
    array = createArray(connection, query)
    return json.dumps({'count': len(array),
                       'planes': array},
                      indent=4)


@app.route('/planes', methods=['GET'])
def getPlanesBy():
    if request.args.get('type'):
        param = request.args.get('type')
        if param != 'small' and param != 'medium' and param != 'large' and param != 'helicopter' and param != 'searama':
            return "Wrong parameter", 400
        connection = create_db_connection('localhost', 'root', '', 'skyrama')
        query = "SELECT * FROM planes WHERE type like '" + param + "'"
        array = createArray(connection, query)
        return json.dumps({'count': len(array),
                           'planes': array},
                          indent=4), 200
    elif request.args.get('cargo'):
        param = 1 if request.args.get('cargo') == 'cargo' else 0 if request.args.get('cargo') == 'passenger' else 2
        print(param)
        if param > 1 or param < 0:
            return "Wrong cargo type", 400
        connection = create_db_connection('localhost', 'root', '', 'skyrama')
        query = "SELECT * FROM planes WHERE cargo = " + str(param)
        array = createArray(connection, query)
        return json.dumps({'count': len(array),
                           'planes': array},
                          indent=4), 200
    return "Something went wrong", 400


@app.route('/add', methods=['POST'])
def addPlane():
    body = request.get_json()
    name = body.get('name')
    type = body.get('type').lower()
    if type != 'small' and type != 'medium' and type != 'large' and type != 'helicopter' and type != 'searama':
        return "Wrong type", 400
    if body.get('cargo') != 'cargo' and body.get('cargo') != 'passenger':
        return "Wrong cargo type", 400
    cargo = 1 if body.get('cargo') == 'cargo' else 0
    cost = body.get('cost')
    if cost < 0:
        return "Wrong input at cost", 400
    flight = getFlightTime(str(body.get('flight')))
    if not flight:
        return "Wrong flight time", 400
    delivery = body.get('delivery')
    if delivery < 0:
        return "Wrong delivery", 400
    exp = body.get('exp')
    if exp < 0:
        return "Wrong exp", 400
    mastery = body.get('mastery')
    if mastery is not True and mastery is not False:
        return "Wrong mastery", 400
    connection = create_db_connection('localhost', 'root', '', 'skyrama')
    query = f"INSERT INTO planes(name, type, cargo, cost, flight, delivery, exp, mastery) VALUES('{name}', " \
            f"'{type}', {cargo}, {cost}, {flight}, {delivery}, {exp}, {mastery})"
    execute_query(connection, query)
    return "Plane added", 201


@app.route('/event', methods=['GET', 'PUT'])
def event():
    if request.method == 'GET':
        connection = create_db_connection('localhost', 'root', '', 'skyrama')
        query = "SELECT * FROM event"
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        for row in result:
            return "Current event currency: " + str(row[0]), 200
    if request.method == 'PUT':
        body = request.get_json()
        value = body.get('value')
        if value < 0:
            return "Wrong value", 400
        connection = create_db_connection('localhost', 'root', '', 'skyrama')
        query = f"UPDATE event SET currency = {value}"
        execute_query(connection, query)
        return f"Currency updated, new value {value}", 200


def findPlane(name):
    connection = create_db_connection('localhost', 'root', '', 'skyrama')
    query = f"SELECT * FROM planes WHERE name like '{name}'"
    return createArray(connection, query)


@app.route('/delete', methods=['DELETE'])
def deletePlane():
    name = request.args.get('name')
    if len(findPlane(name)) == 0:
        return "Could not find plane", 404
    if name == '':
        return "Wrong name", 400
    connection = create_db_connection('localhost', 'root', '', 'skyrama')
    query = f"DELETE FROM planes WHERE name like '{name}'"
    execute_query(connection, query)
    return "Plane deleted ;(", 200


if __name__ == '__main__':
    app.run(debug=True)
