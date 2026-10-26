import pandas as pd
import plotly.express as px

df = pd.read_csv("prepared_co2_gdp.csv")

df = df[
    (df["year"] >= 1990) &
    (df["gdp"] > 0) &
    (df["co2"] >= 0)
]

df = df.dropna(
    subset=["country", "region", "year", "gdp", "co2"]
)

x_min = df["gdp"].min()
x_max = df["gdp"].max()

y_min = df["co2"].min()
y_max = df["co2"].max()

x_pad = (x_max - x_min) * 0.05
y_pad = (y_max - y_min) * 0.05

x_range = [
    max(x_min - x_pad, 0.1),
    x_max + x_pad
]

y_range = [
    y_min - y_pad,
    y_max + y_pad
]

fig = px.scatter(
    df,
    x="gdp",
    y="co2",
    animation_frame="year",
    animation_group="country",
    color="region",
    hover_name="country",
    log_x=True,
    title="Steven Hansen - GDP vs CO2 Emissions Over Time",
    labels={
        "gdp": "GDP Per Capita",
        "co2": "CO2 Emissions Per Person"
    },
    range_x=x_range,
    range_y=y_range
)

fig.write_html(
    "q05.html",
    include_plotlyjs=True
)

fig.show()
