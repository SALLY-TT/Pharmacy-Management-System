from flask import Blueprint, request, jsonify
from db import get_db_connection

drugs_bp = Blueprint("drugs", __name__)

@drugs_bp.route("/drugs", methods=["GET"])
def get_drugs():
    """
    支持分页、搜索、排序的药品列表接口
    """
    name = request.args.get("name", default="", type=str).strip().lower()
    manufacturer = request.args.get("manufacturer", default="", type=str).strip().lower()
    sort = request.args.get("sort", default="", type=str)
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=8, type=int)
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 构建 WHERE 子句
    conditions = []
    params = []

    if name:
        conditions.append("LOWER(name) LIKE %s")
        params.append(f"%{name}%")
    if manufacturer:
        conditions.append("LOWER(manufacturer) LIKE %s")
        params.append(f"%{manufacturer}%")

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT d.*, COALESCE(s.total_sold, 0) AS total_sold
        FROM drugs d
        LEFT JOIN (
            SELECT drug_id, SUM(quantity) AS total_sold
            FROM sales
            GROUP BY drug_id
        ) s ON d.drug_id = s.drug_id
        {where_clause}
    """

    cursor.execute(query, tuple(params))
    drugs = cursor.fetchall()

    # 排序
    if sort == "total_sold_desc":
        drugs.sort(key=lambda d: d["total_sold"], reverse=True)
    elif sort == "total_sold_asc":
        drugs.sort(key=lambda d: d["total_sold"])
    elif sort == "sold_since_restock_desc":
        drugs.sort(key=lambda d: d.get("sold_since_restock", 0), reverse=True)
    elif sort == "sold_since_restock_asc":
        drugs.sort(key=lambda d: d.get("sold_since_restock", 0))

    total_count = len(drugs)
    total_pages = (total_count + limit - 1) // limit

    # 分页
    drugs = drugs[offset: offset + limit]

    cursor.close()
    conn.close()

    return jsonify({
        "drugs": drugs,
        "total_pages": total_pages
    })


@drugs_bp.route("/drugs", methods=["POST"])
def add_drug():
    """
    添加药品，记录 add 类型操作日志
    """
    data = request.json
    username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 验证身份
    cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "User not found"}), 404
    if user["role"] != "manager":
        return jsonify({"message": "Unauthorized"}), 403

    name = data.get("name")
    manufacturer = data.get("manufacturer")
    price = data.get("price")
    stock = data.get("stock")
    code = data.get("code")

    if not name or price is None or stock is None:
        return jsonify({"message": "Missing fields"}), 400

    try:
        # 插入药品数据
        cursor.execute("""
            INSERT INTO drugs (name, manufacturer, price, stock, code)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, manufacturer, price, stock, code))
        # 写入操作日志
        cursor.execute("""
            INSERT INTO operation_log (username, operation_type, drug_id, drug_name, description)
            VALUES (%s, 'add', LAST_INSERT_ID(), %s, %s)
        """, (username, name, f"Added drug '{name}' with stock={stock}, price={price}"))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "DB error", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Drug added"}), 201


@drugs_bp.route("/drugs/<int:drug_id>", methods=["PUT"])
def update_drug(drug_id):
    """
    修改药品信息，记录 update 类型日志
    """
    data = request.json
    username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 验证身份
    cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "User not found"}), 404
    if user["role"] != "manager":
        return jsonify({"message": "Unauthorized"}), 403

    name = data.get("name")
    manufacturer = data.get("manufacturer")
    price = data.get("price")
    stock = data.get("stock")
    code = data.get("code")

    try:
        # 查旧值用于判断是否重置销量
        cursor.execute("SELECT price, stock FROM drugs WHERE drug_id = %s", (drug_id,))
        old = cursor.fetchone()
        reset_needed = (old["price"] != price or old["stock"] != stock)

        # 更新数据
        if reset_needed:
            cursor.execute("""
                UPDATE drugs SET
                    name = %s, manufacturer = %s, price = %s, stock = %s, code = %s,
                    sold_since_restock = 0,
                    last_updated = CURRENT_TIMESTAMP,
                    last_updated_by = %s
                WHERE drug_id = %s
            """, (name, manufacturer, price, stock, code, username, drug_id))
        else:
            cursor.execute("""
                UPDATE drugs SET
                    name = %s, manufacturer = %s, price = %s, stock = %s, code = %s,
                    last_updated = CURRENT_TIMESTAMP,
                    last_updated_by = %s
                WHERE drug_id = %s
            """, (name, manufacturer, price, stock, code, username, drug_id))

        # 插入操作日志
        cursor.execute("""
            INSERT INTO operation_log (username, operation_type, drug_id, drug_name, description)
            VALUES (%s, 'update', %s, %s, %s)
        """, (
            username, drug_id, name,
            f"Updated drug '{name}': price={price}, stock={stock}, manufacturer='{manufacturer}', code='{code}'"
        ))

        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Drug updated successfully"})


@drugs_bp.route("/drugs/<int:drug_id>", methods=["DELETE"])
def delete_drug(drug_id):
    """
    删除药品，记录 delete 类型操作日志
    """
    data = request.json
    username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 查找药品名称（后面用于写日志）
    cursor.execute("SELECT name FROM drugs WHERE drug_id = %s", (drug_id,))
    drug = cursor.fetchone()
    if not drug:
        return jsonify({"message": "Drug not found"}), 404

    # 验证权限
    cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "User not found"}), 404
    if user["role"] != "manager":
        return jsonify({"message": "Unauthorized"}), 403

    try:
        # 写入日志
        cursor.execute("""
            INSERT INTO operation_log (username, operation_type, drug_id, drug_name, description)
            VALUES (%s, 'delete', %s, %s, %s)
        """, (
            username, drug_id, drug["name"],
            f"Deleted drug '{drug['name']}' (ID={drug_id})"
        ))
        # 删除药品
        cursor.execute("DELETE FROM drugs WHERE drug_id = %s", (drug_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Drug deleted successfully"})


@drugs_bp.route("/drugs/<int:drug_id>/restock", methods=["POST"])
def restock_drug(drug_id):
    """
    补货操作，重置销量，同时记录 restock 操作日志
    """
    data = request.get_json()
    amount = data.get("amount")
    username = data.get("username")  # 从前端传入操作人

    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"message": "Invalid restock amount"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM drugs WHERE drug_id = %s", (drug_id,))
    drug = cursor.fetchone()
    if not drug:
        return jsonify({"message": "Drug not found"}), 404

    cursor.execute("""
        UPDATE drugs SET stock = stock + %s, sold_since_restock = 0
        WHERE drug_id = %s
    """, (amount, drug_id))

    cursor.execute("""
        INSERT INTO operation_log (username, operation_type, drug_id, drug_name, description)
        VALUES (%s, 'restock', %s, %s, %s)
    """, (
        username,
        drug_id,
        drug["name"],
        f"Restocked drug '{drug['name']}' by {amount}, sales reset"
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"Drug ID {drug_id} restocked, sales counter reset."})


@drugs_bp.route("/operation/logs", methods=["GET"])
def get_operation_logs():
    """
    返回所有操作日志（按时间降序）
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM operation_log ORDER BY time DESC
    """)
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(logs)
