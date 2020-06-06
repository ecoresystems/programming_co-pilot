from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .utils import db_util
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/get_recommendation', methods=['GET'])
def hello_world():
    compiler_output = request.args.get('comp_output')
    content = request.args.get('content')
    language = request.args.get('language')
    # json_file = open("sample_data.json",'r')
    # for row in json.load(json_file):
    #     compiler_output = row['comp_output']
    #     data1, data2, data3, data4 = db_util.err_msg_match(compiler_output)
    return jsonify(content=compiler_output, d4=content)
    # return "hello world"


if __name__ == '__main__':
    app.run()
