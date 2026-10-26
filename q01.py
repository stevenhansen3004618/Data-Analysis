import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = ("https://archive.ics.uci.edu/ml/"
       "machine-learning-databases/autos/imports-85.data")

columns = {3: "fuel-type", 6: "body-style", 7: "drive-wheels",
           16: "engine-size", 25: "price"}

df = pd.read_csv(url, header=None, na_values="?",
                 usecols=list(columns)).rename(columns=columns)

for col in ["engine-size", "price"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

subset = df.dropna(subset=["body-style", "fuel-type", "price"])

print("Original rows:", len(df))
print("Retained rows:", len(subset))

counts = subset["body-style"].value_counts()
order = counts.index.tolist()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.barplot(
    x=counts.index,
    y=counts.values,
    ax=axes[0]
)

axes[0].bar_label(axes[0].containers[0], fmt="%d")

axes[0].set_title("Body-Style Counts — Steven")
axes[0].set_xlabel("Body Style")
axes[0].set_ylabel("Count")

largest = counts.index[0]
largest_count = counts.values[0]

axes[0].annotate(
    f"Most common: {largest}",
    xy=(0, largest_count),
    xytext=(0.5, largest_count + 10),
    arrowprops=dict(arrowstyle="->", color="black")
)

sns.barplot(
    data=subset,
    x="body-style",
    y="price",
    hue="fuel-type",
    order=order,
    hue_order=["gas", "diesel"],
    errorbar=None,
    ax=axes[1]
)

axes[1].set_title("Mean Price by Body Style and Fuel Type — Steven")
axes[1].set_xlabel("Body Style")
axes[1].set_ylabel("Price ($)")
axes[1].legend(title="Fuel Type")

plt.tight_layout()

plt.savefig("q01.png", dpi=300, bbox_inches="tight")

plt.show()