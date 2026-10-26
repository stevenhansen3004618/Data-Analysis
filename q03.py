import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.float_format = "{:.2f}".format

url = ("https://archive.ics.uci.edu/ml/"
       "machine-learning-databases/autos/imports-85.data")

columns = {3: "fuel-type", 6: "body-style", 7: "drive-wheels",
           16: "engine-size", 25: "price"}

df = pd.read_csv(url, header=None, na_values="?",
                 usecols=list(columns)).rename(columns=columns)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

subset = df.dropna(subset=["body-style", "price"])

print("Original rows:", len(df))
print("Retained rows:", len(subset))

statistics = subset.groupby("body-style")["price"].agg(
    count="count",
    median="median",
    Q1=lambda x: x.quantile(0.25),
    Q3=lambda x: x.quantile(0.75)
)

statistics["IQR"] = statistics["Q3"] - statistics["Q1"]

statistics = statistics.sort_values(
    by=["median"],
    ascending=True
)

display_table = statistics.rename(columns={
    "count": "Count",
    "median": "Median ($)",
    "Q1": "Q1 ($)",
    "Q3": "Q3 ($)",
    "IQR": "IQR ($)",
})
display_table.index.name = "Body style"

print("\nQuestion 3 Summary Statistics:")
print(display_table.to_string(float_format="{:.2f}".format))

order = statistics.index.tolist()

plt.figure(figsize=(12, 7))


sns.boxplot(
    data=subset,
    x="body-style",
    y="price",
    order=order,
    boxprops=dict(facecolor="white", edgecolor="green"),
    whiskerprops=dict(color="green"),
    capprops=dict(color="green"),
    medianprops=dict(color="red", linewidth=2),
    flierprops=dict(
        marker="o",
        markerfacecolor="black",
        markeredgecolor="black",
        markersize=5
    )
)

plt.title("Automobile Prices by Body Style — Steven")
plt.xlabel("Body Style")
plt.ylabel("Price ($)")

plt.tight_layout()
plt.savefig("q03.png", dpi=300, bbox_inches="tight")
plt.show()