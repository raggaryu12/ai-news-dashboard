import streamlit as st
import feedparser
from datetime import datetime
from urllib.parse import quote

# ページ設定
st.set_page_config(
    page_title="AIニュースダッシュボード",
    page_icon="🎣",
    layout="wide"
)

# カスタムCSS - 夏・海・釣りテーマ
st.markdown("""
<style>
    /* 全体の背景 - 海のグラデーション */
    .stApp {
        background: linear-gradient(180deg, #87CEEB 0%, #4A90E2 50%, #2E5C8A 100%);
    }
    
    /* サイドバー - 薄いピンク */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFE4E9 0%, #FFD1DC 100%);
    }
    
    [data-testid="stSidebar"] h1 {
        color: #2E5C8A;
        font-weight: bold;
    }
    
    [data-testid="stSidebar"] label {
        color: #2E5C8A !important;
        font-weight: 600;
    }
    
    /* メインタイトル */
    h1 {
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        text-align: center;
        padding: 20px 0;
    }
    
    /* ニュースカード */
    .news-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F8FF 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 3px solid #4A90E2;
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
        display: block;
        height: 100%;
        min-height: 280px;
    }
    
    .news-card:hover {
        background: linear-gradient(135deg, #FFE5B4 0%, #FFD700 100%);
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        border-color: #FF6B6B;
    }
    
    .news-title {
        color: #2E5C8A;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    
    .news-card:hover .news-title {
        color: #D2691E;
    }
    
    .news-date {
        color: #4A90E2;
        font-size: 0.9em;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .news-summary {
        color: #333333;
        font-size: 0.95em;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    
    .news-link {
        background: linear-gradient(90deg, #4A90E2 0%, #2E5C8A 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .news-card:hover .news-link {
        background: linear-gradient(90deg, #FF6B6B 0%, #D2691E 100%);
        transform: scale(1.05);
    }
    
    /* 検索ボックス */
    .stTextInput input {
        border: 2px solid #4A90E2;
        border-radius: 10px;
        padding: 10px;
        background-color: white;
    }
    
    /* 装飾要素 */
    .wave-decoration {
        font-size: 2em;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown("# 🎣 AIニュースダッシュボード 🌊")
st.markdown('<div class="wave-decoration">🐟 🌴 ⛵ 🏖️ 🐠</div>', unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("## 🔍 検索設定")
    search_query = st.text_input(
        "検索キーワード",
        value="Artificial Intelligence",
        help="検索したいニュースのキーワードを入力してください"
    )
    
    st.markdown("---")
    st.markdown("### 🎣 釣果情報")
    st.info("最新のAIニュースを釣り上げます！")

# Google News RSS URLを生成
def get_rss_url(query):
    encoded_query = quote(query)
    return f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"

# ニュースを取得
@st.cache_data(ttl=600)
def fetch_news(query):
    url = get_rss_url(query)
    feed = feedparser.parse(url)
    return feed.entries

# ニュースを表示
if search_query:
    with st.spinner('🎣 ニュースを釣り上げ中...'):
        news_entries = fetch_news(search_query)
    
    if news_entries:
        st.success(f"🐟 {len(news_entries)}件のニュースを釣り上げました！")
        
        # 3カラムのグリッドレイアウト
        cols_per_row = 3
        for i in range(0, len(news_entries), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(news_entries):
                    entry = news_entries[i + j]
                    
                    # 日付のフォーマット
                    try:
                        pub_date = datetime(*entry.published_parsed[:6])
                        formatted_date = pub_date.strftime("%Y年%m月%d日 %H:%M")
                    except:
                        formatted_date = "日付不明"
                    
                    # 要約を取得
                    summary = entry.get('summary', '要約がありません')
                    # HTMLタグを除去
                    import re
                    summary = re.sub('<[^<]+?>', '', summary)
                    if len(summary) > 150:
                        summary = summary[:150] + "..."
                    
                    # タイトルのHTMLタグも除去
                    title = re.sub('<[^<]+?>', '', entry.title)
                    
                    # カード全体をクリック可能に
                    with cols[j]:
                        st.markdown(f"""
                        <a href="{entry.link}" target="_blank" class="news-card">
                            <div class="news-title">{title}</div>
                            <div class="news-date">📅 {formatted_date}</div>
                            <div class="news-summary">{summary}</div>
                            <span class="news-link">🔗 記事を読む</span>
                        </a>
                        """, unsafe_allow_html=True)
    else:
        st.warning("🐟 ニュースが見つかりませんでした。別のキーワードで試してください。")
else:
    st.info("👈 サイドバーから検索キーワードを入力してください")

# フッター
st.markdown("---")
st.markdown('<div class="wave-decoration">🌊 🌊 🌊</div>', unsafe_allow_html=True)
