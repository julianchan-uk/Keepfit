from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)

RECORDS_FILE = 'my_records.json'
FOOD_LIBRARY_FILE = 'foods.json'

def init_files():
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    if not os.path.exists(FOOD_LIBRARY_FILE):
        default_foods = [
            {"name": "白飯 (一碗)", "cal": 260},
            {"name": "餐蛋麵", "cal": 680},
            {"name": "雲吞麵", "cal": 320},
            {"name": "叉燒飯", "cal": 600},
            {"name": "菠蘿包", "cal": 350},
            {"name": "雞蛋 (一隻)", "cal": 78},
            {"name": "蘋果", "cal": 52}
        ]
        with open(FOOD_LIBRARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_foods, f, ensure_ascii=False, indent=4)

init_files()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_food_library')
def get_food_library():
    try:
        with open(FOOD_LIBRARY_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])

@app.route('/get_records')
def get_records():
    try:
        with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])

@app.route('/add_record', methods=['POST'])
def add_record():
    new_data = request.json
    try:
        with open(RECORDS_FILE, 'r+', encoding='utf-8') as f:
            records = json.load(f)
            records.append(new_data)
            f.seek(0)
            f.truncate()
            json.dump(records, f, ensure_ascii=False, indent=4)
        return "Success", 200
    except:
        return "Error", 500

@app.route('/export')
def export_data():
    return send_file(RECORDS_FILE, as_attachment=True)

@app.route('/import', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    if file:
        try:
            content = file.read()
            json.loads(content)
            with open(RECORDS_FILE, 'wb') as f:
                f.write(content)
            return "Import Success", 200
        except:
            return "Invalid JSON", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
