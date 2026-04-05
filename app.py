from flask import Flask, render_template, request, send_file, jsonify
import json
import os

app = Flask(__name__)

# 設定檔案路徑
RECORDS_FILE = 'my_records.json'
FOOD_LIBRARY_FILE = 'foods.json'

# --- 初始化功能：確保必要的 JSON 檔案存在 ---
def init_files():
    # 1. 確保用戶紀錄檔案存在
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    # 2. 確保食物數據庫存在，如果冇就整一個基本清單
    if not os.path.exists(FOOD_LIBRARY_FILE):
        default_foods = [
            {"name": "白飯 (一碗)", "cal": 260},
            {"name": "餐蛋麵", "cal": 680},
            {"name": "雲吞麵", "cal": 320},
            {"name": "叉燒飯", "cal": 600},
            {"name": "菠蘿包", "cal": 350},
            {"name": "燒賣 (5粒)", "cal": 210},
            {"name": "蝦餃 (4粒)", "cal": 180},
            {"name": "凍奶茶", "cal": 190},
            {"name": "雞蛋 (一隻)", "cal": 78},
            {"name": "蘋果", "cal": 52}
        ]
        with open(FOOD_LIBRARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_foods, f, ensure_ascii=False, indent=4)

# 執行初始化
init_files()

# --- 路由設定 (Routes) ---

@app.route('/')
def index():
    """顯示主網頁"""
    return render_template('index.html')

@app.route('/get_food_library')
def get_food_library():
    """回傳食物大數據清單"""
    try:
        with open(FOOD_LIBRARY_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify([])

@app.route('/get_records')
def get_records():
    """獲
