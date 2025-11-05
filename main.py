import threading
import time
import random
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import requests
from bs4 import BeautifulSoup

# === Приложение Dash ===
app = Dash(__name__)
app.title = "MemePulse LIVE"
server = app.server  # Для Gunicorn / Render

data = []
free_used = 0

# === Функция для сбора мемов ===
def run():
    global data
    while True:
        memes = []

        # --- Reddit ---
        try:
            r = requests.get(
                "https://www.reddit.com/r/memes/hot.json?limit=20",
                headers={'User-agent': 'meme-bot'}
            )
            for post in r.json()['data']['children']:
                url = post['data'].get('url', '')
                if url.endswith(('.jpg', '.png', '.gif')):
                    memes.append({
                        "meme": post['data']['title'][:40] + "...",
                        "growth": post['data'].get('score', 0),
                        "source": "Reddit"
                    })
        except Exception as e:
            print("Reddit error:", e)

        # --- X (Twitter) через скрап ---
        try:
            r = requests.get("https://syndication.twitter.com/srv/timeline-profile/screen-name/elonmusk?count=10")
            soup = BeautifulSoup(r.text, 'html.parser')
            for tweet in soup.find_all('div', {'data-testid': 'tweetText'}):
                memes.append({
                    "meme": tweet.get_text()[:40] + "...",
                    "growth": random.randint(50, 500),  # Эмуляция популярности
                    "source": "X"
                })
        except Exception as e:
            print("X error:", e)

        # --- TikTok (заглушка, без ключей) ---
        trending = ["NPC filter", "Skibidi toilet", "Ohio edit", "Core core", "Gyatt"]
        for t in trending:
            memes.append({
                "meme": t,
                "growth": random.randint(100, 1000),
                "source": "TikTok"
            })

        # --- Сортировка по росту и топ-10 ---
        data = sorted(memes, key=lambda x: x['growth'], reverse=True)[:10]

        # --- Интервал 45 секунд ---
        time.sleep(45)

# === Запуск потока сбора мемов ===
threading.Thread(target=run, daemon=True).start()

# === Layout Dash ===
app.layout = html.Div([
    html.H1("MemePulse LIVE", style={'color':'#00D4FF','fontSize':'68px','textAlign':'center','fontWeight':'900'}),
    html.P("Real-time from Reddit · X · TikTok", style={'color':'#00FF9D','fontSize':'28px','textAlign':'center'}),
    
    html.Div([
        html.Button("FREE 3 MEMES", id="free",
                    style={'background':'#00FF9D','color':'black','padding':'20px 70px','fontSize':'26px',
                           'borderRadius':'20px','fontWeight':'bold'}),
        html.A("Premium $9/month",
               href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick-subscriptions&business=YOUR@EMAIL",
               target="_blank",
               style={'background':'#00D4FF','color':'white','padding':'20px 70px','fontSize':'26px',
                      'borderRadius':'20px','marginLeft':'20px','textDecoration':'none','fontWeight':'bold'})
    ], style={'textAlign':'center','padding':'30px'}),
    
    html.Div(id="free-msg", style={'color':'#00FF9D','fontSize':'24px','textAlign':'center','fontWeight':'bold'}),
    dcc.Graph(id='live', style={'height':'800px'}),
    dcc.Interval(id="interval", interval=45000)  # 45 секунд
], style={'background':'#000','color':'white','fontFamily':'Montserrat','padding':'20px','minHeight':'100vh'})

# === Callback для обновления графика и сообщения ===
@app.callback(
    [Output('live','figure'), Output('free-msg','children')],
    [Input('interval','n_intervals'), Input('free','n_clicks')]
)
def update(_, click):
    global free_used
    msg = ""
    if click and free_used < 3:
        free_used += 1
        msg = f"Free meme #{free_used} unlocked! {3-free_used} left"
    
    fig = go.Figure()
    if data:
        fig = go.Figure(go.Bar(
            x=[d['growth'] for d in data],
            y=[f"{d['meme']} ({d['source']})" for d in data],
            orientation='h',
            marker_color='#00D4FF'
        ))
    fig.update_layout(title="LIVE GLOBAL MEMES", template="plotly_dark", height=800)
    return fig, msg

# === Запуск сервера ===
if __name__ == '__main__':
    app.run_server(debug=False)
