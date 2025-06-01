from flask import Blueprint, request, jsonify
from db import get_db_connection
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, role, created_at FROM users ORDER BY role, username")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@users_bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not all([username, password, role]):
        return jsonify({"message": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({"message": "Username already exists"}), 400
    #用哈希存储密码
    hashed_pw = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, hashed_pw, role)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"User '{username}' added successfully."})

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"User ID {user_id} deleted successfully."})

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_role(user_id):
    data = request.get_json()
    new_role = data.get("role")
    if not new_role:
        return jsonify({"message": "Missing role field"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = %s WHERE user_id = %s", (new_role, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"User ID {user_id} role updated to '{new_role}'."})
