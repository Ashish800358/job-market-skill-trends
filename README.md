# Job Market Skill Trends Analyzer

An interactive dashboard that analyzes real job postings to reveal the most in-demand skills for data analysts, using live scraping, NLP, and Streamlit visualization.


Scrape job postings from job boards, extract in-demand skills using NLP, and visualize them in an interactive dashboard.

## Quickstart

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python scraper/remoteok_scraper.py --role "data analyst" --location "remote" --limit 200
python analysis/clean_and_extract.py --input data/raw/latest.csv --output data/processed/skills_count.csv

streamlit run app/app.py
```

# from repo root, with venv active
python - <<'PY'
import pandas as pd
df = pd.read_csv("data/raw/latest.csv")
df.head(50).to_csv("sample_jobs.csv", index=False)
print("Wrote sample_jobs.csv")
PY


## Notes
- Initial source: RemoteOK (simple fetch)
- Expand skills list in `analysis/skills_list.json` as needed.
