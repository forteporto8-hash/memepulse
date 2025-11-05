import threading, time, os
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import tweepy
import praw
from TikTokApi import TikTokApi

app = Dash(__name__)
app.title = "MemePulse LIVE"
server = app.server

data = []
free_used = 0

# === КЛЮЧИ ИЗ .env (вставь в Render → Environment) ===
BEARER = os.getenv("X_BEARER")
REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
TIKTOK_COOKIE = os.getenv("TIKTOK_COOKIE", "tt_webid_v2=123456789")

# === X (Twitter) ===
def get_x_memes():
    client = tweepy.Client(bearer_token=BEARER)
    tweets = client.search_recent_tweets(query="#meme OR #funny -is:retweet lang:en", max_results=20)
    memes = []
    for t in tweets.data or []:
        memes.append({
            "meme": t.text[:30] + "...",
            "growth": t.public_metrics['like_count'] + t.public_metrics['retweet_count'],
            "source": "X"
        })
    return memes

# === Reddit ===
def get_reddit_memes():
    reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent="meme-pulse")
    memes = []
    for sub in ["memes", "dankmemes", "wholesomememes"]:
        for post in reddit.subreddit(sub).hot(limit=5):
            memes.append({
                "meme": post.title[:30] + "...",
                "growth": post.score,
                "source": "Reddit"
            })
    return memes

# === TikTok ===
def get_tiktok_memes():
    api = TikTokApi.get_instance(custom_verify_fp=TIKTOK_COOKIE)
    memes = []
    for video in api.trending.videos(count=10):
        memes.append({
            "meme": video.desc[:30] + "...",
            "growth": video.stats['diggCount'] + video.stats['shareCount'],
            "source": "TikTok"
        })
    return memes

# === ЖИВОЙ СБОР ===
def run():
    global data
    while True:
        all_memes = []
        try:
            all_memes += get_x_memes()
        except: pass
        try:
            all_memes += get_reddit_memes()
        except: pass
        try:
            all_memes += get_tiktok_memes()
        except: pass

        data = sorted(all_memes, key=lambda x: x['growth'], reverse=True)[:10]
        time.sleep(30)

threading.Thread(target=run, daemon=True).start()

# === ДИЗАЙН ===
app.layout = html.Div([
    html.H1("MemePulse LIVE", style={'color':'#00D4FF','fontSize':'72px','textAlign':'center'}),
    html.P("Real-time from X · Reddit · TikTok", style={'color':'#00FF9D','fontSize':'28px','textAlign':'center'}),
    html.Div([
        html.Button("FREE 3 MEMES", id="free", style={'background':'#00FF9D','color':'black','padding':'20px 70px','fontSize':'26px','borderRadius':'20px','fontWeight':'bold'}),
        html.A("Premium $9/month", href=f"https://paypal.com/...&business={os.getenv('PAYPAL','test@mail.ru')}", target="_blank",
               style={'background':'#00D4FF','color':'white','padding':'20px 70px','fontSize':'26px','borderRadius':'20px','marginLeft':'20px','textDecoration':'none','fontWeight':'bold'})
    ], style={'textAlign':'center','padding':'30px'}),
    html.Div(id="free-msg", style={'color':'#00FF9D','fontSize':'24px','textAlign':'center','fontWeight':'bold'}),
    dcc.Graph(id='live', style={'height':'800px'}),
    dcc.Interval(interval=30000)
], style={'background':'#000','color':'white','fontFamily':'Montserrat','padding':'20px'})

@callback(
    [Output('live','figure'), Output('free-msg','children')],
    [Input('interval','n_intervals'), Input('free','n_clicks')]
)
def update(_, click):
    global free_used
    msg = ""
    if click and free_used < 3:
        free_used += 1
        msg = f"Free meme #{free_used} unlocked! {3-free_used} left"
    fig = go.Figure(go.Bar(
        x=[d['growth'] for d in data],
        y=[f"{d['meme']} ({d['source']})" for d in data],
        orientation='h',
        marker_color='#00D4FF'
    ))
    fig.update_layout(title="LIVE GLOBAL MEMES", template="plotly_dark", height=800)
    return fig, msg

if __name__ == '__main__':
    app.run_server(debug=False)
