import argparse
import json
import os
import re
import pandas as pd
from collections import Counter

def load_skills_dict(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_text(s: str) -> str:
    s = s or ""
    s = s.lower()
    s = re.sub(r"[\r\n]+", " ", s)
    s = re.sub(r"[^a-z0-9+#./\- ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_skills(text: str, skills_dict: dict) -> Counter:
    text = normalize_text(text)
    counts = Counter()
    for cat, skills in skills_dict.items():
        for skill in sorted(skills, key=len, reverse=True):
            pattern = r"(?<![a-z0-9+/#.])" + re.escape(skill) + r"(?![a-z0-9+/#.])"
            if re.search(pattern, text):
                counts[skill] += len(re.findall(pattern, text))
    return counts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw/latest.csv")
    parser.add_argument("--skills", default="analysis/skills_list.json")
    parser.add_argument("--output", default="data/processed/skills_count.csv")
    args = parser.parse_args()

    os.makedirs("data/processed", exist_ok=True)
    df = pd.read_csv(args.input)
    skills_dict = load_skills_dict(args.skills)

    agg = Counter()
    for desc in df["description"].fillna(""):
        agg.update(extract_skills(desc, skills_dict))

    items = sorted(agg.items(), key=lambda x: x[1], reverse=True)
    out_df = pd.DataFrame(items, columns=["skill", "count"])
    out_df.to_csv(args.output, index=False)
    print(f"[analysis] wrote counts to {args.output}")

if __name__ == "__main__":
    main()
