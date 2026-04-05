import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. 網頁基本設定
st.set_page_config(
    page_title="Julian's Calorie Tracker",
    page_icon="🍎",
    layout="centered"
)

# 自定義 CSS 令介面更美觀
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_value=True)

st.title("🍎 卡路里紀錄儀 (Streamlit 版)")

# 2. 初始化數據儲存 (Session State)
if 'records' not in st.session_state:
    st.session_state.records = []

# --- 側邊欄：數據管理 (Import/Export) ---
with st.sidebar:
    st.header("⚙️ 數據管理")
    
    # 匯出功能 (Export)
    if st.session_state.records:
        df_for_export = pd.DataFrame(st.session_state.records)
        csv_data = df_for_export.to_csv(index=False).encode('utf-8-sig') # 支援中文
        
        st.download_button(
            label="📥 匯出 CSV 備份",
            data=csv_data,
            file_name=f"calories_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )
    else:
        st.write("暫時冇數據可以匯出")

    st.divider()

    # 匯入功能 (Import) - 修正後的正確 Function: file_uploader
    uploaded_file = st.file_uploader("📤 匯入 CSV 檔案", type="csv")
    
    if uploaded_file is not None:
        try:
            # 讀取上傳的 CSV
            imported_df = pd.read_csv(uploaded_file)
            #
