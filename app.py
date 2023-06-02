'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from utils import get_experience_by_index, get_education_by_index, get_skill_by_index

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''

    if request.method == 'GET':
        index = request.args.get("index")
        if index is not None:
            return get_experience_by_index(data, index)
        return jsonify(data["experience"])

    if request.method == 'POST':
        req = request.get_json()
        new = Experience(req["title"],
            req["company"],
            req["start_date"],
            req["end_date"],
            req["description"],
            req["logo"]
        )

        data["experience"].append(new)
        return jsonify({"id": data["experience"].index(new)})
    return jsonify({"Server Error": "Couldn't process method"})


@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        index = request.args.get("index")
        if index is not None:
            return get_education_by_index(data, index)
        return jsonify(data["education"])

    if request.method == 'POST':
        req = request.get_json()

        if not isinstance(req, dict):
            return jsonify({"error": "Request data is not valid JSON"}), 400

        required_fields = ["school", "start_date", "end_date", "grade", "logo"]
        missing_fields = [field for field in required_fields if field not in req]

        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Validate fields types
        if not isinstance(req["school"], str) or \
        not isinstance(req["start_date"], str) or \
        not isinstance(req["end_date"], str) or \
        not isinstance(req["grade"], str) or \
        not isinstance(req["logo"], str):
            return jsonify({"error": "Some fields have incorrect type"}), 400

        new = Education(req["course"],
            req["school"],
            req["start_date"],
            req["end_date"],
            req["grade"],
            req["logo"]
        )
        data["education"].append(new)

        return jsonify({"id": data["education"].index(new)})
    return jsonify({"Server Error": "Couldn't process method"})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        index = request.args.get("index")
        if index is not None:
            return get_skill_by_index(data, index)
        return jsonify(data["skill"])

    if request.method == 'POST':
        req = request.get_json()

        if not isinstance(req, dict):
            return jsonify({"error": "Request data is not valid JSON"}), 400

        required_fields = ["name", "proficiency", "logo"]
        missing_fields = [field for field in required_fields if field not in req]

        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Validate fields types
        if not isinstance(req["name"], str) or \
        not isinstance(req["proficiency"], str) or \
        not isinstance(req["logo"], str):
            return jsonify({"error": "Some fields have incorrect type"}), 400

        new = Skill(req["name"], req["proficiency"], req["logo"])
        data["skill"].append(new)

        return jsonify({"id": data["skill"].index(new)})
    return jsonify({"Server Error": "Couldn't process method"})
