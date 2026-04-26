import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="AMZN 주가 분석 대시보드", layout="wide")

# 타이틀
st.title("🚀 아마존(AMZN) 적정 주가 시뮬레이터")
st.markdown("""
이 대시보드는 아마존의 사업 부문별 가치(SOTP)를 산출하고 경쟁사와 비교하기 위해 제작되었습니다. 
왼쪽 사이드바에서 수치를 조정하여 적정 주가 변화를 확인해보세요.
""")

# --- 사이드바: 입력 변수 ---
st.sidebar.header("📊 2025E 실적 전망 수정")

# AWS 부문
st.sidebar.subheader("1. AWS (Cloud)")
aws_rev = st.sidebar.number_input("AWS 예상 매출 ($M)", value=110000, step=1000)
aws_mult = st.sidebar.slider("AWS 적용 배수 (EV/Sales)", 5.0, 15.0, 10.0)

# 광고 부문
st.sidebar.subheader("2. Advertising")
ads_rev = st.sidebar.number_input("광고 예상 매출 ($M)", value=60000, step=1000)
ads_mult = st.sidebar.slider("광고 적용 배수 (EV/Sales)", 3.0, 12.0, 7.0)

# 리테일 부문
st.sidebar.subheader("3. Retail & Others")
retail_rev = st.sidebar.number_input("리테일 예상 매출 ($M)", value=480000, step=1000)
retail_mult = st.sidebar.slider("리테일 적용 배수 (EV/Sales)", 0.5, 2.5, 1.2)

# 기타 재무 정보
st.sidebar.subheader("4. 재무 세부사항")
net_debt = st.sidebar.number_input("순부채 ($M)", value=40000)
shares = st.sidebar.number_input("발행 주식 수 (M)", value=10500)

# --- 계산 로직 ---
val_aws = aws_rev * aws_mult
val_ads = ads_rev * ads_mult
val_retail = retail_rev * retail_mult
total_ev = val_aws + val_ads + val_retail
equity_value = total_ev - net_debt
target_price = equity_value / shares

# --- 메인 화면: 결과 표시 ---
col1, col2, col3 = st.columns(3)
with col1:
    # :.2f로 수정 (실수형 표시)
    st.metric("산출 적정 주가", f"${target_price:.2f}")
with col2:
    st.metric("기업 가치 (EV)", f"${total_ev/1000:,.1f}B")
with col3:
    st.metric("자기자본 가치", f"${equity_value/1000:,.1f}B")

st.divider()

# --- 시각화 1: 사업부별 가치 비중 (Donut Chart) ---
st.subheader("💡 아마존 사업 부문별 가치 기여도")
labels = ['AWS', 'Advertising', 'Retail & Others']
values = [val_aws, val_ads, val_retail]

# color_discrete_sequence 로 오타 수정 완료
fig_pie = px.pie(names=labels, values=values, hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie, use_container_width=True)

# --- 시각화 2: 경쟁사 비교 (Bar Chart) ---
st.subheader("🏁 경쟁사 주요 지표 비교")
comp_data = pd.DataFrame({
    'Company': ['Amazon', 'Microsoft', 'Walmart'],
    'OPM (%)': [10.8, 43.5, 4.2],
    'Rev Growth (%)': [11.5, 14.2, 4.8],
    'Forward P/E': [32.0, 31.0, 28.0]
})

tab1, tab2 = st.tabs(["수익성 & 성장성", "밸류에이션(P/E)"])
with tab1:
    fig_comp = px.bar(comp_data, x='Company', y=['OPM (%)', 'Rev Growth (%)'], 
                      barmode='group', title="영업이익률 및 매출성장률 비교")
    st.plotly_chart(fig_comp, use_container_width=True)
with tab2:
    fig_pe = px.bar(comp_data, x='Company', y='Forward P/E', color='Company', title="선행 P/E 배수 비교")
    st.plotly_chart(fig_pe, use_container_width=True)

# --- 정성적 분석 메모 & 산출 근거 ---
st.divider()
st.subheader("📝 분석 메모 및 산출 근거")
st.markdown(f"""
### 1. 가치 산정 방식 (SOTP)
- **AWS 가치 (${val_aws/1000:,.1f}B):** 클라우드 시장 지배력을 반영하여 EV/Sales {aws_mult}배 적용.
- **광고 가치 (${val_ads/1000:,.1f}B):** 고마진 검색 광고 비즈니스로 {ads_mult}배 적용.
- **리테일 가치 (${val_retail/1000:,.1f}B):** 물류 효율화 가치를 포함하여 {retail_mult}배 적용.

### 2. 정성적 전망
- **Upside:** AWS의 생성형 AI 매출 본격화, 광고 사업 부문의 영업이익 기여도 확대.
- **Downside:** 반독점 규제 이슈, 소비자 지출 둔화.
""")

st.caption("주의: 본 데이터는 학습용이며 투자 권유를 목적으로 하지 않습니다.")
