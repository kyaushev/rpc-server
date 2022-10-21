from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import pandas as pd
import sqlalchemy
import json
import unicodedata

HOSTNAME = 'localhost'
USER = 'user'
PASSWORD = '12345678'
DATABASE = 'news_db'
TABLE = 'news'
connection_string = f'mariadb+pymysql://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE}?charset=utf8mb4'
engine = sqlalchemy.create_engine(connection_string, pool_size=20, pool_recycle=3600)

class RPC(Resource):
    def get_date_clause(self, *date_range):
        if (date_range[0]):
            if (date_range[1]):
                return f" WHERE post_date BETWEEN \'{start}\' AND \'{end}\';"
            return f" WHERE post_date = \'{start}\';"
        return ";"
    def select_query_string(self, *date_range):
        return f"SELECT * FROM {DATABASE}.{TABLE}{self.get_date_clause(date_range)}"
    
    def delete_query_string(self, id):
        return f"DELETE FROM {DATABASE}.{TABLE} WHERE id = {id}"

    def insert_query_string(self, title, body, postDate):
        return f"INSERT INTO {DATABASE}.{TABLE}(title, body, post_date) VALUES(\"{title}\", \"{body}\", \"{postDate}\")"
    
    def update_query_string(self, id, title, body, postDate):
        return f"UPDATE {DATABASE}.{TABLE} SET title = \"{title}\", body = \"{body}\", post_date = \"{postDate}\" WHERE id = {id}"    

    def make_query(self, query):
        return engine.execute(query)
    def make_select_query(self, query):
        return pd.read_sql_query(query, engine).to_json()
    
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
        print()
        print(content_type)
        print(request.json)
        print()
        if (content_type == 'application/json; charset=utf-8'):
            json_dict = request.json#json.loads(request.json)
            print()
            print(json_dict)
            print()
            if (all(elem in json_dict.keys() for elem in ["id", "func", "args"])):
                resp["id"] = json_dict["id"]
                func = json_dict["func"]
                if func == "deleteNews":
                    id = json_dict["args"][0]
                    query = self.delete_query_string(id)
                    try:
                        print(f"QUERY: {query}")
                        self.make_query(query)
                        resp["data"] = ""
                        resp["err"] = 0
                    except Exception as err:
                        print(f"ERR: {err}")
                        resp["err_description"] = "Database error"
                elif func == "addNews":        
                    title, body, postDate = json_dict["args"]
                    query = self.insert_query_string(title, body, postDate)
                    try:   
                        print(f"QUERY: {query}")
                        self.make_query(query)
                        resp["data"] = ""
                        resp["err"] = 0
                    except Exception as err:
                        print(f"ERR: {err}")
                        resp["err_description"] = "Database error"
                elif func == "updateNews":        
                    id, title, body, postDate = json_dict["args"]
                    query = self.update_query_string(id, title, body, postDate)
                    try:   
                        print(f"QUERY: {query}")
                        self.make_query(query)
                        resp["data"] = ""
                        resp["err"] = 0
                    except Exception as err:
                        print(f"ERR: {err}")
                        resp["err_description"] = "Database error"               
                elif func == "getNews":
                    query = self.select_query_string(*json_dict['args'])
                    try:   
                        print(f"QUERY: {query}")
                        resp["data"] = self.make_select_query(query) #.encode().decode('utf-8', errors='ignore')
                        resp["err"] = 0
                    except Exception as err:
                        print(f"ERR: {err}")
                        resp["err_description"] = "Database error"
                else: 
                    resp["err_description"] = f"Function \'{func}\' is not found"         
            else:
                resp["err_description"] = "Expected form: \{ \"id\": id, \"func\": func_name, \"args\": [start, end] \}"
        else:
            resp["err_description"] = f"Content-Type {content_type} is not supported!"

        return resp, 201
          
    def put(self):
        return "Use POST method instead", 404
    def delete(self, id):
        return "Use POST method instead", 404