"""
Module for Response Generator, that generates the response for a given content summaries.

This module represents the G3/G_resp (response-generating model), that generate a cumulative response r
backed by sources S.

For simplification purposes, we will use a LLM-based to generate the response.
Probably in prod this is a more complex pipeline.
"""

import instructor
from summary import Summary
from pydantic import BaseModel, Field

class AugmentedResponse(BaseModel):
    """
    Represents the augmented response for a given query.
    """
    response: str = Field(..., description="Response for a given query.")
    sources: list[str] = Field(..., description="Sources used to generate the response.")

RESPONSE_GENERATION_PROMPT = """
You are a Search-Augmented Generation (RAG) engine. 
Your goal is to provide a comprehensive, informative, and detailed answer based ON THE PROVIDED SUMMARIES.

GUIDELINES:
1. EXHAUSTIVE CONTENT: Do not just answer the basic question. Incorporate relevant details from the summaries such as statistics, culture, economy, and infrastructure.
2. CITATIONS: Every factual claim must be followed by a citation in the format [Source Name/URL].
3. STRUCTURE: Use markdown (bolding, lists) to make the response scannable.
4. TONE: Professional, encyclopedic, and helpful.
5. NO EXTERNAL KNOWLEDGE: Use only the information provided in the summaries. If the information isn't there, say you don't know.
"""

class ResponseGenerator:
    def __init__(self, model: str = "groq/openai/gpt-oss-120b"):
        self.client = instructor.from_provider(model=model)

    def generate(self, query: str, summaries: list[Summary]) -> AugmentedResponse:
        """
        Generates the response for a given query based on the summaries.
        """
        print(f"\n\nGenerating response for {query} based on {len(summaries)} summaries\n\n")
        
        user_prompt = f"""
        User Query: ### {query} ###
        Summaries: ### {summaries} ###
        """

        return self.client.chat.completions.create(
            response_model=AugmentedResponse,
            messages=[
                {"role": "system", "content": RESPONSE_GENERATION_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

if __name__ == "__main__":
    generator = ResponseGenerator()
    query = "What is the capital of France?"

    summary_text = """
    Paris, the capital and largest city of France, had an estimated city population of about 2.05 million and a metropolitan population of 13.2 million in January 2026. Situated on the Seine in Île‑de‑France, it is the EU’s fourth‑largest city and is nicknamed the “City of Light.” The city is divided into 20 arrondissements, each with its own identity, and was reshaped in the 19th century by Haussmann’s boulevards and parks. Paris is a major transport hub—home to the EU’s busiest airport (Charles de Gaulle), an extensive railway and motorway network, and a world‑renowned, award‑winning sustainable public‑transport system, including the iconic Art‑Nouveau Métro.

    Culturally, Paris boasts numerous museums (e.g., Musée d’Orsay, Musée Rodin, Musée Picasso) and UNESCO‑listed riverbanks, and it remains a global centre for finance, diplomacy, fashion, and gastronomy. Politically, it hosts the French President, Parliament, and several UN agencies (UNESCO, OECD, IEA, etc.) as well as European bodies like ESA and EBA. The city is a sports hub, staging events such as the French Open, and is home to Paris Saint‑Germain (football) and Stade Français (rugby); it has hosted the Summer Olympics three times.
    """
    summary = Summary(
        summary=summary_text,
        source="https://en.wikipedia.org/wiki/Paris"
    )

    response = generator.generate(query, [summary])
    print(response.response)
    print(response.sources)