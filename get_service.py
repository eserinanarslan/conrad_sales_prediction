import pandas as pd
import os

import sqlite3 as sql
import flask
from flask import request, jsonify
import configparser


import json
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.float_format', '{:.4f}'.format)


config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

data = pd.read_csv(os.getcwd()+"/ds_takehome_task/submission.csv")

conn = sql.connect(os.getcwd()+"/ds_takehome_task/submission.db")
data.to_sql("submission", conn, if_exists='replace')

data = pd.read_sql("SELECT * FROM submission", conn).drop(columns="index")
unique_data = pd.read_csv(os.getcwd()+"/ds_takehome_task/submission.csv")

data.fillna("NA", inplace=True)
unique_data.fillna("NA", inplace=True)

df = data.to_json(orient="records")
df = json.loads(df)

df_unique = unique_data.to_json(orient="records")
df_unique = json.loads(df_unique)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/all_sales', methods=['GET'])
def total_api():
    return jsonify(df[:100])

@app.route('/sales', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'productsGroup_key' in request.args:
        productsGroup_key = request.args['productsGroup_key']
    else:
        return "Error: No productsGroup_key field provided. Please specify a key."

    # Create an empty list for our results
    results = []
    # Loop through the data and match results that fit the requested ID.

    for id_ in range(len(df)):
        if (df[id_]["productsGroup_key"] == productsGroup_key):
            results.append(df[id_])

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    if len(results)<1:
        return "Products Group Key is not found", 404
    else:
        return jsonify(results)

app.run(host=config["Service"]["Host"], port=int(config["Service"]["Port"]), debug=True)


