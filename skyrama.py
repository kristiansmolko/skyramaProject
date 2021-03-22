from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
import methods as m

app = Flask(__name__)
api = Api(app)


@app.route('/planes/all')
def getPlanes():
    """
    Method that will return all planes

    Returns: json format with all planes
    """

    connection = m.create_db_connection('localhost', 'root', '', 'skyrama')
    query = 'SELECT * FROM planes'
    array = m.createArray(connection, query)
    return json.dumps({'count': len(array),
                       'planes': array},
                      indent=4)


@app.route('/planes', methods=['GET'])
def getPlanesBy():
    """
    Method that will return planes based on criteria
    """

    connection = m.create_db_connection('localhost', 'root', '', 'skyrama')
    if request.args.get('type'):
        """
        If parameter is type, method will find planes,
        with certain type
        
        If 'type' is not small, medium, large, helicopter
        or searama, will return code 400
        
        Returns: json format with planes
        """

        param = request.args.get('type')
        if param != 'small' and param != 'medium' and param != 'large' and param != 'helicopter' and param != 'searama':
            return "Wrong parameter", 400
        query = f"SELECT * FROM planes WHERE type like '{param}'"
        array = m.createArray(connection, query)
        return json.dumps({'count': len(array),
                           'planes': array},
                          indent=4), 200
    elif request.args.get('cargo'):
        """
        If parameter is cargo, method will find planes,
        with certain cargo type
        
        If 'cargo' is not cargo or passenger, will return
        code 400
        
        Returns: json format with planes
        """

        param = 1 if request.args.get('cargo') == 'cargo' else 0 if request.args.get('cargo') == 'passenger' else 2
        print(param)
        if param > 1 or param < 0:
            return "Wrong cargo type", 400
        query = "SELECT * FROM planes WHERE cargo = " + str(param)
        array = m.createArray(connection, query)
        return json.dumps({'count': len(array),
                           'planes': array},
                          indent=4), 200
    return "Something went wrong", 400


@app.route('/add', methods=['POST'])
def addPlane():
    """
    This method will add new plane to database

    If one of parameters is missing, will return
    code 400
    If 'type' is not small, medium, large, helicopter
    or searama, will return code 400
    If 'cargo' is not cargo or passenger, will
    return code 400
    If 'cost', 'delivery', 'exp' or 'flight' is
    lower than 0, will return code 400
    If mastery is not True or False, will return
    code 400

    Returns: code 201 (if created)
             code 400 (if error)
    """
    body = request.get_json()
    name = body.get('name')
    if name is None or name == '':
        return "Wrong name", 400
    type = body.get('type').lower()
    if type != 'small' and type != 'medium' and type != 'large' and type != 'helicopter' and type != 'searama':
        return "Wrong type", 400
    if body.get('cargo') != 'cargo' and body.get('cargo') != 'passenger':
        return "Wrong cargo type", 400
    cargo = 1 if body.get('cargo') == 'cargo' else 0
    cost = body.get('cost')
    if cost < 0:
        return "Wrong input at cost", 400
    flight = m.getFlightTime(str(body.get('flight')))
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
    connection = m.create_db_connection('localhost', 'root', '', 'skyrama')
    query = f"INSERT INTO planes(name, type, cargo, cost, flight, delivery, exp, mastery) VALUES('{name}', " \
            f"'{type}', {cargo}, {cost}, {flight}, {delivery}, {exp}, {mastery})"
    if m.execute_query(connection, query) is None:
        return "Error", 400
    return "Plane added", 201


@app.route('/event', methods=['GET', 'PUT'])
def event():
    """
    Method that works with event table in database
    """

    if request.method == 'GET':
        """
        If method is 'GET', will connect to database
        and return event currency value
        
        Returns: string with currency value
        """

        connection = m.create_db_connection('localhost', 'root', '', 'skyrama')
        query = "SELECT * FROM event"
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        for row in result:
            return "Current event currency: " + str(row[0]), 200
    if request.method == 'PUT':
        """
        If method is 'PUT', will connect to database
        and change actual value of currency
        
        Returns: string with updated value
        """

        body = request.get_json()
        value = body.get('value')
        if value < 0:
            return "Wrong value", 400
        connection = m.create_db_connection('localhost', 'root', '', 'skyrama')
        query = f"UPDATE event SET currency = {value}"
        if m.execute_query(connection, query) is None:
            return "Error", 400
        return f"Currency updated, new value {value}", 200


@app.route('/delete', methods=['DELETE'])
def deletePlane():
    """
    Method will delete plane from database

    If plane does not exist, returns code 404
    If name is empty, returns code 400

    Returns: code 200 (if deleted)
             code 400 (if error)
    """

    name = request.args.get('name')
    if len(m.findPlane(name)) == 0:
        return "Could not find plane", 404
    if name == '':
        return "Wrong name", 400
    connection = m.create_db_connection('localhost', 'root', '', 'skyrama')
    query = f"DELETE FROM planes WHERE name like '{name}'"
    if m.execute_query(connection, query) is None:
        return "Error", 400
    return "Plane deleted ;(", 200


if __name__ == '__main__':
    app.run(debug=True)
