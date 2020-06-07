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
    data1, data2, data3, data4 = db_util.err_msg_match(compiler_output)
    return jsonify(question_df=data1.to_json(), question_time=data2, answer_df=data3.to_json(), answer_time=data4)
    # return "hello world"


if __name__ == '__main__':
    app.run()
