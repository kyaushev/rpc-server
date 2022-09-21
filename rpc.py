from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import pandas as pd
import sqlalchemy
import json

HOSTNAME = 'localhost'
USER = 'user'
PASSWORD = '12345678'
DATABASE = 'news_db'
TABLE = 'news'
connection_string = f'mariadb+pymysql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}?charset=utf8mb4'
engine = sqlalchemy.create_engine(connection_string, pool_size=20, pool_recycle=3600)

class RPC(Resource):
    def get_date_clause(self, start, end):
        if (start):
            if (end):
                return f" WHERE post_date BETWEEN \'{start}\' AND \'{end}\';"
            return f" WHERE post_date = \'{start}\';"
        return ";"
    def query_string(self, start, end):
        return f"SELECT * FROM {DATABASE}.{TABLE}{self.get_date_clause(start, end)}"
    
    def make_query(self, query):
        data = pd.read_sql_query(query, engine).to_json()

        return             
    
    def get(self):
        return "Use POST method instead", 404
    def post(self):
        resp = {
            "id": -1, 
            "err": 1, 
            "err_description": "", 
            "data": {}
        }
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json_dict = json.loads(request.json)
            if (all(elem in json_dict.keys() for elem in ["id", "func", "args"])):
                resp["id"] = json_dict["id"]
                start, end = json_dict["args"]
                query = self.query_string(start, end)
                try:  
                    
                    print(f"QUERY: {query}")
                    resp["data"] = self.make_query(query).to_json()
                    resp["err"] = 0
                except Exception as err:
                    print(f"ERR: {err}")
                    resp["err_description"] = "Database error"  
            else:
                resp["err_description"] = "Expected form: \{ \"id\": id, \"func\": func_name, \"args\": [start, end] \}"
        else:
            resp["err_description"] = f"Content-Type {content_type} is not supported!"

        return resp, 201
          
    def put(self):
        return "Use POST method instead", 404
    def delete(self, id):
        return "Use POST method instead", 404