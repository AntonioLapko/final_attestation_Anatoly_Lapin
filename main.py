from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource, reqparse
import psycopg2
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder
connection = psycopg2.connect(dbname='final_attestation', user='alapin', password='1234', host='localhost')
cursor = connection.cursor()
create_table_query = '''CREATE TABLE mobile
                          (lot INT PRIMARY KEY     NOT NULL,
                          ph REAL    NOT NULL,
                          temperature REAL NOT NULL,
                          color REAL NOT NULL); '''
cursor.execute(create_table_query)
connection.commit()
app = Flask(__name__)
api = Api(app)
##@app.route('/')
##def index():
##    return render_template('index.html')

class Milk(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("lot")
        parser.add_argument("ph")
        parser.add_argument("temperature")
        parser.add_argument("color")
        params = parser.parse_args()
        insert_query = """ INSERT INTO mobile (lot, ph, temperature, color) 
        VALUES (params["lot"], params["ph"], params["temperature"], params["color"])"""
        cursor.execute(insert_query)
        connection.commit()

api.add_resource(Milk, "/milk")
if __name__ == '__main__':
    app.run(debug=True)
