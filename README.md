# Job Market Skill Trends Analyzer

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

## Notes
- Initial source: RemoteOK (simple fetch)
- Expand skills list in `analysis/skills_list.json` as needed.
