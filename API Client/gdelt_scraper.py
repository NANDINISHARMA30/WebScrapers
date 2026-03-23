import requests
import pandas as pd
from collections import Counter

# -----------------------------
# CONFIG
# -----------------------------
BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

PARAMS = {
    "query": "(India OR Delhi) AND (AI OR Technology OR Energy OR Politics)",
    "mode": "ArtList",
    "maxrecords": 50,
    "format": "json",
    "timespan": "1day",
    "lang": "English"
}

# -----------------------------
# FETCH DATA
# -----------------------------
def fetch_data():
    try:
        response = requests.get(BASE_URL, params=PARAMS)
        print("Status:", response.status_code)

        data = response.json()
        return data.get("articles", [])

    except Exception as e:
        print("Error:", e)
        return []

# -----------------------------
# NLP: SIMPLE CATEGORY TAGGING
# -----------------------------
def categorize(title):
    title = title.lower()

    if any(word in title for word in ["ai", "technology", "tech"]):
        return "Tech"
    elif any(word in title for word in ["energy", "coal", "power"]):
        return "Energy"
    elif any(word in title for word in ["minister", "government", "policy"]):
        return "Politics"
    elif any(word in title for word in ["trade", "economy", "business"]):
        return "Business"
    else:
        return "Other"

# -----------------------------
# PROCESS DATA
# -----------------------------
def process_data(articles):
    if not articles:
        print("No data found")
        return None

    df = pd.DataFrame(articles)

    # Select columns safely
    cols = ["title", "url", "sourcecountry", "language", "seendate"]
    df = df[[c for c in cols if c in df.columns]]

    # Remove duplicates
    df.drop_duplicates(subset="title", inplace=True)

    # Add category column
    df["category"] = df["title"].apply(categorize)

    return df

# -----------------------------
# ANALYTICS
# -----------------------------
def analyze(df):
    print("\n📊 CATEGORY DISTRIBUTION:")
    print(df["category"].value_counts())

    print("\n🌍 TOP SOURCE COUNTRIES:")
    print(df["sourcecountry"].value_counts().head())

    # Trending keywords
    words = " ".join(df["title"]).lower().split()
    common_words = Counter(words).most_common(10)

    print("\n🔥 TRENDING WORDS:")
    for word, count in common_words:
        print(f"{word}: {count}")

# -----------------------------
# SAVE
# -----------------------------
def save(df):
    df.to_csv("gdelt_enriched.csv", index=False)
    print("\n✅ Saved as gdelt_enriched.csv")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    articles = fetch_data()
    print(f"\nFetched: {len(articles)} articles")

    df = process_data(articles)

    if df is not None:
        print("\nPreview:\n", df.head())

        analyze(df)
        save(df)