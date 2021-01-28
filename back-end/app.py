import os
import subprocess
import sys

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from .utils import db_util

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/annotation', methods=['GET'])
def get_annotator_page():
    return render_template('annotator.html')


@app.route('/api/load_std_code_snippet', methods=['GET'])
def get_std_code_snippet():
    # TODO: Load student code from database
    # TODO: Execute code and get compiler output
    # TODO: Return the code and the compiler output to front end
    pass


@app.route('/api/get_recommendation', methods=['GET'])
def get_recommendation():
    print("Receiving Get Request")
    compiler_output = request.args.get('comp_output')
    content = request.args.get('content')
    language = request.args.get('language')
    result, question_query_time, answer_query_time = db_util.err_msg_match(compiler_output)
    print(result)
    return jsonify(query_result=result.to_json(orient='records'), question_time=question_query_time,
                   answer_time=answer_query_time)
    # return "hello world"


def code_executor(code_snippet):
    with open("main.py", 'w', encoding='utf-8') as python_file:
        python_file.write(code_snippet)
    print("Opening process")
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen([sys.executable, 'main.py'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )
    stdout, stderr = proc.communicate()

    return proc.returncode, stdout, stderr


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    app.run()
