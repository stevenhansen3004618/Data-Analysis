import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

np.random.seed(42)

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

order = (
    subset.groupby("body-style")["price"]
    .median()
    .sort_values()
    .index
    .tolist()
)

plt.figure(figsize=(12, 7))

sns.violinplot(
    data=subset,
    x="body-style",
    y="price",
    order=order,
    inner="quart",
    cut=0,
    density_norm="width"
)

sns.stripplot(
    data=subset,
    x="body-style",
    y="price",
    order=order,
    jitter=0.15,
    size=4,
    alpha=0.4,
    color="black",
)


means = subset.groupby("body-style")["price"].mean()

for i, body_style in enumerate(order):
    plt.scatter(
        i,
        means[body_style],
        color="red",
        marker="D",
        s=60,
        label="Mean" if i == 0 else ""
    )

plt.title("Automobile Prices by Body Style — Steven")
plt.xlabel("Body Style")
plt.ylabel("Price ($)")

plt.legend()

plt.tight_layout()
plt.savefig("q04.png", dpi=300, bbox_inches="tight")
plt.show()