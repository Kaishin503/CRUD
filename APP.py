
from flask_cors import CORS
from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv
from CRUDFUNCTIONS import create_product,create_category,list_products,search_product,update_product,delete_product
load_dotenv()

def get_connection():
    return pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    "Trusted_Connection=yes;")


app = Flask(__name__)
CORS(app)

@app.route("/products",methods=["GET","POST"])
def products():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        id_or_name = request.args.get("id_or_name")
        if id_or_name:
            try:
                results = search_product(cursor,id_or_name)
            except ValueError as err:
                return jsonify({"ERROR_MESSAGE":str(err)}),404
        else:
            results = list_products(cursor)
        return jsonify(results),200
    if request.method == "POST":
        data = request.get_json()
        try:
            product_creation = create_product(cursor,data["NAME"],data["CATEGORY"],data["PRICE"],data["STOCK"])
            conn.commit()
            return jsonify({"MESSAGE":product_creation}),201
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400
        
@app.route("/products/<int:id>",methods=["PUT","DELETE"])
def product(id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "PUT":
        data = request.get_json()
        try:
            product_update = update_product(cursor,id,name=data["NAME"],category=data["CATEGORY"],price=data["PRICE"])
            conn.commit()
            return jsonify({"MESSAGE":product_update}),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400
    if request.method == "DELETE":
        try:
            product_deletion = delete_product(cursor,id)
            conn.commit()
            return jsonify({"MESSAGE":product_deletion}),200
        except ValueError as err:
            return jsonify({"ERROR_MESSAGE":str(err)}),400

@app.route("/categories",methods=["POST"])
def categories():
    conn = get_connection()
    cursor = conn.cursor()
    dados = request.get_json()
    try:
        category_creation = create_category(cursor,dados["CATEGORY_NAME"])
        conn.commit()
        return jsonify({"MESSAGE":category_creation}),201
    except ValueError as err:
        return jsonify({"ERROR_MESSAGE":str(err)}),400

if __name__ == "__main__":
    app.run(debug=True)