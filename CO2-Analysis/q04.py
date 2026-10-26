import pandas as pd
import plotly.express as px

df = pd.read_csv("prepared_co2_gdp.csv")
df = df[df['gdp'] > 0]

df = df.dropna(subset=['co2', 'gdp', 'country', 'region'])
fig = px.scatter(
    df[df["year"] == 2010],
    x="gdp",
    y="co2",
    color="region",
    hover_name="country",   
    log_x=True,
    facet_col="region",
    title= 'Steven Hansen - GDP vs CO2 Emissions by Region (2010)',
    labels={
    "gdp": "GDP per Capita",
    "co2": "CO2 Emissions per Person"
    })

fig.write_html(
    "q04.html",
    include_plotlyjs=True
)

fig.show()
