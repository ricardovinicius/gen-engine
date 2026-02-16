"""
Module for Generative Engine.

This module represents the Generative Engine described in the paper,
as the main component of the system.
"""

from response import AugmentedResponse
from summary import Summary
from search_engine import SearchResult
from response import ResponseGenerator
from query import ReformulatedQueries
from summary import SummarizingModel
from query import QuerySetGenerator
from search_engine import SearchEngine

class GenerativeEngine:
    def __init__(self, 
        query_generator: QuerySetGenerator, 
        search_engine: SearchEngine, 
        summary_generator: SummarizingModel,
        response_generator: ResponseGenerator,
    ):
        self.query_generator = query_generator
        self.search_engine = search_engine
        self.summary_generator = summary_generator
        self.response_generator = response_generator

    def generate(self, query: str) -> AugmentedResponse:
        """
        Generates the answer for a given query.
        """
        query_set: ReformulatedQueries = self.query_generator.generate_query_set(query)
        results: list[SearchResult] = self.search_engine.full_search(query_set)
        summaries: list[Summary] = []
        for result in results:
            summaries.append(self.summary_generator.summarize(result.content, result.url))

        final_response = self.response_generator.generate(query, summaries)

        return final_response

if __name__ == "__main__":
    generator = QuerySetGenerator()
    search_engine = SearchEngine()
    summary_generator = SummarizingModel()
    response_generator = ResponseGenerator()
    engine = GenerativeEngine(generator, search_engine, summary_generator, response_generator)
    response = engine.generate("What is the capital of France?")
    print(f"\n\nResponse: {response.response}\n\n")
    print(f"\n\nSources: {response.sources}\n\n")
