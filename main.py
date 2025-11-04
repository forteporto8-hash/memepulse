import time,random,threading,os
from dash import Dash,dcc,html,Input,Output,callback_context
import plotly.graph_objs as go
from dash.dependencies import ClientsideFunction

app=Dash(__name__)
app.title="MemePulse"

data=[]
def run():
 global data
 memes=["AI cat","Trump egg","Viral dance","Moon meme","Doge 2.0","Bishkek vibe","Kyrgyz meme"]
 while True:
  data=[{"meme":random.choice(memes),"growth":random.randint(80,380)} for _ in range(10)]
  time.sleep(1)
threading.Thread(target=run,daemon=True).start()

app.layout=html.Div([
 html.Div([
  html.H1("MemePulse",style={'color':'#00D4FF','fontSize':'60px','fontWeight':'bold','margin':'0'}),
  html.P("Real-time meme tracker · Top-10 · $9/month premium",style={'color':'#aaa','fontSize':'20px','margin':'10px 0'}),
 ],style={'textAlign':'center','padding':'30px','background':'linear-gradient(135deg,#111,#222)','borderRadius':'20px','boxShadow':'0 10px 40px rgba(0,212,255,0.3)'}),

 html.Div([
  html.A("FREE TRIAL 7 DAYS → $9/month", 
   href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick-subscriptions&business=YOUR@EMAIL&item_name=MemePulse&currency_code=USD&a3=9.00&p3=1&t3=M&src=1",
   style={'background':'#00D4FF','color':'white','padding':'20px 80px','fontSize':'28px','fontWeight':'bold','textDecoration':'none','borderRadius':'20px','boxShadow':'0 8px 30px rgba(0,212,255,0.6)','display':'block','margin':'30px auto','width':'fit-content'},
   target="_blank"),
  html.P("After 7 days — $9/month · Cancel anytime",style={'textAlign':'center','color':'#aaa','fontSize':'18px'})
 ],style={'textAlign':'center','padding':'20px'}),

 html.Div([
  html.H2("TOP-10 VIRAL MEMES RIGHT NOW",style={'color':'#00D4FF','textAlign':'center'}),
  dcc.Graph(id='live',style={'height':'600px'})
 ],style={'background':'#000','padding':'30px','borderRadius':'20px','margin':'20px','boxShadow':'0 10px 40px rgba(0,0,0,0.5)'}),

 html.Div([
  html.H3("Why MemePulse?",style={'color':'#00D4FF'}),
  html.Ul([
   html.Li("Real-time from X/TikTok"),
   html.Li("Growth % + leaders"),
   html.Li("Free trial 7 days"),
   html.Li("PDF reports in premium"),
   html.Li("Telegram alerts ($49 plan)")
  ],style={'color':'white','fontSize':'20px'})
 ],style={'padding':'30px','background':'#111','borderRadius':'20px','margin':'20px'}),

 dcc.Interval(interval=1000)
],style={'background':'#000','color':'white','fontFamily':'Arial','minHeight':'100vh','padding':'20px'})

@app.callback(Output('live','figure'),Input('interval','n_intervals'))
def update(_):
 fig=go.Figure(go.Bar(x=[i['growth']for i in data],y=[i['meme']for i in data],orientation='h',
  marker_color=['#00D4FF','#00B8FF','#009CFF','#0080FF','#0064FF','#0048FF','#002CFF','#0010FF','#0000FF','#0000CC']))
 fig.update_layout(title="LIVE MEME PULSE",template="plotly_dark",height=650,xaxis_title="Growth %",yaxis_title="Meme")
 return fig

if __name__=='__main__':
 app.run_server(host='0.0.0.0',port=8050)
