import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = ("https://archive.ics.uci.edu/ml/"
       "machine-learning-databases/autos/imports-85.data")

columns = {3: "fuel-type", 6: "body-style", 7: "drive-wheels",
           16: "engine-size", 25: "price"}

df = pd.read_csv(url, header=None, na_values="?",
                 usecols=list(columns)).rename(columns=columns)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

subset = df.dropna(subset=["price"])

print("Original rows:", len(df))
print("Retained rows:", len(subset))

mean_price = subset["price"].mean()
median_price = subset["price"].median()
p90_price = subset["price"].quantile(0.90)

plt.figure(figsize=(10, 6))

sns.histplot(
    subset["price"],
    bins=45,
    edgecolor="black",
    color="skyblue"
)

plt.title("Price Distribution with Summary Statistics — Steven")
plt.xlabel("Price ($)")
plt.ylabel("Count")

plt.axvline(
    mean_price,
    color="red",
    linestyle="-",
    linewidth=2,
    label=f"Mean: ${mean_price:.2f}"
)

plt.axvline(
    median_price,
    color="#B8860B",
    linestyle="--",
    linewidth=2,
    label=f"Median: ${median_price:.2f}"
)

plt.axvline(
    p90_price,
    color="purple",
    linestyle=":",
    linewidth=2,
    label=f"90th Percentile: ${p90_price:.2f}"
)

plt.annotate(
    "High prices pull the mean upward",
    xy=(mean_price, 8),
    xytext=(mean_price + 5000, 18),
    arrowprops=dict(arrowstyle="->"),
    fontsize=10
)

plt.annotate(
    "Median is less sensitive to extreme prices",
    xy=(median_price, 5),
    xytext=(median_price - 6000, 24.2),
    arrowprops=dict(arrowstyle="->"),
    fontsize=10
)

plt.legend()

plt.tight_layout()
plt.savefig("q02.png", dpi=300, bbox_inches="tight")
plt.show()