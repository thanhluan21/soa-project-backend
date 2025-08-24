# services/project/api.py

from sqlalchemy import exc
from flask import Blueprint, jsonify, request

from project import db
from project.api.models import Exercise, User  # Assuming User model exists
from project.api.utils import authenticate

exercises_blueprint = Blueprint("exercises", __name__)

@exercises_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify({"status": "success", "message": "pong!"})

@exercises_blueprint.route("/", methods=["GET"])
def get_all_exercises():
    """Get all exercises"""
    response_object = {
        "status": "success",
        "data": {"exercises": [ex.to_json() for ex in Exercise.query.all()]},
    }
    return jsonify(response_object), 200

@exercises_blueprint.route("/<exercise_id>", methods=["GET"])
def get_single_exercise(exercise_id):
    """Get single exercise"""
    response_object = {"status": "fail", "message": "Exercise does not exist"}
    try:
        exercise = Exercise.query.filter_by(id=int(exercise_id)).first()
        if not exercise:
            return jsonify(response_object), 404
        else:
            response_object = {"status": "success", "data": exercise.to_json()}
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@exercises_blueprint.route("/validate_code", methods=["POST"])
def validate_code():
    data = request.get_json()
    if not data or "answer" not in data or "exercise_id" not in data:
        return (
            jsonify({"status": "fail", "message": "Invalid data!"}),
            400,
        )

    answer = data["answer"]
    exercise_id = data["exercise_id"]

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return (
            jsonify({"status": "fail", "message": "Exercise not found!"}),
            404,
        )

    tests = exercise.test_cases
    solutions = exercise.solutions

    if len(tests) != len(solutions):
        return (
            jsonify(
                {"status": "fail", "message": "Tests and solutions length mismatch!"}
            ),
            500,
        )

    results = []
    user_results = []

    namespace = {}
    try:
        exec(answer, namespace)
    except Exception as e:
        return (
            jsonify(
                {"status": "fail", "message": f"Code compilation failed: {str(e)}!"}
            ),
            400,
        )

    for test, sol in zip(tests, solutions):
        try:
            res = eval(test, namespace)
            user_str = str(res)
            user_results.append(user_str)
            results.append(user_str == sol)
        except Exception as e:
            user_results.append(f"Error: {str(e)}")
            results.append(False)

    return (
        jsonify(
            {
                "status": "success",
                "results": results,
                "user_results": user_results,
                "all_correct": all(results),
            }
        ),
        200,
    )

@exercises_blueprint.route("/", methods=["POST"])
@authenticate
def add_exercise(user_id):
    """Add exercise"""
    user = User.query.get(user_id)
    if not user:
        response_object = {
            "status": "error",
            "message": "User not found.",
        }
        return jsonify(response_object), 404
    if not user.admin:  # Assuming 'admin' is a boolean field on User model
        response_object = {
            "status": "error",
            "message": "You do not have permission to do that.",
        }
        return jsonify(response_object), 401
    
    post_data = request.get_json()
    if not post_data:
        response_object = {"status": "fail", "message": "Invalid payload."}
        return jsonify(response_object), 400
    title = post_data.get("title")
    body = post_data.get("body")
    difficulty = post_data.get("difficulty")
    test_cases = post_data.get("test_cases")
    solutions = post_data.get("solutions")
    try:
        exercise = Exercise(
            title=title,
            body=body,
            difficulty=difficulty,
            test_cases=test_cases,
            solutions=solutions,
        )
        db.session.add(exercise)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "New exercise was added!",
            "data": exercise.to_json(),
        }
        return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object = {"status": "fail", "message": "Invalid payload."}
        return jsonify(response_object), 400

@exercises_blueprint.route("/<exercise_id>", methods=["PUT"])
@authenticate
def update_exercise(user_id, exercise_id):
    """Update exercise"""
    user = User.query.get(user_id)
    if not user:
        response_object = {
            "status": "error",
            "message": "User not found.",
        }
        return jsonify(response_object), 404
    if not user.admin:  # Assuming 'admin' is a boolean field on User model
        response_object = {
            "status": "error",
            "message": "You do not have permission to do that.",
        }
        return jsonify(response_object), 401

    response_object = {"status": "fail", "message": "Invalid payload."}

    try:
        post_data = request.json
        if not post_data:
            return jsonify(response_object), 400

        title = post_data.get("title")
        body = post_data.get("body")
        difficulty = post_data.get("difficulty")
        test_cases = post_data.get("test_cases")
        solutions = post_data.get("solutions")

        if all(x is None for x in [title, body, difficulty, test_cases, solutions]):
            response_object["message"] = "No fields to update in payload!"
            return jsonify(response_object), 400

        exercise = Exercise.query.filter_by(id=int(exercise_id)).first()
        if exercise:
            if title is not None:
                exercise.title = title
            if body is not None:
                exercise.body = body
            if difficulty is not None:
                exercise.difficulty = difficulty
            if test_cases is not None:
                exercise.test_cases = test_cases
            if solutions is not None:
                exercise.solutions = solutions
            db.session.commit()
            response_object["status"] = "success"
            response_object["message"] = "Exercise was updated!"
            response_object["data"] = exercise.to_json()
            return jsonify(response_object), 200
        else:
            response_object["message"] = "Sorry. That exercise does not exist."
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError, TypeError) as e:
        db.session.rollback()
        response_object["message"] = f"Error: {str(e)}"
        return jsonify(response_object), 400
    except Exception as e:  # Bắt lỗi parse JSON nếu fail
        response_object["message"] = f"Parse JSON fail: {str(e)}, Error!"
        return jsonify(response_object), 400