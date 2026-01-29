from flask import Flask
import mysql.connector

app = Flask(__name__)

cnx = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = 'infoj',
    database = 'mitoverso'
)

cursor = cnx.cursor()