import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from app.mcq_generation import MCQGenerator
from flask import render_template
from app.mcq_generation import MCQGenerator  

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

MCQ_Generator = MCQGenerator()

@app.route("/")
@cross_origin()
def hello():
    return render_template('../bitsp-projs-ui/site/app/templates/course/CourseMaterials.twig') 


@app.route("/generate", methods=["POST"])
@cross_origin()
def generate():
    try:
        request_data = request.get_json()
        context = request_data.get("context")

        if context is None:
            return jsonify({"error": "Context is required"}), 400

        count = int(request_data.get("count", 10))

        questions = MCQ_Generator.generate_mcq_questions(context, count)
        result = [question.__dict__ for question in questions]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run('localhost', 9002)
