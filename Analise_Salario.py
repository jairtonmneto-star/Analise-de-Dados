import pandas as pd
import plotly.express as px
Arquivo_Salarial=pd.read_csv("ai_jobs_market_2025_2026.csv")

Arquivo_Salarial=Arquivo_Salarial.drop(columns=["company_size", "is_remote_friendly"])
display(Arquivo_Salarial.info())
Arquivo_Salarial=Arquivo_Salarial.dropna()
display(Arquivo_Salarial.info())


#for coluna in Arquivo_Salarial.columns:
grafico=px.histogram(Arquivo_Salarial,x= "country", y="annual_salary_usd",histfunc="sum",text_auto='.2s',title="Total de Salarios Pagos por Pais(Anual)",color="country")
#Organiza do Maior Para o Menos PAra Facilitar a Leitura
grafico.update_layout(xaxis={'categoryorder':'total descending'})
display(grafico)
