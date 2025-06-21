
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI()

def load_clustered_data():
    path = "data/clustered_journal_results_" + datetime.now().strftime('%Y%m%d') + ".json"
    with open(path, "r") as f:
        return json.load(f)

def generate_prompt(entry):
    return f"""
Based on the following article:

Title: {entry['title']}
Summary: {entry['summary']}

Suggest a research question and a method to explore this question.
"""

def generate_ideas():
    data = load_clustered_data()
    output = []
    for entry in data[:10]:  # Limit to 10 entries for API quota
        prompt = generate_prompt(entry)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        idea = response.choices[0].message.content.strip()
        output.append({
            "title": entry["title"],
            "idea": idea
        })
    with open("data/enhanced_ideas.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    generate_ideas()
