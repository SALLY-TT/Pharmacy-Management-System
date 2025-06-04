from flask import Blueprint, request, jsonify
from db import get_db_connection

report_bp = Blueprint("report", __name__)

@report_bp.route("/sales/report", methods=["GET"])
def sales_report():
    username = request.args.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 获取用户ID
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_id = user["user_id"]

    # 查询销售记录（关联药品名）
    cursor.execute("""
        SELECT 
            s.drug_id,
            d.name AS drug_name,
            d.manufacturer AS drug_manufacturer,
            s.quantity,
            d.price,
            (d.price * s.quantity) AS total_price, 
            s.sale_time
        FROM sales s
        JOIN drugs d ON s.drug_id = d.drug_id
        WHERE s.seller_id = %s
        ORDER BY s.sale_time DESC
    """, (user_id,))
    sales = cursor.fetchall()

    # 计算总销售额
    total = sum(s["quantity"] * float(s["price"]) for s in sales)

    conn.close()

    return jsonify({
        "sales": sales,
        "total_sales": round(total, 2)
    })
