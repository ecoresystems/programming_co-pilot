from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from .utils import db_util
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/get_recommendation', methods=['GET'])
def hello_world():
    print("Receiving Get Request")
    compiler_output = request.args.get('comp_output')
    content = request.args.get('content')
    language = request.args.get('language')
    result, question_query_time, answer_query_time = db_util.err_msg_match(compiler_output)
    return jsonify(query_result=result.to_json(), question_time=question_query_time, answer_time=answer_query_time)
    # return "hello world"


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    app.run()


