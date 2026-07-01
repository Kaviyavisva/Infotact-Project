from src.prompt_builder import PromptBuilder

# Create PromptBuilder object
builder = PromptBuilder()

# Sample user query
query = "Why is the machine vibrating excessively?"

# Sample retrieved chunks
retrieved_chunks = [
    "Bearings require regular lubrication.",
    "High vibration may indicate bearing wear.",
    "Temperature increase can occur due to friction."
]

# Build the prompt
prompt = builder.build_prompt(query, retrieved_chunks)

# Print the prompt
print(prompt)