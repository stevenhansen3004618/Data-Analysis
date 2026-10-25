import pandas as pd

from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    Slider,
    CustomJS,
    CDSView,
    GroupFilter
)
from bokeh.plotting import figure
from bokeh.palettes import Category10

df = pd.read_csv("prepared_co2_gdp.csv")

df = df[df["co2"] > 0].copy()

regions = sorted(df["region"].unique())

color_map = {
    region: Category10[10][i % len(Category10[10])]
    for i, region in enumerate(regions)
}

df["color"] = df["region"].map(color_map)

years = sorted(df["year"].unique())

initial_year = 2000 if 2000 in years else years[0]

current_df = df[df["year"] == initial_year]

all_source = ColumnDataSource(df)
source = ColumnDataSource(current_df)

# Fixed ranges from COMPLETE dataset
x_min = df["gdp"].min()
x_max = df["gdp"].max()

x_pad = (x_max - x_min) * 0.05

y_min = df["co2"].min() / 1.5
y_max = df["co2"].max() * 1.5

p = figure(
    width=900,
    height=600,
    x_range=(x_min - x_pad, x_max + x_pad),
    y_range=(y_min, y_max),
    y_axis_type="log",
    title=f"Steven Hansen - GDP vs CO2 ({initial_year})",
    tools="pan,wheel_zoom,box_zoom,reset,save"
)

for region in regions:

    view = CDSView(
        filter=GroupFilter(
            column_name="region",
            group=region
        )
    )

    p.scatter(
        x="gdp",
        y="co2",
        source=source,
        view=view,
        color="color",
        size=8,
        legend_label=region,
        muted_alpha=0.1
    )

hover = HoverTool(
    tooltips=[
        ("Country", "@country"),
        ("Region", "@region"),
        ("GDP", "@gdp{0,0}"),
        ("CO2", "@co2{0.00}")
    ]
)

p.add_tools(hover)

p.xaxis.axis_label = "GDP Per Capita"
p.yaxis.axis_label = "CO2 Emissions Per Person"

p.legend.click_policy = "mute"

slider = Slider(
    start=min(years),
    end=max(years),
    value=initial_year,
    step=1,
    title="Year"
)

callback = CustomJS(
    args=dict(
        all_source=all_source,
        source=source,
        plot=p
    ),
    code="""
    const year = cb_obj.value;

    const all = all_source.data;

    const gdp = [];
    const co2 = [];
    const country = [];
    const region = [];
    const color = [];

    for (let i = 0; i < all['year'].length; i++) {

        if (Number(all['year'][i]) === Number(year)) {

            gdp.push(all['gdp'][i]);
            co2.push(all['co2'][i]);
            country.push(all['country'][i]);
            region.push(all['region'][i]);
            color.push(all['color'][i]);
        }
    }

    source.data = {
        gdp: gdp,
        co2: co2,
        country: country,
        region: region,
        color: color
    };

    plot.title.text =
        "Steven Hansen - GDP vs CO2 (" + year + ")";

    source.change.emit();
"""
)

slider.js_on_change("value", callback)

layout = column(slider, p)

output_file("q03.html")

show(layout)