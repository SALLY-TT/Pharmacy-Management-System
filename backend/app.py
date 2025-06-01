from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection
from routes.drugs import drugs_bp
from routes.sales import sales_bp
from routes.users import users_bp
from routes.report import report_bp
from werkzeug.security import check_password_hash

app = Flask(__name__)

#  正确配置 CORS：允许来自 5500 端口的前端访问
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

#  注册蓝图
app.register_blueprint(drugs_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(users_bp)
app.register_blueprint(report_bp)

@app.route("/")
def home():
    return "Pharmacy Management System Backend is running."

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    stored_password = user["password"]
    #  支持两种情况：哈希密码 和 明文密码
    if check_password_hash(stored_password, password) or stored_password == password:
        return jsonify({"message": "Login successful", "username": username, "role": user["role"]})
    else:
        return jsonify({"message": "Invalid password"}), 401

if __name__ == "__main__":
    # 监听 127.0.0.1:5000，调试模式开启
    app.run(host="127.0.0.1", port=5000, debug=True)
