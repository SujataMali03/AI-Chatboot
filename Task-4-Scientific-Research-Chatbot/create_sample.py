import csv

INPUT_FILE = "data/cs_papers.csv"
OUTPUT_FILE = "data/cs_papers_sample.csv"

MAX_PAPERS = 10000

count = 0

with open(INPUT_FILE, "r", encoding="utf-8", newline="") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Copy header
    header = next(reader)
    writer.writerow(header)

    for row in reader:
        writer.writerow(row)

        count += 1

        if count % 1000 == 0:
            print(f"Copied {count:,} papers...")

        if count >= MAX_PAPERS:
            break

print("\nSample dataset created successfully!")
print(f"Papers copied: {count:,}")
print(f"Saved to: {OUTPUT_FILE}")