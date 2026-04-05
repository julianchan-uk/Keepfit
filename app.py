from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

# 內建一些基本食物資料庫 (每 100g)
FOOD_DB = {
    "白飯": 130, "玄米飯": 110, "雞胸肉": 165, "雞蛋": 155,
    "西蘭花": 34, "蘋果": 52, "香蕉": 89, "全脂奶": 61,
    "雲吞麵": 380, "奶茶": 40, "方包": 260
}

# 確保 data.json 存在
def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

# 1. 搜尋功能：前端輸入名稱時，後端即時回傳卡路里
@app.route('/api/search')
def search_food():
    name = request.args.get('name', '')
    calories = FOOD_DB.get(name, 0)
    return jsonify({"calories": calories})

# 2. 獲取所有紀錄
@app.route('/api/records')
def get_records():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

# 3. 新增紀錄
@app.route('/api/add', methods=['POST'])
def add_record():
    new_data = request.json
    with open(DATA_FILE, 'r+', encoding='utf-8') as f:
        records = json.load(f)
        records.append(new_data)
        f.seek(0)
        json.dump(records, f, ensure_ascii=False, indent=4)
        f.truncate()
    return jsonify({"status": "success"})

# 4. 匯出功能 (Export)
@app.route('/api/export')
def export_data():
    return send_file(DATA_FILE, as_attachment=True, download_name='my_calories.json')

# 5. 匯入功能 (Import)
@app.route('/api/import', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    file.save(DATA_FILE)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
