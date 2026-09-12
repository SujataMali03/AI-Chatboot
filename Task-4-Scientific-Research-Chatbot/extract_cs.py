import json
import csv
import os

INPUT_FILE = "data/arxiv-metadata-oai-snapshot.json"
OUTPUT_FILE = "data/cs_papers.csv"

# Computer Science categories we want
CS_CATEGORIES = {
    "cs.AI",
    "cs.CL",
    "cs.CV",
    "cs.LG",
    "cs.NE",
    "cs.IR",
    "cs.RO",
    "cs.SE",
    "cs.DS",
    "cs.CC",
    "cs.CR",
    "cs.DB",
    "cs.DC",
    "cs.HC",
    "cs.IT",
    "cs.NI",
    "cs.PL",
    "cs.SI",
    "cs.SY"
}

print("Starting extraction...")
print("Input:", INPUT_FILE)
print("Output:", OUTPUT_FILE)

count = 0
total = 0

with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as outfile:

    writer = csv.writer(outfile)

    # CSV header
    writer.writerow([
        "id",
        "title",
        "authors",
        "abstract",
        "categories",
        "update_date"
    ])

    for line in infile:
        total += 1

        try:
            paper = json.loads(line)

            categories = paper.get("categories", "")
            category_list = categories.split()

            # Keep papers containing at least one selected CS category
            if any(category in CS_CATEGORIES for category in category_list):

                paper_id = paper.get("id", "")
                title = paper.get("title", "").replace("\n", " ").strip()
                authors = paper.get("authors", "").replace("\n", " ").strip()
                abstract = paper.get("abstract", "").replace("\n", " ").strip()
                update_date = paper.get("update_date", "")

                writer.writerow([
                    paper_id,
                    title,
                    authors,
                    abstract,
                    categories,
                    update_date
                ])

                count += 1

                if count % 10000 == 0:
                    print(f"CS papers extracted: {count:,}")

        except json.JSONDecodeError:
            print("Skipping invalid JSON line.")

print("\nExtraction completed!")
print(f"Total papers scanned: {total:,}")
print(f"Computer Science papers: {count:,}")
print(f"Saved to: {OUTPUT_FILE}")