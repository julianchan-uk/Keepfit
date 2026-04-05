from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)
RECORDS_FILE = 'my_records.json'
FOOD_DB = 'foods.json'

# 初始化紀錄檔案
if not os.path.exists(RECORDS_FILE):
    with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

# 讓網頁讀取那 200 條食物數據
@app.route('/get_food_library')
def get_food_library():
    if os.path.exists(FOOD_DB):
        with open(FOOD_DB, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

# 獲取今日已紀錄的數據
@app.route('/get_records')
def get_records():
    with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

# 新增紀錄
@app.route('/add_record', methods=['POST'])
def add_record():
    new_data = request.json
    with open(RECORDS_FILE, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data.append(new_data)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "OK"

# 匯出 (Export)
@app.route('/export')
def export_data():
    return send_file(RECORDS_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
