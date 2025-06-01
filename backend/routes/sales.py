from flask import Blueprint, request, jsonify
from db import get_db_connection
from datetime import datetime,timedelta
import mysql.connector  
import pytz

sales_bp = Blueprint("sales", __name__)


@sales_bp.route("/sales", methods=["POST"])
def sell_drug():
    data_list = request.get_json()
    if not isinstance(data_list, list):
        return jsonify({"message": "Expected a list of items"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    error_messages = []
    
    try:
        conn.start_transaction()

        for data in data_list:
            drug_id = data.get("drug_id")
            quantity = int(data.get("quantity"))
            seller_username = data.get("seller_username")

            # 获取当前北京时间并格式化为字符串
            beijing_tz = pytz.timezone("Asia/Shanghai")
            sale_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
            
            # 查用户
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (seller_username,))
            user = cursor.fetchone()
            if not user:
                error_messages.append(f"Seller {seller_username} not found")
                continue
            seller_id = user["user_id"]

            # 查药品
            cursor.execute("SELECT * FROM drugs WHERE drug_id = %s", (drug_id,))
            drug = cursor.fetchone()
            if not drug:
                error_messages.append(f"Drug ID {drug_id} not found")
                continue

            if drug["stock"] < quantity:
                error_messages.append(f"Insufficient stock for drug ID {drug_id}")
                continue

            # 插入销售记录
            cursor.execute(
                "INSERT INTO sales (drug_id, seller_id, quantity, sale_time) VALUES (%s, %s, %s, %s)",
                (drug_id, seller_id, quantity,sale_time)
            )

            # 更新库存、销量
            cursor.execute(
                "UPDATE drugs SET stock = stock - %s, total_sold = total_sold + %s, sold_since_restock = sold_since_restock + %s WHERE drug_id = %s",
                (quantity, quantity, quantity, drug_id)
            )

            # 更新销售额
            total_price = quantity * float(drug["price"])
            cursor.execute(
                "UPDATE users SET total_sales_amount = total_sales_amount + %s WHERE user_id = %s",
                (total_price, seller_id)
            )
            # 插入日志记录
            cursor.execute("""
                INSERT INTO sales_log 
                (drug_id, drug_name, manufacturer, price, quantity, total_price, sale_time)
                SELECT d.drug_id, d.name, d.manufacturer, d.price, %s, %s, %s
                FROM drugs d WHERE d.drug_id = %s
            """, (quantity, total_price, sale_time, drug_id))



        conn.commit()
        if error_messages:
            return jsonify({"message": "Some sales failed", "errors": error_messages}), 207
        else:
            return jsonify({"message": "All sales recorded successfully"}), 200
        
    except mysql.connector.Error as e:
        conn.rollback()
        print("Transaction error:", e)
        return jsonify({"message": "Transaction failed.", "error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# 查询销售日志接口
@sales_bp.route("/sales/logs", methods=["GET"])
def get_sales_logs():
    name = request.args.get("name", "")
    manufacturer = request.args.get("manufacturer", "")
    start = request.args.get("start_date", "")
    end = request.args.get("end_date", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM sales_log WHERE 1=1"
    params = []

    #在sql里面新增筛选条件
    if name:
        query += " AND LOWER(drug_name) LIKE %s"
        params.append(f"%{name.lower()}%")      #%{name}% 表示模糊查询
    if manufacturer:
        query += " AND LOWER(manufacturer) LIKE %s"
        params.append(f"%{manufacturer.lower()}%")
    if start:
        query += " AND sale_time >= %s"
        params.append(start)
    if end:
        query += " AND sale_time <= %s"
        params.append(end)

    cursor.execute(query, tuple(params))
    logs = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(logs)
