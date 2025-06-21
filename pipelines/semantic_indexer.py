
import os
import json
import pickle
from datetime import datetime
from sentence_transformers import SentenceTransformer

def log(msg):
    print(f"[semantic_indexer] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def embed_summaries(json_path, model_name="all-MiniLM-L6-v2"):
    with open(json_path, "r") as f:
        data = json.load(f)
    summaries = [entry.get("summary", "") for entry in data]
    model = SentenceTransformer(model_name)
    embeddings = model.encode(summaries)
    output_path = "data/summary_embeddings.pkl"
    with open(output_path, "wb") as f:
        pickle.dump({"embeddings": embeddings, "data": data}, f)
    log(f"Saved semantic index to {output_path}")

if __name__ == "__main__":
    path = "data/clustered_journal_results_" + datetime.now().strftime("%Y%m%d") + ".json"
    embed_summaries(path)
