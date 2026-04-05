from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)

# 檔案名稱定義
DATA_FILE = 'my_records.json'   # 儲存你每日食咗乜
FOOD_DB = 'foods.json'         # 你啱啱更新咗嗰個 200 條數據嘅檔案

# 初始化：確保紀錄檔存在
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

# API: 讀取食物資料庫供前端選單使用
@app.route('/get_food_library')
def get_food_library():
    try:
        with open(FOOD_DB, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: 獲取已儲存的紀錄
@app.route('/get_records')
def get_records():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

# API: 新增一筆紀錄
@app.route('/add_record', methods=['POST'])
def add_record():
    record = request.json
    with open(DATA_FILE, 'r+', encoding='utf-8') as f:
        data = json.json.load(f)
        data.append(record)
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "OK"

# API: 匯出紀錄 (Download)
@app.route('/export')
def export_data():
    return send_file(DATA_FILE, as_attachment=True)

# API: 匯入紀錄 (Upload)
@app.route('/import', methods=['POST'])
def import_data():
    file = request.files['file']
    if file:
        file.save(DATA_FILE)
    return "Success"

if __name__ == '__main__':
    # 執行程式
    app.run(debug=True, port=5000)
