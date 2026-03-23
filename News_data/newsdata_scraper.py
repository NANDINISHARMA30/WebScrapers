import requests
import pandas as pd
import time

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "pub_a7b3a8270eb7462395f9ec7152028449"
BASE_URL = "https://newsdata.io/api/1/latest"

params = {
    "apikey": API_KEY,
    "q": "India AI",
    "language": "en",
    "country": "in"
}

all_articles = []
next_page = None

# -----------------------------
# FETCH MULTIPLE PAGES
# -----------------------------
while len(all_articles) < 200:
    if next_page:
        params["page"] = next_page

    response = requests.get(BASE_URL, params=params)
    print("Status:", response.status_code)

    data = response.json()

    articles = data.get("results", [])
    next_page = data.get("nextPage")

    if not articles:
        break

    all_articles.extend(articles)

    print(f"Collected: {len(all_articles)} articles")

    if not next_page:
        break

    time.sleep(1)  # avoid rate limits

# -----------------------------
# PROCESS DATA
# -----------------------------
df = pd.DataFrame(all_articles)

cols = ["title", "link", "source_id", "country", "language", "pubDate"]
df = df[[c for c in cols if c in df.columns]]

# Remove duplicates
df.drop_duplicates(subset="title", inplace=True)

# Keep only first 200
df = df.head(200)

# -----------------------------
# SAVE
# -----------------------------
df.to_csv("newsdata_50.csv", index=False)

print("\n✅ Saved 50+ articles to newsdata_50.csv")
print("\nPreview:\n", df.head())