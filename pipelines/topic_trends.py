
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

def log(msg):
    print(f"[topic_trends] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def load_all_clustered_files(data_path='data'):
    return sorted([
        f for f in os.listdir(data_path)
        if f.startswith("clustered_") and f.endswith(".json")
    ])

def count_clusters_per_day():
    files = load_all_clustered_files()
    trends = defaultdict(lambda: defaultdict(int))
    for file in files:
        date_str = file.split("_")[-1].split(".")[0]
        with open(os.path.join("data", file), "r") as f:
            items = json.load(f)
        for item in items:
            cluster = str(item.get("topic_cluster", -1))
            trends[date_str][cluster] += 1
    return trends

def plot_trends(trends):
    clusters = sorted(set(k for d in trends.values() for k in d.keys()))
    dates = sorted(trends.keys())

    for cluster in clusters:
        counts = [trends[date].get(cluster, 0) for date in dates]
        plt.plot(dates, counts, label=f"Cluster {cluster}")
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.title("Topic Trends Over Time")
    plt.legend()
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig("outputs/topic_trends.png")
    log("Saved topic trends chart to outputs/topic_trends.png")

if __name__ == "__main__":
    trends = count_clusters_per_day()
    plot_trends(trends)
