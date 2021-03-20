from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import mysql.connector as mysqlConnector
from mysql.connector import Error
import json

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