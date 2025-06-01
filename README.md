# 💊 药房管理系统部署指南（PharmaSystem Setup Guide）

本项目为药房信息管理系统，采用前后端分离架构。后端使用 Python Flask 框架，数据库采用 MySQL。

---

## 📦 一、环境准备

### 1. 安装 Python（推荐版本 3.8 ~ 3.11）

- 下载地址：https://www.python.org/downloads/
- 安装时请务必勾选 `Add Python to PATH`

### 2. 安装 VS Code 编辑器（推荐）

- 下载地址：https://code.visualstudio.com/
- 推荐安装插件：（这些是gpt生成的，反正我记得当时我安装的时候挺简单的，没有额外单独配置啥，也可以看CSDN）
  - Python
  - Pylance
  - ESLint（前端）

### 3. 安装 MySQL 数据库（推荐 8.0）

- 下载地址：https://dev.mysql.com/downloads/installer/
- 推荐教程：https://www.bilibili.com/video/BV1Kr4y1i7ru?p=3&vd_source=97c0e0b4649623ae5b5210298d3926df（b站）
- 安装完成后设置 root 密码（推荐：`123456`）

- ✅ 推荐同时安装图形化工具：DataGrip / DBeaver / Navicat，用于管理数据库
>我用的是datagrip（免费 也挺好用的）
>推荐教程：https://www.bilibili.com/video/BV1Kr4y1i7ru?p=11&vd_source=97c0e0b4649623ae5b5210298d3926df
-
---

## 📁 二、获取项目文件

你应获得以下项目包：<br>
PharmaSystem/<br>
├── backend/ ← Flask 后端代码<br>
├── frontend/ ← 登录/销售等前端页面<br>
├── yaofangsystem.sql ← 数据库结构+数据导出文件<br>


---

## 🛠️ 三、数据库导入

### 步骤 1：创建数据库
![屏幕截图 2025-06-01 225005](https://github.com/user-attachments/assets/e158ec7b-25ca-46d8-a66f-2156770c076c)

使用 DataGrip 或命令行运行：

```sql
CREATE DATABASE yaofangsystem;
```

### 步骤 2：导入 SQL 文件
使用 DataGrip：
右键 yaofangsystem 数据库 → 把yaofang-dump.sql文件直接拖入

加载 yaofangsystem.sql → 全选点击运行 ✅

一共会有五个表格（其中user_log里面是没有数据的）

## 🐍 四、配置与运行后端（Flask）

### 1. 进入后端目录并创建虚拟环境

```bash
cd backend
python -m venv venv
```

### 2. 激活虚拟环境
```bash
.\venv\Scripts\activate
```

### 3. 安装依赖库
```bash
.pip install -r requirements.txt
```

若无 requirements.txt，可手动安装：

```bash
.pip install flask flask-cors mysql-connector-python
```

### 4. 配置数据库连接

修改 db.py 中数据库连接配置为你本地的账号和密码：（如果你跟我上面一样就不用改）

```Python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # 替换为你的用户名
        password="123456",     # 替换为你的密码
        database="yaofangsystem"
    )
```

## ✅ 步骤 5：运行后端服务
### 1. 启动 Flask 应用
![image](https://github.com/user-attachments/assets/62ad69d0-2ebe-49b5-afd8-b68537d98067)

## 🌐 步骤 6：运行前端页面
使用文件管理器打开 frontend 文件夹，找到 login.html
![d26f721636250030fad96b8bb4ad35b](https://github.com/user-attachments/assets/84e5e7ad-37d3-48cf-be09-75026e09f2c3)

