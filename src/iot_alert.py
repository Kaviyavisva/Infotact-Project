from src.search_engine import search_query

query = input("Enter your query: ")

results = search_query(query)

print("\nTop 3 Relevant Chunks:\n")

for i, result in enumerate(results, 1):
    print(f"{i}. {result}")
