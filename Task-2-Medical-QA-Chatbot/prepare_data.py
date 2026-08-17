import os
import xml.etree.ElementTree as ET
import pandas as pd

# Location of the original MedQuAD dataset
DATASET_DIR = "MedQuAD"

# Location for the processed dataset
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "medquad.csv")


def extract_xml_file(xml_file):
    records = []

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Get document-level information
        source = root.attrib.get("source", "")
        document_id = root.attrib.get("id", "")
        url = root.attrib.get("url", "")

        focus_element = root.find("Focus")
        focus = focus_element.text.strip() if focus_element is not None and focus_element.text else ""

        # Find all Question-Answer pairs
        for qa_pair in root.findall(".//QAPair"):

            question_element = qa_pair.find("Question")
            answer_element = qa_pair.find("Answer")

            if question_element is None or answer_element is None:
                continue

            question = question_element.text.strip() if question_element.text else ""
            answer = answer_element.text.strip() if answer_element.text else ""

            qid = question_element.attrib.get("qid", "")
            qtype = question_element.attrib.get("qtype", "")
            pid = qa_pair.attrib.get("pid", "")

            if question and answer:
                records.append({
                    "document_id": document_id,
                    "qid": qid,
                    "pid": pid,
                    "source": source,
                    "focus": focus,
                    "question_type": qtype,
                    "question": question,
                    "answer": answer,
                    "url": url
                })

    except ET.ParseError as e:
        print(f"XML error in {xml_file}: {e}")

    except Exception as e:
        print(f"Error processing {xml_file}: {e}")

    return records


def main():

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_records = []

    print("Starting MedQuAD dataset processing...")
    print()

    # Walk through all folders and files
    for root_dir, dirs, files in os.walk(DATASET_DIR):

        for file in files:

            if file.lower().endswith(".xml"):

                xml_path = os.path.join(root_dir, file)

                records = extract_xml_file(xml_path)

                all_records.extend(records)

    # Convert records to DataFrame
    df = pd.DataFrame(all_records)

    # Save CSV
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print()
    print("==========================================")
    print("MedQuAD processing completed!")
    print("==========================================")
    print(f"Total Q&A pairs: {len(df)}")
    print(f"Output file: {OUTPUT_FILE}")
    print()

    # Display sample data
    if not df.empty:
        print("Dataset columns:")
        print(list(df.columns))
        print()
        print("First 5 records:")
        print(df[["question", "question_type", "focus"]].head())


if __name__ == "__main__":
    main()