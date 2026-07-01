from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

# Read parsed text
with open("..\Input\parsed_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Create splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Split text
chunks = text_splitter.split_text(text)

# Save chunks
with open("..\Output\chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4)

print(f"{len(chunks)} chunks created successfully!")