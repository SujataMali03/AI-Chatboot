from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.units import inch
import re


INPUT_FILE = "PROJECT_REPORT.md"
OUTPUT_FILE = "Dynamic_Knowledge_Base_Chatbot_Report.pdf"


# Read report
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read()


# PDF setup
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=45,
    leftMargin=45,
    topMargin=45,
    bottomMargin=45
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=20,
    leading=25,
    spaceAfter=20
)

heading_style = ParagraphStyle(
    "HeadingCustom",
    parent=styles["Heading1"],
    fontSize=15,
    leading=19,
    spaceBefore=14,
    spaceAfter=8
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=10.5,
    leading=16,
    spaceAfter=7
)

code_style = ParagraphStyle(
    "CodeCustom",
    parent=styles["Code"],
    fontSize=8.5,
    leading=12,
    leftIndent=10,
    rightIndent=10,
    spaceBefore=5,
    spaceAfter=8
)


story = []


def escape_html(value):
    value = value.replace("&", "&amp;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    return value


# Process Markdown
lines = text.splitlines()

in_code = False
code_lines = []


for line in lines:

    # Code block
    if line.strip().startswith("```"):

        if in_code:
            code_text = "<br/>".join(
                escape_html(x) for x in code_lines
            )

            story.append(
                Paragraph(
                    code_text,
                    code_style
                )
            )

            code_lines = []
            in_code = False

        else:
            in_code = True

        continue


    if in_code:
        code_lines.append(line)
        continue


    line = line.strip()

    if not line:
        story.append(Spacer(1, 4))
        continue


    # Main title
    if line.startswith("# "):

        title = line[2:].strip()

        story.append(
            Paragraph(
                escape_html(title),
                title_style
            )
        )


    # Heading
    elif line.startswith("## "):

        heading = line[3:].strip()

        story.append(
            Paragraph(
                escape_html(heading),
                heading_style
            )
        )


    # Subheading
    elif line.startswith("### "):

        heading = line[4:].strip()

        story.append(
            Paragraph(
                escape_html(heading),
                styles["Heading2"]
            )
        )


    # Bullet
    elif line.startswith("- "):

        item = escape_html(line[2:].strip())

        story.append(
            Paragraph(
                "• " + item,
                body_style
            )
        )


    # Numbered list
    elif re.match(r"^\d+\.", line):

        story.append(
            Paragraph(
                escape_html(line),
                body_style
            )
        )


    else:

        # Basic bold Markdown
        line = escape_html(line)

        line = re.sub(
            r"\*\*(.*?)\*\*",
            r"<b>\1</b>",
            line
        )

        story.append(
            Paragraph(
                line,
                body_style
            )
        )


# Build PDF
doc.build(story)

print()
print("==========================================")
print(" PDF REPORT CREATED SUCCESSFULLY")
print("==========================================")
print()
print(f"File: {OUTPUT_FILE}")
print()