from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!!"

@app.route('/hithere')
def hi_there_everyone():
    return "I just hit /hithere"

@app.route('/add_two_nums', methods=['POST'])
def add_two_nums():
    # Get x, y from the posted data
    dataDict = request.get_json()
    x = dataDict['x']
    y = dataDict['y']
    # Add z=x+y
    z = x+y
    # Prepare a JSON, "z": z
    retJSON = {
        'z': z
    }
    # return jsonify(map_prepared)
    return jsonify(retJSON)

@app.route('/bye')
def bye():
    # Prepare a response for the request that came to /bye
    c = 2*534
    s = str(c)
    age = 2*5
    retJson = {
        'Name': 'Ahmed',
        'Age': age,
        'phones': [
            {
                "phoneName": "Iphone8",
                "phoneNumber": 1111
            },
            {
                "phoneName": "Nokia",
                "phoneNumber": 1211
            }
        ]
       }
    return jsonify(retJson)

if __name__ == "__main__":
    app.run(debug=True)