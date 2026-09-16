import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 처리: 세로막대 기호(|)로 분리된 경우 첫 번째 장르만 extraction
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip())
    return df

df = load_data()

# 구역 1: 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 수']

# 플롯리 도넛 그래프 생성
fig1 = px.pie(
    genre_counts, 
    values='영화 수', 
    names='장르', 
    hole=0.4,
    title="장르별 영화 비율"
)

# 호버 시 편수와 비율이 모두 표시되도록 설정
fig1.update_traces(hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}")

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 안내 구역
st.info("**이 그래프로 알 수 있는 것:** 특정 장르가 전체 박스오피스 상위권 영화 중 차지하는 비중과 다수 제작된 대표 장르를 한눈에 파악할 수 있습니다.")

st.divider()
