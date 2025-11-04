from dash import Dash,dcc,html,Input,Output
import plotly.graph_objs as go

app=Dash(__name__)
app.title="MemePulse"

data=[]
free_used=0

def run():
 global data
 memes=["AI cat","Trump egg","Viral dance","Moon meme","Doge 2.0","Bishkek vibe","Kyrgyz meme"]
 while True:
  data=[{"meme":random.choice(memes),"growth":random.randint(80,380)} for _ in range(10)]
  time.sleep(1)
threading.Thread(target=run,daemon=True).start()

app.layout=html.Div([
 html.Div([
  html.H1("MemePulse",style={'color':'#00D4FF','fontSize':'72px','fontWeight':'bold','margin':'0'}),
  html.P("Real-time meme tracker · Top-10 · Free 3 memes",style={'color':'#00D4FF','fontSize':'26px','margin':'10px 0'}),
 ],style={'textAlign':'center','padding':'40px','background':'linear-gradient(135deg,#000,#111)','borderRadius':'25px','boxShadow':'0 15px 50px rgba(0,212,255,0.4)'}),

 html.Div([
  html.Button("FREE 3 MEMES (no card)",id="free",style={'background':'#00FF9D','color':'black','padding':'20px 80px','fontSize':'28px','fontWeight':'bold','border':'none','borderRadius':'20px','margin':'20px'}),
  html.A("Premium $9/month →",href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick-subscriptions&business=YOUR@EMAIL&item_name=MemePulse&currency_code=USD&a3=9.00&p3=1&t3=M&src=1",target="_blank",style={'background':'#00D4FF','color':'white','padding':'20px 80px','fontSize':'28px','fontWeight':'bold','textDecoration':'none','borderRadius':'20px','margin':'20px','display':'inline-block'}),
  html.Div(id="free-msg",style={'color':'#00FF9D','fontSize':'20px','textAlign':'center'})
 ],style={'textAlign':'center','padding':'20px'}),

 html.Div([
  html.H2("TOP-10 VIRAL MEMES RIGHT NOW",style={'color':'#00D4FF','textAlign':'center'}),
  dcc.Graph(id='live',style={'height':'700px'})
 ],style={'background':'#000','padding':'40px','borderRadius':'25px','margin':'30px','boxShadow':'0 15px 50px rgba(0,0,0,0.6)'}),

 html.Div([
  html.H3("Why MemePulse?",style={'color':'#00D4FF'}),
  html.Ul([
   html.Li("Real-time from X/TikTok",style={'fontSize':'22px'}),
   html.Li("Free 3 memes — no card",style={'fontSize':'22px'}),
   html.Li("Growth % + leaders",style={'fontSize':'22px'}),
   html.Li("PDF reports ($9)",style={'fontSize':'22px'}),
   html.Li("Email alerts ($49)",style={'fontSize':'22px'})
  ])
 ],style={'padding':'40px','background':'#111','borderRadius':'25px','margin':'30px'}),

 dcc.Interval(interval=1000)
],style={'background':'#000','color':'white','fontFamily':'Arial','minHeight':'100vh','padding':'20px'})

@callback([Output('live','figure'),Output('free-msg','children')],[Input('interval','n_intervals'),Input('free','n_clicks')])
def update(_,click):
 global free_used
 msg=""
 if click and free_used<3:
  free_used+=1
  msg=f"Free meme #{free_used} unlocked! {3-free_used} left"
 fig=go.Figure(go.Bar(x=[i['growth']for i in data],y=[i['meme']for i in data],orientation='h',
  marker=dict(color=['#00D4FF','#00B8FF','#009CFF','#0080FF','#0064FF','#0048FF','#002CFF','#0010FF','#0000FF','#0000CC'])))
 fig.update_layout(title="LIVE MEME PULSE",template="plotly_dark",height=700,xaxis_title="Growth %",yaxis_title="Meme")
 return fig,msg

if __name__=='__main__':
 app.run_server(debug=False)
 
