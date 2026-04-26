import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("AMZN Valuation Dashboard & Simulator")

# 1. 사이드바 - 사용자 입력 (수치 수정 가능)
st.sidebar.header("Valuation Inputs (2025E)")
aws_rev = st.sidebar.number_input("AWS Revenue ($M)", value=110000)
aws_mult = st.sidebar.slider("AWS EV/S Multiple", 5.0, 15.0, 10.0)

ads_rev = st.sidebar.number_input("Ads Revenue ($M)", value=60000)
ads_mult = st.sidebar.slider("Ads EV/S Multiple", 3.0, 10.0, 7.0)

retail_rev = st.sidebar.number_input("Retail Revenue ($M)", value=480000)
retail_mult = st.sidebar.slider("Retail EV/S Multiple", 0.5, 2.0, 1.2)

# 2. 계산 로직
aws_val = aws_rev * aws_mult
ads_val = ads_rev * ads_mult
retail_val = retail_rev * retail_mult
total_ev = aws_val + ads_val + retail_val
share_price = total_ev / 10500 # 주식수 10.5B 가정

# 3. 메인 화면 - 시각화
col1, col2, col3 = st.columns(3)
col1.metric("적정 시가총액", f"${total_ev/1000:,.1f}B")
col2.metric("산출 적정 주가", f"${share_price:,.2d}")
col3.metric("현재가 대비 상승여력", "+15%") # 예시

st.markdown("---")
st.subheader("경쟁사 비교 분석 (정성/정량)")
df = pd.DataFrame({
    'Metric': ['OPM', 'Revenue Growth', 'FCF Margin'],
    'AMZN': [10.8, 11.5, 9.2],
    'MSFT': [43.5, 14.2, 28.0],
    'WMT': [4.2, 4.8, 2.5]
})
st.bar_chart(df.set_index('Metric'))

st.info("메모: 아마존의 주가는 AWS의 AI 매출 가속화 여부에 따라 배수가 재평가될 수 있습니다.")
