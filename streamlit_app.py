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
            data = get_balance(api_key, api_secret)

        # 에러 처리
        if "error" in data:
            rows.append({
                "Account": acc,
                "Status": "❌ 실패",
                "Equity": None,
                "Available Balance": None,
                "Unrealized PnL": None,
                "Message": data["error"]
            })
            continue

        # =========================
        # 실제 GRVT 응답 기준 필드
        # =========================
        equity = data.get("equity")
        available = data.get("availableBalance")
        unrealized_pnl = data.get("unrealizedPnl")

        rows.append({
            "Account": acc,
            "Status": "✅ 성공",
            "Equity": equity,
            "Available Balance": available,
            "Unrealized PnL": unrealized_pnl,
            "Message": ""
        })

    df = pd.DataFrame(rows)

    st.success("✅ 조회 완료")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# =========================
# 디버그 (필드 확인용)
# =========================
with st.expander("🛠 API 응답 구조 확인 (디버그)"):
    test_acc = st.selectbox(
        "확인할 계정 선택",
        ["GR1", "GR2", "GR3", "GR4", "GR5", "GR6"]
    )

    if st.button("선택 계정 원본 응답 보기"):
        api_key = st.secrets[test_acc]["api_key"]
        api_secret = st.secrets[test_acc]["api_secret"]
        raw = get_balance(api_key, api_secret)
        st.json(raw)
