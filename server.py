from distutils.log import debug
from urllib import request
from flask import Flask, Response, request
import pymongo
import json

app = Flask(__name__)


try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
    db = mongo.company
    mongo.server_info() #trigger exception if cant connect to DB
except:
    print("ERROR - Can't connect to DB")

@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        print(data)
        return Response(
            response=json.dumps({"message":"success"}),
            status=200,
            mimetype="application/json"
        )
    
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message":"can't read users"}),
            status=500,
            mimetype="application/json"
        )

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {"name": request.form["name"], "lastName": request.form["lastName"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        return Response(
            response=json.dumps({"message":"user created","id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print("******")
        print(ex)
        print("******")



if __name__ == '__main__':
    app.run(port=80, debug=True)