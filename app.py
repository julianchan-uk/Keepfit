# 喺 app.py 加入呢段
FOOD_DATABASE = {
    "雞蛋": 155,
    "白飯": 130,
    "雞胸肉": 165,
    "西蘭花": 34,
    "蘋果": 52
}

@app.route('/get_calories')
def get_calories():
    food_name = request.args.get('name')
    # 喺資料庫搵，搵唔到就回傳 0
    calories = FOOD_DATABASE.get(food_name, 0)
    return {"calories": calories}
