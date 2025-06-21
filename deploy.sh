
#!/bin/bash

echo "[DEPLOY] Starting weekly pipeline execution..."

# Activate virtual environment
source venv/bin/activate

# Run entire research pipeline
python3 run_all_pipelines.py

# Store to SQLite
python3 pipelines/store_sqlite.py

# Index for semantic search
python3 pipelines/semantic_indexer.py

# Email report if credentials set
python3 pipelines/emailer.py

# Optional: Build citation graph and enhanced ideas
python3 agents/citation_graph.py
python3 agents/draft_assistant.py

echo "[DEPLOY] Weekly automation complete!"
