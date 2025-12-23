import streamlit as st
import requests
import pandas as pd

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="GRVT GR1 ~ GR6 잔고 대시보드",
    layout="wide"
)

st.title("📊 GRVT GR1 ~ GR6 잔고 대시보드")

AUTH_URL = "https://edge.grvt.io/auth/api_key/login"
BALANCE_URL = "https://edge.grvt.io/api/account/balance"

# =========================
# GRVT 인증
# =========================
def authenticate(api_key):
    headers = {
        "Content-Type": "application/json",
        "Cookie": "rm=true;"
    }
    payload = {
        "api_key": api_key
    }

    r = requests.post(AUTH_URL, headers=headers, json=payload, timeout=10)

    if r.status_code != 200:
        return None, None, f"Auth failed: {r.text}"

    cookie = r.headers.get("Set-Cookie")
    account_id = r.headers.get("X-Grvt-Account-Id")

    return cookie, account_id, None


# =========================
# 잔고 조회
# =========================
def get_balance(cookie, account_id):
    headers = {
        "Cookie": cookie,
        "X-Grvt-Account-Id": account_id
    }

    r = requests.get(BALANCE_URL, headers=headers, timeout=10)

    if r.status_code != 200:
        return {"error": r.text}

    return r.json()


# =========================
# 메인 UI
# =========================
st.subheader("🔎 전체 계정 잔고 요약")

if st.button("모든 계정 잔고 조회"):
    rows = []

    for acc in ["GR1", "GR2", "GR3", "GR4", "GR5", "GR6"]:
        api_key = st.secrets[acc]["api_key"]

        with st.spinner(f"{acc} 인증 중..."):
            cookie, account_id, err = authenticate(api_key)

        if err:
            rows.append({
                "Account": acc,
                "Status": "❌ 인증 실패",
                "Equity": None,
                "Available": None,
                "Message": err
            })
            continue

        data = get_balance(cookie, account_id)

        if "error" in data:
            rows.append({
                "Account": acc,
                "Status": "❌ 조회 실패",
                "Equity": None,
                "Available": None,
                "Message": data["error"]
            })
            continue

        # 실제 GRVT balance 응답 필드 (full 기준)
        equity = data.get("equity")
        available = data.get("availableBalance")

        rows.append({
            "Account": acc,
            "Status": "✅ 성공",
            "Equity": equity,
            "Available": available,
            "Message": ""
        })

    df = pd.DataFrame(rows)
    st.success("조회 완료")
    st.dataframe(df, use_container_width=True, hide_index=True)


# =========================
# 디버그
# =========================
with st.expander("🛠 선택 계정 원본 응답 보기"):
    dbg_acc = st.selectbox("계정 선택", ["GR1", "GR2", "GR3", "GR4", "GR5", "GR6"])

    if st.button("원본 API 응답 보기"):
        api_key = st.secrets[dbg_acc]["api_key"]
        cookie, account_id, err = authenticate(api_key)

        if err:
            st.error(err)
        else:
            raw = get_balance(cookie, account_id)
            st.json(raw)
