from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'my_records.json'
LIB_FILE = 'foods.json'

# 初始化紀錄檔
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

# 🔍 搜尋食物庫
@app.route('/search_lib')
def search_lib():
    q = request.args.get('q', '').lower()
    if not os.path.exists(LIB_FILE):
        return jsonify([])
    with open(LIB_FILE, 'r', encoding='utf-8') as f:
        library = json.load(f)
    # 搵出符合關鍵字嘅食物 (頭 10 個)
    matches = [i for i in library if q in i['name'].lower()]
    return jsonify(matches[:10])

@app.route('/get_records')
def get_records():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/add_record', methods=['POST'])
def add_record():
    new_data = request.json
    with open(DATA_FILE, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data.append(new_data)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "OK"

@app.route('/export')
def export():
    return send_file(DATA_FILE, as_attachment=True)

@app.route('/import', methods=['POST'])
def import_data():
    file = request.files['file']
    if file:
        file.save(DATA_FILE)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
