from distutils.log import debug
from urllib import request
from winreg import DisableReflectionKey
from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

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
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
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

@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"name":request.form["name"], "lastName":request.form["lastName"]}}
        )
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")
        
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message":"User has been updated"}),
                status=500,
                mimetype="application/json"
            )
        
        else:
            return Response(
                response=json.dumps({"message":"Nothing to update"}),
                status=500,
                mimetype="application/json"
            )

    except Exception as ex:
        print("*********")
        print(ex)
        print("*********")
        return Response(
            response=json.dumps({"message":"user cannot be updated"}),
            status=500,
            mimetype="application/json"
        )
    
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")
        if dbResponse.deleted_count == 1:
            return Response(
                    response=json.dumps({"message":"User has been deleted", "id":f"{id}"}),
                    status=500,
                    mimetype="application/json"
                )

        return Response(
                    response=json.dumps({"message":"User not found", "id":f"{id}"}),
                    status=500,
                    mimetype="application/json"
                )

    except Exception as ex:
        print("*********")
        print(ex)
        print("*********")
        return Response(
            response=json.dumps({"message":"user cannot be deleted"}),
            status=500,
            mimetype="application/json"
        )

if __name__ == '__main__':
    app.run(port=80, debug=True)