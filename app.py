from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)

# 紀錄檔案路徑
DATA_FILE = 'my_records.json'

# 確保紀錄檔案存在
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

# 獲取已儲存的紀錄
@app.route('/get_records')
def get_records():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

# 新增一條紀錄
@app.route('/add_record', methods=['POST'])
def add_record():
    record = request.json
    with open(DATA_FILE, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data.append(record)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "OK"

# 匯出檔案
@app.route('/export')
def export_data():
    return send_file(DATA_FILE, as_attachment=True)

if __name__ == '__main__':
    # 執行 App
    app.run(debug=True, port=5000)
