import pandas as pd

from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10

df = pd.read_csv("prepared_co2_gdp.csv")

df = df[(df["year"] == 2000) & (df["co2"] > 0)]

regions = sorted(df["region"].unique())

colors = {
    region: Category10[10][i % 10]
    for i, region in enumerate(regions)
}

fig = figure(
    title="Steven Hansen: CO2 Emissions vs GDP per Capita (2000)",
    x_axis_label="GDP per Capita",
    y_axis_label="CO2 Emissions per Person",
    y_axis_type="log",
    tools="pan,wheel_zoom,box_zoom,reset,save"
)

for region in regions:
    region_df = df[df["region"] == region]

    source = ColumnDataSource(region_df)

    fig.scatter(
        x="gdp",
        y="co2",
        source=source,
        size=8,
        color=colors[region],
        alpha=0.8,
        muted_alpha=0.1,
        legend_label=region
    )

hover = HoverTool(
    tooltips=[
        ("Country", "@country"),
        ("Region", "@region"),
        ("GDP per Capita", "@gdp{0,0.00}"),
        ("CO2 per Person", "@co2{0.00}")
    ]
)

fig.add_tools(hover)

fig.legend.title = "Region"
fig.legend.location = "bottom_right"
fig.legend.click_policy = "mute"

output_file("q02.html")

save(fig)
show(fig)
