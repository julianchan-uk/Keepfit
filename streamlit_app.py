import streamlit as st
import pandas as pd
import json
from datetime import datetime

# 設定網頁標題
st.set_page_config(page_title="Julian's Calorie Tracker", layout="centered")

st.title("🍎 卡路里紀錄儀 (Streamlit 版)")

# 初始化 Session State (用嚟暫存數據，費事重新整理就消失)
if 'records' not in st.session_state:
    st.session_state.records = []

# --- 側邊欄：匯入 / 匯出 ---
st.sidebar.header("數據管理")

# 匯出功能
if st.session_state.records:
    df_export = pd.DataFrame(st.session_state.records)
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 匯出 CSV 備份",
        data=csv,
        file_name=f"calories_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )

# 匯入功能
uploaded_file = st.sidebar.file_input("📤 匯入 CSV 檔案", type="csv")
if uploaded_file is not None:
    imported_df = pd.read_csv(uploaded_file)
    st.session_state.records = imported_df.to_dict('records')
    st.sidebar.success("匯入成功！")

# --- 主要介面：新增紀錄 ---
with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        food = st.text_input("食物名稱", placeholder="例如：雞胸肉")
    with col2:
        cal = st.number_input("卡路里 (kcal)", min_value=0, step=1)
    
    submit = st.form_submit_button("新增紀錄")
    if submit and food:
        new_record = {"時間": datetime.now().strftime("%H:%M"), "食物": food, "卡路里": cal}
        st.session_state.records.append(new_record)
        st.rerun()

# --- 顯示數據 ---
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    
    # 顯示總計數值
    total_cal = df['卡路里'].sum()
    st.metric(label="今日總攝取", value=f"{total_cal} kcal")
    
    # 顯示表格
    st.subheader("今日清單")
    st.dataframe(df, use_container_width=True)

    # 簡單圖表分析
    st.subheader("比例分析")
    st.bar_chart(df.set_index('食物')['卡路里'])

    if st.button("🗑️ 清空所有紀錄"):
        st.session_state.records = []
        st.rerun()
else:
    st.info("目前仲未有紀錄，開始輸入你第一餐啦！")

st.divider()
st.caption("Developed by julianchan-uk | Powered by Streamlit")
