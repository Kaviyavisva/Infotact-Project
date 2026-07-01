"""
Prompt Builder module for the Prescriptive Maintenance RAG Agent.
Builds a structured prompt using retrieved document chunks and the user's query.
"""


class PromptBuilder:
    """
    Builds prompts that combine retrieved context with the user's question.
    """

    def __init__(self):
        pass

    def build_prompt(self, query: str, retrieved_chunks: list) -> str:
        """
        Builds a prompt using the retrieved document chunks and the user's query.
        """

        # Combine all retrieved chunks into a single context string
        context = "\n\n".join(retrieved_chunks)

        # Create the prompt
        prompt = f"""
You are an expert maintenance engineer.

Use ONLY the information provided in the context below to answer the user's question.
If the answer is not available in the context, say that the information is not available.

Context:
--------------------
{context}
--------------------

Question:
{query}

Answer:
"""

        return prompt