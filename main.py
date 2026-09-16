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

# ==========================================
# 구역 1: 장르별 영화 편수 (도넛 그래프)
# ==========================================
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

# 그래프 1 해석 안내
st.info("**이 그래프로 알 수 있는 것:** 특정 장르가 전체 박스오피스 상위권 영화 중 차지하는 비중과 다수 제작된 대표 장르를 한눈에 파악할 수 있습니다.")

st.divider()

# ==========================================
# 구역 2: 장르 및 영화별 총 관객수 (트리맵)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객수 분포")

# 플롯리 트리맵 생성 (장르 > 영화명 계층구조, 칸 크기 = total_audi)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르-영화별 총 관객수 트리맵"
)

# 호버 시 영화명과 총 관객수가 표시되도록 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 2 해석 안내
st.info("**이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 가장 많은 총 관객수를 모았으며, 시장 지배력이 높은지 직관적으로 비교할 수 있습니다.")

st.divider()

# ==========================================
# 구역 3: 총 관객수 분포 (히스토그램)
# ==========================================
st.subheader("3. 영화별 총 관객수 분포")

# 플롯리 히스토그램 생성
fig3 = px.histogram(
    df, 
    x='total_audi',
    nbins=30,
    title="총 관객수 히스토그램",
    labels={'total_audi': '총 관객수(명)'}
)

fig3.update_traces(
    hovertemplate="관객수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# 최다 관객 동적 계산
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 그래프 3 해석 안내
st.info(
    f"**이 그래프로 알 수 있는 것:** 대다수의 영화는 총 관객수 100만~200만 명 이하의 낮은 구간에 밀집되어 있는 오른쪽으로 비대칭(Right-skewed)된 분포 형태를 띱니다. "
    f"가장 많은 관객 수를 기록한 1위 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,}명)입니다."
)

st.divider()
