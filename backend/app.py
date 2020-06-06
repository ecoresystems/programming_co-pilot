from flask import Flask, request, jsonify
from utilities import db_util
import json

app = Flask(__name__)


@app.route('/api/get_recommendation', methods=['GET'])
def hello_world():
    # compiler_output = request.args.get('comp_output')
    # content = request.args.get('content')
    # language = request.args.get('language')
    json_file = open("sample_data.json",'r')
    for row in json.load(json_file):
        compiler_output = row['comp_output']
        data1, data2, data3, data4 = db_util.err_msg_match(compiler_output)
    return jsonify(content=data2, d4=data4)
    # return "hello world"


if __name__ == '__main__':
    app.run()
