# services/project/api.py


from sqlalchemy import exc
from flask import Blueprint, jsonify, request

from project import db
from project.api.models import Score
from project.api.utils import authenticate


scores_blueprint = Blueprint("scores", __name__)


@scores_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify({"status": "success", "message": "pong!"})


@scores_blueprint.route("/", methods=["GET"])
def get_all_scores():
    """Get all scores"""
    response_object = {
        "status": "success",
        "data": {"scores": [ex.to_json() for ex in Score.query.all()]},
    }
    return jsonify(response_object), 200


@scores_blueprint.route("/user", methods=["GET"])
@authenticate
def get_all_scores_by_user_user(resp):
    """Get all scores by user id"""
    scores = Score.query.filter_by(user_id=int(resp)).all()
    response_object = {
        "status": "success",
        "data": {"scores": [ex.to_json() for ex in scores]},
    }
    return jsonify(response_object), 200


@scores_blueprint.route("/user/<score_id>", methods=["GET"])
@authenticate
def get_single_score_by_user_id(resp, score_id):
    """Get single score by user id"""
    response_object = {"status": "fail", "message": "Score does not exist"}
    try:
        score = Score.query.filter_by(id=int(score_id), user_id=int(resp)).first()
        if not score:
            return jsonify(response_object), 404
        else:
            response_object = {"status": "success", "data": score.to_json()}
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@scores_blueprint.route("/", methods=["POST"])
@authenticate
def add_scores(resp):
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    if not post_data:
        return jsonify(response_object), 400
    exercise_id = post_data.get("exercise_id")
    answer = post_data.get("answer")
    results = post_data.get("results")
    user_results = post_data.get("user_results")
    try:
        score = Score(
            user_id=int(resp),
            exercise_id=exercise_id,
            answer=answer,
            results=results,
            user_results=user_results,
        )
        db.session.add(score)
        db.session.commit()
        response_object["status"] = "success"
        response_object["message"] = "New score was added!"
        response_object["data"] = score.to_json()
        return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400


@scores_blueprint.route("/<exercise_id>", methods=["PUT"])
@authenticate
def update_score(resp, exercise_id):
    """Update score"""
    response_object = {"status": "fail", "message": "Invalid payload."}

    try:
        post_data = request.json  # Thay get_json() bằng json để force parse
        if not post_data:
            return jsonify(response_object), 400

        answer = post_data.get("answer")
        results = post_data.get("results")
        user_results = post_data.get("user_results")
        if answer is None and results is None and user_results is None:
            response_object["message"] = "No fields to update in payload!"
            return jsonify(response_object), 400

        score = Score.query.filter_by(
            exercise_id=int(exercise_id), user_id=int(resp)
        ).first()
        if score:
            if answer is not None:
                score.answer = answer
            if results is not None:
                score.results = results
            if user_results is not None:
                score.user_results = user_results
            db.session.commit()
            response_object["status"] = "success"
            response_object["message"] = "Score was updated!"
            response_object["data"] = score.to_json()
            return jsonify(response_object), 200
        else:
            response_object["message"] = "Sorry. That score does not exist."
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError, TypeError) as e:
        db.session.rollback()
        response_object["message"] = (
            f"Error: {str(e)} {post_data} {exercise_id}, Error!"
        )
        return jsonify(response_object), 400
    except Exception as e:  # Bắt lỗi parse JSON nếu fail
        response_object["message"] = f"Parse JSON fail: {str(e)}, Error!"
        return jsonify(response_object), 400