from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)

# 檔案路徑設定
RECORDS_FILE = 'my_records.json'
FOOD_LIBRARY_FILE = 'foods.json'

# 初始化：確保紀錄檔案存在
def init_files():
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    # 如果食物庫唔存在，整一個基本版費事報錯
    if not os.path.exists(FOOD_LIBRARY_FILE):
        default_foods = [
            {"name": "白飯 (一碗)", "cal": 260},
            {"name": "雞蛋 (一隻)", "cal": 78},
            {"name": "蘋果 (一個)", "cal": 52}
        ]
        with open(FOOD_LIBRARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_foods, f, ensure_ascii=False, indent=4)

init_files()

@app.route('/')
def index():
    return render_template('index.html')

# 1. 獲取大數據食物清單 (供前端下拉選單使用)
@app.route('/get_food_library')
def get_food_library():
    try:
        with open(FOOD_LIBRARY_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify([])

# 2. 獲取用戶自己嘅卡路里紀錄
@app.route('/get_records')
def get_records():
    with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

# 3. 新增一條紀錄
@app.route('/add_record', methods=['POST'])
def add_record():
    new_record = request.json
    with open(RECORDS_FILE, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data.append(new_record)
        f.seek(0)
        f.truncate() # 清除舊內容
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "Success"

# 4. 匯出 (Export)
@app.route('/export')
def export_data():
    return send_file(RECORDS_FILE, as_attachment
