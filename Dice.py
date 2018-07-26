import json
import argparse
import random
from time import time
from flask import Flask, jsonify, request, render_template

parser = argparse.ArgumentParser(description="Command line arguments")
parser.add_argument('-p',action='store', metavar='<port>', default='5000', help='The port to listen on default 5000')
args = parser.parse_args()

def dice_gen(number):
    return random.randint(1, number)

app = Flask(__name__)
@app.route('/dice/json/<int:number>', methods=['GET'])
def json_dice(number):
    response = {
        'message': "New dice roll ",
        'type': "d%s" %number,
        'result': dice_gen(number),
        'timestamp': time(),
    }
    return jsonify(response), 200

@app.route('/dice/<int:number>', methods=['GET'])
def dice(number):
    return render_template('dice.html', number=number,result=dice_gen(number))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(args.p))