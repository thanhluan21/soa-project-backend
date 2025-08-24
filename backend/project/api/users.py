# services/users/project/api/users.py


from sqlalchemy import exc

from flask import Blueprint, jsonify, request, render_template

from project.api.models import User
from project import db
from project.api.utils import authenticate, is_admin
from project.logger import get_logger

# Get logger for this module
logger = get_logger('users_api')


users_blueprint = Blueprint("users", __name__, template_folder="./templates")


@users_blueprint.route("/manager", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        db.session.add(User(username=username, email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template("index.html", users=users)


@users_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify({"status": "success", "message": "pong!"})


@users_blueprint.route("/", methods=["GET"])
def get_all_users():
    """Get all users"""
    logger.info("Getting all users")
    try:
        users = User.query.all()
        logger.debug(f"Found {len(users)} users")
        response_object = {
            "status": "success",
            "data": {"users": [user.to_json() for user in users]},
        }
        logger.info("Successfully retrieved all users")
        return jsonify(response_object), 200
    except Exception as e:
        logger.error(f"Error getting all users: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@users_blueprint.route("/<user_id>", methods=["GET"])
def get_single_user(user_id):
    """Get single user details"""
    logger.info(f"Getting user with ID: {user_id}")
    response_object = {"status": "fail", "message": "User does not exist"}
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            return jsonify(response_object), 404
        else:
            logger.info(f"Successfully found user: {user.username}")
            response_object = {
                "status": "success",
                "data": user.to_json(),
            }
            return jsonify(response_object), 200
    except ValueError as e:
        logger.error(f"Invalid user ID format: {user_id} - {str(e)}")
        return jsonify(response_object), 404
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@users_blueprint.route("/", methods=["POST"])
@authenticate
def add_user(resp):
    logger.info("Adding new user")
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    
    if not is_admin(resp):
        logger.warning("Non-admin user attempted to add user")
        response_object["message"] = "You do not have permission to do that."
        return jsonify(response_object), 401
        
    if not post_data:
        logger.warning("Empty payload received for add user")
        return jsonify(response_object), 400
        
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    
    logger.debug(f"Attempting to add user: {username} with email: {email}")
    
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"Successfully added user: {username} ({email})")
            response_object["status"] = "success"
            response_object["message"] = f"{email} was added!"
            response_object["data"] = new_user.to_json()
            return jsonify(response_object), 201
        else:
            logger.warning(f"Attempted to add user with existing email: {email}")
            response_object["message"] = "Sorry. That email already exists."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        logger.error(f"Database integrity error adding user {email}: {str(e)}")
        db.session.rollback()
        return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        logger.error(f"Error adding user {email}: {str(e)}")
        logger.exception("Full traceback:")
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route("/admin_create", methods=["GET","POST"])
@authenticate
def admin_create_user(resp):
    logger.info("Admin creating new user")
    post_data = request.get_json()
    response_object = {"status": "fail", "message": "Invalid payload."}
    
    if not is_admin(resp):
        logger.warning("Non-admin user attempted to admin create user")
        response_object["message"] = "You do not have permission to do that."
        return jsonify(response_object), 401
        
    if not post_data:
        logger.warning("Empty payload received for admin create user")
        return jsonify(response_object), 400
        
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    admin_flag = post_data.get("admin", False)
    active_flag = post_data.get("active", True)
    
    logger.debug(f"Attempting to admin create user: {username} with email: {email}, admin: {admin_flag}, active: {active_flag}")
    
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(username=username, email=email, password=password, admin=admin_flag)
            new_user.active = active_flag
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"Successfully admin created user: {username} ({email}), admin: {admin_flag}, active: {active_flag}")
            response_object["status"] = "success"
            response_object["message"] = f"{email} was added!"
            response_object["data"] = new_user.to_json()
            return jsonify(response_object), 201
        else:
            logger.warning(f"Attempted to admin create user with existing email: {email}")
            response_object["message"] = "Sorry. That email already exists."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        logger.error(f"Database integrity error admin creating user {email}: {str(e)}")
        db.session.rollback()
        return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        logger.error(f"Error admin creating user {email}: {str(e)}")
        logger.exception("Full traceback:")
        db.session.rollback()
        return jsonify(response_object), 400