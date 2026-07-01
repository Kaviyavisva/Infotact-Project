import fitz
import os

# Folder containing manuals
pdf_folder = "data/manuals"

# Output file
output_file = "output/parsed_text.txt"

all_text = ""

# Read all PDF files
for file_name in os.listdir(pdf_folder):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file_name)

        pdf = fitz.open(pdf_path)

        for page in pdf:
            all_text += page.get_text()

        pdf.close()

# Save extracted text
with open(output_file, "w", encoding="utf-8") as file:
    file.write(all_text)

print("PDF parsing completed successfully!")