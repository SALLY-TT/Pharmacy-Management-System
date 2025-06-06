from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection
from routes.drugs import drugs_bp
from routes.sales import sales_bp
from routes.users import users_bp
from routes.report import report_bp
from werkzeug.security import check_password_hash
import hashlib
import re
from OpenSSL import crypto  # 需要安装pyopenssl
from flask import send_file

import os

app = Flask(__name__)
CORS(app)

# 配置证书路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CERT_DIR = os.path.join(BASE_DIR, 'certs', 'admin')
ADMIN_CERT_PATH = os.path.join(CERT_DIR, 'cert.pem')

# 注册蓝图
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

    if not user:
        return jsonify({"message": "Invalid username"}), 401

    stored_password = user["password"]
    if check_password_hash(stored_password, password) or stored_password == password:
        return jsonify({
            "message": "Login successful",
            "username": username,
            "role": user["role"]
        })
    else:
        return jsonify({"message": "Invalid password"}), 401


# 修改verify_certificate函数
@app.route("/verify_cert", methods=["POST"])
def verify_certificate():
    data = request.json
    username = data.get("username")
    client_cert_pem = data.get("certificate", "").strip()

    # 获取用户信息包括证书指纹
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT role, cert_fingerprint FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or user["role"] != "admin":
        return jsonify({"verified": False, "message": "User not authorized"}), 403

    # 如果没有证书指纹，说明该管理员未分配证书
    if not user.get("cert_fingerprint"):
        return jsonify({"verified": False, "message": "No certificate registered for this admin"}), 403

    try:
        # 计算上传证书的指纹
        def calc_cert_fingerprint(cert_pem):
            """计算证书的SHA256指纹"""
            # 清理PEM格式
            cert_clean = re.sub(r'-----(BEGIN|END) CERTIFICATE-----|\s', '', cert_pem)
            # Base64解码
            import base64
            cert_der = base64.b64decode(cert_clean)
            # 计算SHA256
            return hashlib.sha256(cert_der).hexdigest().lower()

        client_fp = calc_cert_fingerprint(client_cert_pem)
        stored_fp = user["cert_fingerprint"].lower()

        if client_fp == stored_fp:
            return jsonify({"verified": True})
        else:
            return jsonify({
                "verified": False,
                "message": "Certificate does not match this admin account"
            }), 401

    except Exception as e:
        app.logger.error(f"Certificate verification error: {str(e)}", exc_info=True)
        return jsonify({
            "verified": False,
            "message": f"Certificate processing error: {str(e)}"
        }), 500


from werkzeug.utils import secure_filename
from pathlib import Path


# 证书下载路由
@app.route("/certs/<username>/<filename>")
def download_cert(username, filename):
    """提供证书下载功能"""
    try:
        # 构建安全的文件路径
        cert_dir = Path(app.config["CERT_DIR"]) / secure_filename(username)
        cert_path = cert_dir / secure_filename(filename)

        # 检查文件是否存在
        if not cert_path.exists():
            app.logger.error(f"证书文件不存在: {cert_path}")
            return jsonify({"error": "File not found"}), 404

        # 返回文件下载
        return send_file(
            cert_path,
            as_attachment=True,
            download_name=f"{username}_certificate.pem",
            mimetype="application/x-pem-file"
        )

    except Exception as e:
        app.logger.error(f"证书下载错误: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to download certificate"}), 500

if __name__ == "__main__":
    if not os.path.exists(CERT_DIR):
        os.makedirs(CERT_DIR)
    app.run(host="127.0.0.1", port=5000, debug=True)

