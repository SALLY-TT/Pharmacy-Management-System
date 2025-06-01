from flask import Blueprint, request, jsonify
from db import get_db_connection

drugs_bp = Blueprint("drugs", __name__)

# 添加药品（仅限 manager）
@drugs_bp.route("/drugs", methods=["POST"])
def add_drug():
    data = request.json
    username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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
        cursor.execute("""
            INSERT INTO drugs (name, manufacturer, price, stock, code)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, manufacturer, price, stock, code))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "DB error", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Drug added"}), 201

# 获取药品列表 + 销量信息
@drugs_bp.route("/drugs", methods=["GET"])
def get_drugs():
    name = request.args.get("name", default="", type=str).strip().lower()
    manufacturer = request.args.get("manufacturer", default="", type=str).strip().lower()
    sort = request.args.get("sort", default="", type=str)
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=12, type=int)
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 组装 WHERE 子句
    conditions = []
    params = []

    if name:
        conditions.append("LOWER(name) LIKE %s")
        params.append(f"%{name}%")
    if manufacturer:
        conditions.append("LOWER(manufacturer) LIKE %s")
        params.append(f"%{manufacturer}%")

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    # 查询所有符合条件的药品（不分页
    query_main = f"""
        SELECT d.*, 
            COALESCE(s.total_sold, 0) AS total_sold 
        FROM drugs d
        LEFT JOIN (
            SELECT drug_id, SUM(quantity) AS total_sold
            FROM sales
            GROUP BY drug_id
        ) s ON d.drug_id = s.drug_id
        {where_clause}
    """

    cursor.execute(query_main, tuple(params))
    drugs = cursor.fetchall()

    # 收集 drug_ids
    drug_ids = tuple(d["drug_id"] for d in drugs)

    # 添加 total_sold 字段到每个药品
    for d in drugs:
        d["total_sold"] = d["total_sold"] or 0
        d["sold_since_restock"] = d["sold_since_restock"] or 0


    #  Python 中排序
    if sort == "total_sold_desc":
        drugs.sort(key=lambda x: x["total_sold"], reverse=True)
    elif sort == "total_sold_asc":
        drugs.sort(key=lambda x: x["total_sold"])
    elif sort == "sold_since_restock_desc":
        drugs.sort(key=lambda x: x["sold_since_restock"], reverse=True)
    elif sort == "sold_since_restock_asc":
        drugs.sort(key=lambda x: x["sold_since_restock"])

    # 分页（在排序后进行切片）
    total_count = len(drugs)
    total_pages = (total_count + limit - 1) // limit
    drugs = drugs[offset: offset + limit]

    cursor.close()
    conn.close()

    return jsonify({
        "drugs": drugs,
        "total_pages": total_pages
    })

# 修改药品（仅限 manager）
@drugs_bp.route("/drugs/<int:drug_id>", methods=["PUT"])
def update_drug(drug_id):
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

    # 获取新数据
    name = data.get("name")
    manufacturer = data.get("manufacturer")
    price = data.get("price")
    stock = data.get("stock")
    code = data.get("code")

    try:
        # 先查旧值
        cursor.execute("SELECT price, stock FROM drugs WHERE drug_id = %s", (drug_id,))
        old = cursor.fetchone()
        reset_needed = (old["price"] != price or old["stock"] != stock)

        if reset_needed:
            # 清空 sold_since_restock
            cursor.execute("""
                UPDATE drugs SET
                    name = %s,
                    manufacturer = %s,
                    price = %s,
                    stock = %s,
                    code = %s,
                    sold_since_restock = 0,
                    last_updated = CURRENT_TIMESTAMP,
                    last_updated_by = %s
                WHERE drug_id = %s
            """, (name, manufacturer, price, stock, code, username, drug_id))
        else:
            # 不清空
            cursor.execute("""
                UPDATE drugs SET
                    name = %s,
                    manufacturer = %s,
                    price = %s,
                    stock = %s,
                    code = %s,
                    last_updated = CURRENT_TIMESTAMP,
                    last_updated_by = %s
                WHERE drug_id = %s
            """, (name, manufacturer, price, stock, code, username, drug_id))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Update error:", e)
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Drug updated successfully"})


# 删除药品（仅限 manager）
@drugs_bp.route("/drugs/<int:drug_id>", methods=["DELETE"])
def delete_drug(drug_id):
    data = request.json
    username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "User not found"}), 404
    if user["role"] != "manager":
        return jsonify({"message": "Unauthorized"}), 403

    try:
        cursor.execute("DELETE FROM drugs WHERE drug_id = %s", (drug_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Drug deleted successfully"})

# 补货重置销量
@drugs_bp.route("/drugs/<int:drug_id>/restock", methods=["POST"])
def restock_drug(drug_id):
    data = request.get_json()
    amount = data.get("amount")

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
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"Drug ID {drug_id} restocked, sales counter reset."})
