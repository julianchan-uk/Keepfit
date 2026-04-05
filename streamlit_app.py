import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 基本設定
st.set_page_config(page_title="Julian's KeepFit", layout="centered")

if 'records' not in st.session_state:
    st.session_state.records = []

st.title("🍎 卡路里紀錄儀")

# 2. 側邊欄 - 匯入與匯出 (包好 try-except 防止報錯)
with st.sidebar:
    st.header("數據管理")
    
    # 匯出 CSV
    if st.session_state.records:
        df_export = pd.DataFrame(st.session_state.records)
        csv = df_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 匯出 CSV 備份", data=csv, file_name="calories.csv", mime="text/csv")
    
    # 匯入 CSV
    uploaded_file = st.file_uploader("📤 匯入 CSV 檔案", type="csv")
    if uploaded_file is not None:
        try:
            imported_df = pd.read_csv(uploaded_file)
            st.session_state.records = imported_df.to_dict('records')
            st.success("匯入成功！")
            st.rerun()
        except Exception as e:
            st.error(f"檔案出錯: {e}")

# 3. 新增紀錄表單
with st.form("input_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    food = col1.text_input("食物名稱")
    cal = col2.number_input("卡路里", min_value=0, step=1)
    if st.form_submit_button("新增"):
        if food:
            st.session_state.records.append({
                "日期": datetime.now().strftime("%Y-%m-%d"),
                "食物": food,
                "卡路里": cal
            })
            st.rerun()

# 4. 顯示數據
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.metric("今日總計", f"{df['卡路里'].sum()} kcal")
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index('食物')['卡路里'])
    
    if st.button("🗑️ 清空紀錄"):
        st.session_state.records = []
        st.rerun()
else:
    st.info("仲未有紀錄，入啲嘢食試吓啦！")
