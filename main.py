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

# ==========================================
# 구역 4: 개봉일 스크린수와 총 관객수의 관계 (산점도)
# ==========================================
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

# 플롯리 산점도 생성
fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객수(명)',
        'genre': '장르'
    }
)

# 호버 서식 변경 (영화명 + 상세 스크린수 및 관객수)
fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

# 그래프 4 해석 안내
st.info("**이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 대체로 총 관객수가 높은 양의 상관관계를 보이지만, 스크린수에 비해 유독 높은 흥행을 거둔 작품과 장르별 차이도 함께 확인할 수 있습니다.")

st.divider()

# ==========================================
# 구역 5: 주요 장르별 총 관객수 분포 (상자 그림)
# ==========================================
st.subheader("5. 주요 장르별 총 관객수 분포 (10편 이상 장르)")

# 영화가 10편 이상인 장르만 필터링
genre_counts = df['genre'].value_counts()
major_genres = genre_counts[genre_counts >= 10].index
df_filtered = df[df['genre'].isin(major_genres)]

# 플롯리 박스플롯 생성
fig5 = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points="outliers",  # 이상치(상자 밖 점) 표시
    title="주요 장르별 총 관객수 박스플롯",
    labels={
        'genre': '장르',
        'total_audi': '총 관객수(명)'
    }
)

# 호버 마우스 오버 서식 지정
fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

# 그래프 5 해석 안내
st.info("**이 그래프로 알 수 있는 것:** 주요 장르별 관객수의 중간값과 분포 범위를 비교할 수 있으며, 상자 밖으로 튀어나온 이상치 점들을 통해 장르 평균을 뛰어넘은 대형 흥행작을 쉽게 식별할 수 있습니다.")

st.divider()

# ==========================================
# 구역 6: 개봉 성과와 최종 흥행의 관계 (버블 그래프)
# ==========================================
st.subheader("6. 개봉일 성과(스크린, 첫 주 관객)와 최종 흥행(총 관객)의 관계")

# 플롯리 버블 그래프 생성 (fig4 기반)
fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi', # 점 크기 = 첫 주 관객
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수 (크기: 첫 주 관객)",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객수(명)',
        'first_week_audi': '첫 주 관객수(명)',
        'genre': '장르'
    },
    size_max=60 # 버블 최대 크기 설정
)

# 호버 서식 변경 (첫 주 관객 정보 추가)
fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>"
                  "개봉일 스크린수: %{x:,}개<br>"
                  "<b>첫 주 관객수: %{marker.size:,}명</b><br>"
                  "총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

# 그래프 6 해석 안내
st.info("**이 그래프로 알 수 있는 것:** 네 번째 산점도에 '첫 주 관객수'를 점의 크기로 추가하여, 초기 흥행(개봉 성과)이 최종 총 관객수에 미치는 영향력을 시각적으로 비교할 수 있습니다. 버블이 크고 위쪽에 위치할수록 초기 기세가 최종 흥행으로 잘 이어진 경우입니다.")

st.divider()

# ==========================================
# 구역 7: 제작 국가 및 장르별 영화 편수 (선버스트)
# ==========================================
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포")

# 선버스트용 집계 (국가 x 장르별 편수)
nation_genre_counts = df.groupby(['nation', 'genre']).size().reset_index(name='movie_count')

# 플롯리 선버스트 그래프 생성
fig7 = px.sunburst(
    nation_genre_counts,
    path=['nation', 'genre'],
    values='movie_count',
    title="제작 국가 > 장르별 영화 편수 선버스트"
)

# 호버 서식 지정
fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%} (상위 항목 대비)<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

# 그래프 7 해석 안내
st.info("**이 그래프로 알 수 있는 것:** 각 제작 국가별로 어떤 장르의 영화가 주로 수입되거나 제작되었는지, 국가 간 대표 장르의 다변화 구조를 한눈에 비교할 수 있습니다.")

st.divider()

# ==========================================
# 구역 8: 개봉일 스크린수와 10위권 체류일수 (관계 분석)
# ==========================================
st.subheader("8. 개봉일 스크린수가 많으면 10위에 더 오래 머무는가?")

# 개봉일 스크린수 vs 10위권 체류일수 산점도
fig8 = px.scatter(
    df,
    x='first_scrn',
    y='days_in_top10',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 10위권 체류일수 (Days in Top 10)",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'days_in_top10': '10위권 체류일수(일)',
        'genre': '장르'
    }
)

# 호버 서식 변경
fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>10위권 체류일수: %{y}일<extra></extra>"
)

st.plotly_chart(fig8, use_container_width=True)

# 그래프 8 해석 안내
st.info("**이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많은 영화들이 대체로 10위권 체류일수가 긴 편이지만, 스크린수가 적어도 관객 평가에 힘입어 오래 머문 영화나 스크린수가 많았음에도 일찍 순위권에서 벗어난 사례도 확인할 수 있습니다.")

st.divider()
