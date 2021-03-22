import mysql.connector as mysqlConnector
from mysql.connector import Error


def create_db_connection(host_name, user_name, user_password, db_name):
    """
    Method that connects to database

    If error occurs, will return error

    Returns: connection to database
    """

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
    """
    Method that will execute provided query

    Returns: True (if query was executed)
             None (if error occurred)
    """

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
        return True
    except Error as err:
        print(f"Error '{err}'")
        return None


def read_query(connection, query):
    """
    Method that will execute "SELECT" query

    Returns: result from query (list)
    """

    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error '{err}'")


def createArray(connection, query):
    """
    Method will create custom array with information
    about planes

    Returns: custom array with planes
    """

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
    """
    Method will compute flight time

    Returns: integer with time in seconds
    """

    times = time.split(":")
    if int(times[1]) > 60 or int(times[0]) > 24 or int(times[1]) < 0 or int(times[0]) < 0:
        return False
    hour = int(times[0]) * 3600
    minute = int(times[1]) * 60
    return hour + minute


def makeFlightTime(time):
    """
    Method will create string from seconds

    Returns: string format of time
    """

    hour = int(time / 3600)
    minutes = int((time % 3600) / 60)
    return f"{hour}:{minutes}"


def findPlane(name):
    """
    Method that will search for plane in database

    Returns: array with plane/s
    """

    if name is None or name == '':
        return []
    connection = create_db_connection('localhost', 'root', '', 'skyrama')
    query = f"SELECT * FROM planes WHERE name like '{name}'"
    return createArray(connection, query)
