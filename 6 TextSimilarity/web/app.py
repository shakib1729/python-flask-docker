from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')

db = client.SimilarityDB
users = db['Users']


def userExists(username):
    if users.count_documents({'Username': username}) == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']
        
        if userExists(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            'Username': username,
            'Password': hashed_pw,
            'Tokens': 6
        })

        retJson = {
            'status': 200,
            'msg': "You've successfully signed up for the API"
        }

        return jsonify(retJson)

def verifyPw(username, password):
    if not userExists(username):
        return False
    
    hashed_pw = users.find({
        'Username': username
    })[0]['Password']

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        'Username': username
    })[0]['Tokens']

    return tokens

class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']

        text1 = postedData['text1']
        text2 = postedData['text2']
        
        if not userExists(username):
            retJson = {
                'status': 301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                'status': 302,
                'msg': 'Invalid Password'
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = {
                'status': 303,
                'msg': 'Out of tokens'
            }
            return jsonify(retJson)

        # Calculate edit distance
        nlp = spacy.load('en_core_web_sm')

        text1 = nlp(text1)
        text2 = nlp(text2)
        
        # Ratio is a number between 0 and 1
        # The closer to 1, the more similar text1 and text2 are
        ratio = text1.similarity(text2)

        retJson = {
            'status': 200,
            'similarity': ratio,
            'msg': 'Similarity score calculated successfully'
        }

        users.update({
            'Username': username
        }, {
            '$set':{
                'Tokens': num_tokens-1
            }
        })

        return jsonify(retJson)


class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['admin_pw']
        refill_amount = postedData['refill']
        
        if not userExists(username):
            retJson = {
                'status': 301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)
        
        # For now, we are just hardcoding the admin password
        # We should make a new collection 'Admin' and store username and correct password there
        correct_pw = "abc123"
        if not password == correct_pw:
            retJson = {
                'status': 304,
                'msg': 'Invalid Admin Password'
            }
            return jsonify(retJson)

        users.update({
            'Username': username
        },{
            '$set':{
                'Tokens': refill_amount
            }
        })

        retJson = {
            'status': 200,
            'msg': 'Refilled successfully'
        }

        return jsonify(retJson)

api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__ == '__main__':
    app.run(host='0.0.0.0')