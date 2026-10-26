import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = ("https://archive.ics.uci.edu/ml/"
       "machine-learning-databases/autos/imports-85.data")

columns = {3: "fuel-type", 6: "body-style", 7: "drive-wheels",
           16: "engine-size", 25: "price"}

df = pd.read_csv(url, header=None, na_values="?",
                 usecols=list(columns)).rename(columns=columns)

df["engine-size"] = pd.to_numeric(df["engine-size"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

subset = df.dropna(subset=["engine-size", "price", "drive-wheels"])

print("Original rows:", len(df))
print("Retained rows:", len(subset))

x_min = subset["engine-size"].min()
x_max = subset["engine-size"].max()
y_min = subset["price"].min()
y_max = subset["price"].max()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.scatterplot(
    data=subset,
    x="engine-size",
    y="price",
    hue="drive-wheels",
    hue_order=["4wd", "fwd", "rwd"],
    alpha=0.6,
    ax=axes[0]
)

axes[0].set_title("Engine Size vs. Price — Steven")
axes[0].set_xlabel("Engine Size")
axes[0].set_ylabel("Price ($)")
axes[0].set_xlim(x_min, x_max)
axes[0].set_ylim(y_min, y_max)

hexbin = axes[1].hexbin(
    subset["engine-size"],
    subset["price"],
    gridsize=15,
    mincnt=1
)

axes[1].set_title("Engine Size vs. Price — Steven")
axes[1].set_xlabel("Engine Size")
axes[1].set_ylabel("Price ($)")
axes[1].set_xlim(x_min, x_max)
axes[1].set_ylim(y_min, y_max)


colorbar = fig.colorbar(hexbin, ax=axes[1])
colorbar.set_label("Number of automobile records")

plt.tight_layout()
plt.savefig("q05.png", dpi=300, bbox_inches="tight")
plt.show()