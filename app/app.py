import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Job Skill Trends", layout="wide")

st.title("Job Market Skill Trends")
st.write("Upload a scraped CSV (or use the default) and view top skills.")

default_csv = "data/raw/latest.csv"
uploaded = st.file_uploader("Upload jobs CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
elif os.path.exists(default_csv):
    df = pd.read_csv(default_csv)
else:
    st.warning("No data found. Run the scraper first.")
    st.stop()

st.subheader("Sample of scraped jobs")
st.dataframe(df.head(20))

if st.button("Compute Top Skills"):
    import json, re
    from collections import Counter

    def normalize_text(s):
        s = s or ""
        s = s.lower()
        s = re.sub(r"[\r\n]+", " ", s)
        # Put '-' at the end and allow whitespace via \s
        s = re.sub(r"[^a-z0-9+#./\s-]", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s


    with open("analysis/skills_list.json", "r", encoding="utf-8") as f:
        skills_dict = json.load(f)

    agg = Counter()
    for desc in df["description"].fillna(""):
        text = normalize_text(desc)
        for cat, skills in skills_dict.items():
            for skill in sorted(skills, key=len, reverse=True):
                pattern = r"(?<![a-z0-9+/#.])" + re.escape(skill) + r"(?![a-z0-9+/#.])"
                matches = re.findall(pattern, text)
                if matches:
                    agg[skill] += len(matches)

    if not agg:
        st.info("No skills found. Edit skills_list.json.")
    else:
        out_df = pd.DataFrame(sorted(agg.items(), key=lambda x: x[1], reverse=True), columns=["skill","count"])
        st.subheader("Top Skills")
        st.bar_chart(out_df.set_index("skill").head(20))
        st.dataframe(out_df.head(50))
