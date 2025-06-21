
import os
import json
import networkx as nx
from datetime import datetime
import matplotlib.pyplot as plt

def log(msg):
    print(f"[citation_graph] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def build_citation_graph(data_file="data/clustered_journal_results_" + datetime.now().strftime('%Y%m%d') + ".json"):
    G = nx.DiGraph()
    try:
        with open(data_file, "r") as f:
            entries = json.load(f)
        for i, item in enumerate(entries):
            G.add_node(item['title'], label=item['journal'])
            # Simulated citation connection: link between items in same cluster
            for j, other in enumerate(entries):
                if i != j and item.get("topic_cluster") == other.get("topic_cluster"):
                    G.add_edge(item['title'], other['title'])
        nx.write_gexf(G, "data/citation_graph.gexf")
        log("Citation graph saved to data/citation_graph.gexf")
        return G
    except Exception as e:
        log(f"Failed to generate graph: {e}")
        return None

if __name__ == "__main__":
    build_citation_graph()
