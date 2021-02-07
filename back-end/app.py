import os
import subprocess
import sys,codecs

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from .annotation_service import AnnotationService
from .utils import db_util
from .vector_matcher import VectorMatcher


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
annotation_service = AnnotationService()
vector_matcher = VectorMatcher()


@app.route('/annotation', methods=['GET'])
def get_annotator_page():
    return render_template('annotator.html')


@app.route('/api/load_std_code_snippet', methods=['GET'])
def get_std_code_snippet():
    err_type = request.args.get('err_type')
    print('****************************')
    if err_type == 'random' or err_type == '':
        err_type = 'SyntaxError'
    code_id, code_snippet = annotation_service.load_historical_code(err_type)
    code_snippet = codecs.escape_decode(bytes(code_snippet[1:-2], "utf-8"))[0].decode("utf-8")
    return_code, err_msg = code_executor(code_snippet)
    return jsonify(code_id=code_id, code_snippet=code_snippet, err_msg=err_msg.decode('utf-8'))


@app.route('/api/get_recommendation', methods=['GET'])
def get_recommendation():
    print("Receiving Get Request")
    compiler_output = request.args.get('comp_output')
    content = request.args.get('content')
    language = request.args.get('language')
    print('----------------------------------')
    ids = vector_matcher.solution_finder(compiler_output,content,0.002,5,0.001,20)
    print(len(ids))
    questions_info,answers = vector_matcher.solution_loader(ids)
    print(questions_info)
    print(answers)
    matching_response = annotation_service.response_builder(questions_info,answers)
    result, question_query_time, answer_query_time = db_util.err_msg_match(compiler_output)
    print(result)
    print(matching_response)
    return jsonify(query_result=result.to_json(orient='records'), question_time=question_query_time,
                   answer_time=answer_query_time,matching_response=matching_response)
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
    print(stdout,stderr)

    return proc.returncode, stdout


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    app.run(debug=False)
