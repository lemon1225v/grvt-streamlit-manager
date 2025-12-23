import streamlit as st
import requests
import pandas as pd

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="GRVT Multi-Account Manager",
    layout="wide"
)

st.title("📊 GRVT GR1 ~ GR6 잔고 대시보드")

# =========================
# GRVT API 함수
# =========================
def get_balance(api_key, api_secret):
    """
    GRVT 계정 잔고 조회
    """
    url = "https://api.grvt.io/v1/account/balance"
    headers = {
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# =========================
# 메인 UI
# =========================
st.subheader("🔎 전체 계정 잔고 요약")

if st.button("모든 계정 잔고 조회"):
    rows = []

    for acc in ["GR1", "GR2", "GR3", "GR4", "GR5", "GR6"]:
        api_key = st.secrets[acc]["api_key"]
        api_secret = st.secrets[acc]["api_secret"]

        with st.spinner(f"{acc} 조회 중..."):
            data = get_balance(api_key, a
