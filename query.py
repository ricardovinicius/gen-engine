"""
Module for G_qr model, that generates a set of queries for a given user query.

For simplification purposes, we will use a LLM-based to generate the set of queries.
Probably in prod this is a more complex pipeline.
"""

import instructor
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

REFORMULATING_QUERY_PROMPT = """
You are a model specialized in query generation process.

TASK: Generate a set of reformulated queries for a given User Query, to improve the search accuracy, coverage, and relevance.
"""

class ReformulatedQueries(BaseModel):
    """
    Represents the set of reformulated queries.
    """
    queries: list[str] = Field(..., description="List of reformulated queries, to improve the search accuracy, coverage, and relevance.")

class QuerySetGenerator:
    def __init__(self, model: str = "groq/openai/gpt-oss-120b"):
        self.client = instructor.from_provider(model=model)

    def generate_query_set(self, query: str) -> ReformulatedQueries:
        """
        Describes the G_qr function of paper.
        """
        user_prompt = f"""
        User Query: ### {query} ###
        """

        return self.client.chat.completions.create(
            response_model=ReformulatedQueries,
            messages=[
                {"role": "system", "content": REFORMULATING_QUERY_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

if __name__ == "__main__":
    generator = QuerySetGenerator()
    query = "What is the capital of France?"
    result = generator.generate_query_set(query)
    print(result)


