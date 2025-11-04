import time,random,threading
from dash import Dash,dcc,html,Input,Output
import plotly.graph_objs as go

app=Dash(__name__)
app.title="MemePulse"

data=[]
def run():
 global data
 memes=["AI cat","Trump egg","Viral dance","Moon meme","Doge 2.0"]
 while True:
  data=[{"meme":random.choice(memes),"growth":random.randint(50,380)} for _ in range(10)]
  time.sleep(1)
threading.Thread(target=run,daemon=True).start()

app.layout=html.Div([
 html.H1("MemePulse",style={'textAlign':'center','color':'#00D4FF','fontSize':'48px','fontWeight':'bold'}),
 html.Div([html.A("Premium: $9 / month",
  href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick-subscriptions&business=YOUR@EMAIL&item_name=MemePulse&currency_code=USD&a3=9.00&p3=1&t3=M&src=1",
  style={'background':'#00D4FF','color':'white','padding':'18px 60px','fontSize':'24px','fontWeight':'bold','textDecoration':'none','borderRadius':'15px','boxShadow':'0 6px 30px rgba(0,212,255,0.5)'},
  target="_blank")],style={'textAlign':'center','padding':'40px'}),
 dcc.Graph(id='live'),dcc.Interval(interval=1000)
],style={'background':'#111','color':'white','fontFamily':'Arial','minHeight':'100vh'})

@app.callback(Output('live','figure'),Input('interval','n_intervals'))
def update(_):
 fig=go.Figure(go.Bar(x=[i['growth']for i in data],y=[i['meme']for i in data],orientation='h',marker_color='#00D4FF'))
 fig.update_layout(title="GLOBAL TOP-10 MEMES",template="plotly_dark",height=650)
 return fig

if __name__=='__main__':
 app.run_server(host='0.0.0.0',port=8050)
