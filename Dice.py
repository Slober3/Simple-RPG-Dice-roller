import json
import argparse
import random
from time import time
from hashlib import sha256
from flask import Flask, jsonify, request, render_template

parser = argparse.ArgumentParser(description="Command line arguments")
parser.add_argument('-p',action='store', metavar='<port>', default='5000', help='The port to listen on default 5000')
args = parser.parse_args()

def dice_gen(number):
    return random.randint(1, number)

def dice_proof(number,dice_time):
    y = 0
    while sha256(f'{number}{y}{dice_time}'.encode()).hexdigest()[:5] != "00000":
        y += 1
    return y

def dice_validate_proof(proof,result,dice_time):
    return sha256(f'{result}{proof}{dice_time}'.encode()).hexdigest()[:5] == "00000"

app = Flask(__name__)
@app.route('/dice/json/<int:number>', methods=['GET'])
def json_dice(number):
    result = dice_gen(number)
    dice_time = time()
    response = {
        'message': "New dice roll ",
        'type': "d%s" %number,
        'result': result,
        'proof' : dice_proof(result,dice_time),
        'timestamp': dice_time,
    }
    return jsonify(response), 200

@app.route('/dice/<int:number>', methods=['GET'])
def dice(number):
    return render_template('dice.html', number=number,result=dice_gen(number))

@app.route('/validate/<int:result>/<int:proof>/<float:dice_time_r>', methods=['GET'])
def dice_validate(proof,result,dice_time_r):
    result = dice_validate_proof(result,proof,dice_time_r)
    dice_time = time()
    response = {
        'message': "Validate",
        'type': result,
        'timestamp': dice_time,
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(args.p))