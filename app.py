from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'my_calories.json'

# 模擬一些基本食物數據（之後可以改為讀取更大型的 CSV 或 API）
COMMON_FOODS = {
    "白飯": 130,
    "雞胸肉": 165,
    "雞蛋": 155,
    "蘋果": 52,
    "香蕉": 89,
    "西蘭花": 34,
    "奶茶": 40
}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

# 搜尋基本食物資料
@app.route('/search_food')
def search_food():
    query = request.args.get('q', '')
    # 簡單過濾建議
    results = {name: cal for name, cal in COMMON_FOODS.items() if query in name}
    return jsonify(results)

@app.route('/get_records')
def get_records():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/add_record', methods=['POST'])
def add_record():
    record = request.json
    with open(DATA_FILE, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data.append(record)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "OK"

@app.route('/export')
def export_data():
    return send_file(DATA_FILE, as_attachment=True)

@app.route('/import', methods=['POST'])
def import_data():
    file = request.files['file']
    if file:
        content = file.read()
        with open(DATA_FILE, 'wb') as f:
            f.write(content)
    return "Import Success"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
