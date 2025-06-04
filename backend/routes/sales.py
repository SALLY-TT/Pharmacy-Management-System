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
                (drug_id, drug_name, manufacturer, price, quantity, sale_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                drug["drug_id"],
                drug["name"],
                drug["manufacturer"],
                drug["price"],
                quantity,
                sale_time
            ))


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
    # 获取前端传来的查询参数
    name = request.args.get("name", "")
    manufacturer = request.args.get("manufacturer", "")
    start = request.args.get("start_date", "")
    end = request.args.get("end_date", "")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 8))
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 构建基础 SQL 查询语句（WHERE 1=1 方便追加条件）
    base_condition = "FROM sales_log WHERE 1=1"
    filters = []
    params = []

    # 模糊搜索药品名称（不区分大小写）
    if name:
        filters.append("AND LOWER(drug_name) LIKE %s")
        params.append(f"%{name.lower()}%")

    # 模糊搜索厂家（不区分大小写）
    if manufacturer:
        filters.append("AND LOWER(manufacturer) LIKE %s")
        params.append(f"%{manufacturer.lower()}%")

    # 起始日期（包含当天）
    if start:
        filters.append("AND DATE(sale_time) >= %s")
        params.append(start)

    # 截止日期（包含当天）
    if end:
        filters.append("AND DATE(sale_time) <= %s")
        params.append(end)

    filter_clause = " ".join(filters)

    # 1. 获取分页数据（默认按销售时间倒序）
    data_query = f"SELECT * {base_condition} {filter_clause} ORDER BY sale_time DESC LIMIT %s OFFSET %s"
    cursor.execute(data_query, (*params, limit, offset))
    logs = cursor.fetchall()

    # 2. 获取总记录数（用于计算总页数）
    count_query = f"SELECT COUNT(*) as total {base_condition} {filter_clause}"
    cursor.execute(count_query, tuple(params))
    total = cursor.fetchone()["total"]

    # 3. 获取总销量与总金额（用于底部统计）
    stats_query = f"SELECT SUM(quantity) as total_items, SUM(total_price) as total_amount {base_condition} {filter_clause}"
    cursor.execute(stats_query, tuple(params))
    stats = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({
        "logs": logs,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
        "stats": stats
    })
