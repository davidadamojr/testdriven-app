from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.utils import authenticate
from project.api.models import Score
from project import db

scores_blueprint = Blueprint("scores", __name__)


@scores_blueprint.route("/scores", methods=["GET"])
def get_all_scores():
    scores = Score.query.all()
    response = {
        "message": "Success",
        "data": {"scores": [score.to_json() for score in scores]},
    }
    return jsonify(response), 200


@scores_blueprint.route("/scores/<user_id>", methods=["GET"])
def get_all_scores_by_user(user_id):
    scores = Score.query.filter_by(user_id=user_id).all()
    response = {
        "message": "Success",
        "data": {"scores": [score.to_json() for score in scores]},
    }
    return jsonify(response), 200


@scores_blueprint.route("/scores/user/<id>", methods=["GET"])
def get_single_score_by_user(id):
    score = Score.query.filter_by(id=id).first()
    response = {"message": "No score found with provided id.", "data": None}
    if not score:
        return jsonify(response), 404

    response["message"] = "Success"
    response["data"] = {"score": score.to_json()}
    return jsonify(response), 200


@scores_blueprint.route("/scores", methods=["POST"])
@authenticate
def add_score(auth_response):
    data = request.json
    score = Score(
        user_id=data["user_id"],
        exercise_id=data["exercise_id"],
        correct=data["correct"],
    )
    db.session.add(score)
    db.session.commit()
    response = {"message": "New score was added!", "status": "Success"}
    return jsonify(response), 201


@scores_blueprint.route("/scores/<int:exercise_id>", methods=["PUT"])
@authenticate
def update_score_by_exercise_id(auth_response, exercise_id):
    data = request.json
    try:
        score = Score.query.filter_by(exercise_id=exercise_id).first()
        if score:
            response = {"message": "Score was updated!", "status": "Success"}
            score.correct = data["correct"]
            db.session.add(score)
            db.session.commit()
            response["data"] = score.to_json()
            return jsonify(response), 200
        else:
            db.session.add(Score(user_id=auth_response['data']['id'],
                                 exercise_id=exercise_id,
                                 correct=data['correct']))
            db.session.commit()
            response = {"message": "New score was added!", "status": "Success"}
            return jsonify(response), 201
    except (exc.IntegrityError, ValueError, TypeError):
        db.session().rollback()
        return {"message": "An error occurred.", "status": "fail"}
