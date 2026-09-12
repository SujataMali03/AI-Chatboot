import pandas as pd
import re

INPUT_FILE = "data/cs_papers_sample.csv"
OUTPUT_FILE = "data/cs_papers_clean.csv"

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original papers: {len(df):,}")

# --------------------------------------------------
# 1. Remove duplicate papers
# --------------------------------------------------

df = df.drop_duplicates(subset="id")

print(f"After removing duplicates: {len(df):,}")

# --------------------------------------------------
# 2. Remove papers with missing abstracts
# --------------------------------------------------

df = df.dropna(subset=["abstract"])

print(f"After removing missing abstracts: {len(df):,}")

# --------------------------------------------------
# 3. Clean text
# --------------------------------------------------

def clean_text(text):

    text = str(text)

    # Remove new lines
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text


df["title"] = df["title"].apply(clean_text)
df["abstract"] = df["abstract"].apply(clean_text)
df["authors"] = df["authors"].apply(clean_text)
df["categories"] = df["categories"].apply(clean_text)

# --------------------------------------------------
# 4. Remove empty titles
# --------------------------------------------------

df = df[df["title"].str.len() > 0]

# --------------------------------------------------
# 5. Remove very short abstracts
# --------------------------------------------------

df = df[df["abstract"].str.len() > 100]

# --------------------------------------------------
# 6. Save cleaned dataset
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nCleaning completed successfully!")

print(f"Final papers: {len(df):,}")

print(f"Saved to: {OUTPUT_FILE}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst paper:")
print("Title:", df.iloc[0]["title"])
print("Category:", df.iloc[0]["categories"])
print("Abstract:", df.iloc[0]["abstract"][:300])