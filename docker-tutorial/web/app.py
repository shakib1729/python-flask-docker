from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)

api = Api(app)

client = MongoClient("mongodb://db:27017")

# Create a database
db = client.aNewDB

# Create a new collection
UserNum = db["UserNum"] 

# Insert a document that tracks number of visited users
UserNum.insert({
    'num_of_users': 0
})

class Visit(Resource):
    def get(self):
        print('Number of Documents: ', UserNum.find({}).count())
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {'$set':{'num_of_users': new_num}})
        return str("Hello user " + str(new_num))

def checkPostedData(postedData, functionName):
    if functionName == 'add' or functionName == 'subtract' or functionName == 'multiply':
        if ('x' not in postedData) or ('y' not in postedData):
            return 301 # Missing parameter
        else:
            return 200
    elif functionName == 'division':
        if ('x' not in postedData) or ('y' not in postedData):
            return 301 # Missing parameter
        elif int(postedData['y']) == 0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        # If I am here, then the resource Add was requested using the method POST

        # Step 1: Get posted data:
        postedData = request.get_json()

        # Step1b: Verify the validity of posted data
        status_code = checkPostedData(postedData, 'add')

        if status_code != 200:
            retJson = {
                'Message': 'An error has happened',
                'Status Code': status_code
            }
            return jsonify(retJson)

        # If I am here, then status code == 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Add the posted data
        ret = x+y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        # If I am here, then the resource Subtract was requested using the method POST

        # Step 1: Get posted data:
        postedData = request.get_json()

        # Step1b: Verify the validity of posted data
        status_code = checkPostedData(postedData, 'subtract')

        if status_code != 200:
            retJson = {
                'Message': 'An error has happened',
                'Status Code': status_code
            }
            return jsonify(retJson)

        # If I am here, then status code == 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Subtract the posted data
        ret = x-y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        # If I am here, then the resource Multiply was requested using the method POST

        # Step 1: Get posted data:
        postedData = request.get_json()

        # Step1b: Verify the validity of posted data
        status_code = checkPostedData(postedData, 'multiply')

        if status_code != 200:
            retJson = {
                'Message': 'An error has happened',
                'Status Code': status_code
            }
            return jsonify(retJson)

        # If I am here, then status code == 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Multiply the posted data
        ret = x*y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        # If I am here, then the resource Divide was requested using the method POST

        # Step 1: Get posted data:
        postedData = request.get_json()

        # Step1b: Verify the validity of posted data
        status_code = checkPostedData(postedData, 'division')

        if status_code != 200:
            retJson = {
                'Message': 'An error has happened oh my god you are in division',
                'Status Code': status_code
            }
            return jsonify(retJson)

        # If I am here, then status code == 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Divide the posted data
        ret = (x*1.0)/y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/division')
api.add_resource(Visit, '/hello')

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
