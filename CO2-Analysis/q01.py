import pandas as pd

co2_df = pd.read_csv("co2.csv")
gm_df = pd.read_csv("gapminder.csv")

df_regions = gm_df[['Country', 'region']].drop_duplicates()
df_regions.rename(columns={'Country': 'country'}, inplace=True)

df = pd.merge(co2_df, df_regions, on='country', how='inner')

year_cols = [c for c in df.columns if c.isdigit() and len(c) == 4]

df_long = pd.melt(
    df,
    id_vars=["country", "region"],
    value_vars=year_cols,
    var_name="year",
    value_name="co2"
)

df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")
df_long["co2"] = pd.to_numeric(df_long["co2"], errors="coerce")

df_long.dropna(subset=["year", "co2"], inplace=True)

df_long = df_long[df_long["year"] >= 1964]

gm_df.rename(
    columns={
        "Country": "country",
        "Year": "year",
        "GDP": "gdp"
    },
    inplace=True
)

gdp_df = gm_df[["country", "year", "gdp"]]

gdp_df["year"] = pd.to_numeric(gdp_df["year"], errors="coerce")
gdp_df["gdp"] = pd.to_numeric(gdp_df["gdp"], errors="coerce")

gdp_df.dropna(subset=["year", "gdp"], inplace=True)

gdp_df.drop_duplicates(
    subset=["country", "year"],
    inplace=True
)

final_df = pd.merge(
    df_long,
    gdp_df,
    on=["country", "year"],
    how="inner"
)

final_df = final_df[
    (final_df["co2"] >= 0) &
    (final_df["gdp"] > 0)
]

final_df.sort_values(
    by=["country", "year"],
    inplace=True
)

final_df.to_csv(
    "prepared_co2_gdp.csv",
    index=False
)

print("There are:", len(final_df), "rows in the final dataset.")
print("There are:", len(final_df.columns), "columns in the final dataset.")
print("The maximum year in the final dataset is:", final_df["year"].max())
print("The minimum year in the final dataset is:", final_df["year"].min())
print("There are:", final_df["region"].nunique(), "unique regions in the final dataset.\n")

print("The first 5 rows of the final dataset are:")
print(final_df.head())
