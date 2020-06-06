from flask import Flask, request,jsonify

app = Flask(__name__)


@app.route('/api/get_recommendation', methods=['GET'])
def hello_world():
    compiler_output = request.args.get('comp_output')
    content = request.args.get('content')
    language = request.args.get('language')
    return jsonify(compiler_output=compiler_output,content= content, language=language)
    # return "hello world"


if __name__ == '__main__':
    app.run()
