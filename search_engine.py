"""
Module for Search Engine, that performs the web search operation.

This module emulates a Google-alike search engine. Performs the search operation in Duck Duck Go engine
and return the results.
"""

from query import ReformulatedQueries
from pydantic import BaseModel, Field
import trafilatura
from ddgs import DDGS

MAX_PROCESSED_DOCUMENTS = 5
MAX_WEBPAGE_CONTENT_LENGTH = 10000

class SearchResult(BaseModel):
    """
    Represents the result of a search operation.
    """
    title: str = Field(..., description="Title of the search result.")
    url: str = Field(..., description="URL of the search result.")
    body: str = Field(..., description="Body of the search result.")
    content: str = Field(..., description="Extracted content of website")

class SearchEngine:
    def __init__(self):
        self.ddgs = DDGS()

    def full_search(self, query_set: ReformulatedQueries) -> list[SearchResult]:
        """
        Performs the search operation in Duck Duck Go engine and return the result with content extract from website.
        """
        print(f"\n\nPerforming full search for {query_set.queries}\n\n")
        
        unique_results = {}
        for query in query_set.queries:
            search_output = self.search(query)
            for item in search_output:
                unique_results[item['href']] = item

        print(f"\n\nFound {len(unique_results)} results for {query_set.queries}\n\n")


        for i, result in enumerate(unique_results.values()):
            if i < MAX_PROCESSED_DOCUMENTS:
                result['content'] = self._document_extractor(result['href'])
            else:
                result['content'] = None

        output = []
        for url, result in unique_results.items():
            if result['content'] is not None:
                output.append(SearchResult(title=result['title'], url=result['href'], body=result['body'], content=result['content']))
        
        return output

    def search(self, query: str) -> list[dict]:
        """
        Performs the search operation in Duck Duck Go engine and return the results.
        """
        print(f"\n\nSearching on DDG for {query}\n\n")

        return self.ddgs.text(query, max_results=5)

    def _document_extractor(self, url: str) -> str:
        """
        Extracts the content from a given URL.
        """
        print(f"\n\nExtracting content from {url}\n\n")
        raw_content = trafilatura.fetch_url(url)

        extracted_content = trafilatura.extract(raw_content)
        
        if extracted_content is None:
            return None
        return extracted_content[:MAX_WEBPAGE_CONTENT_LENGTH]

if __name__ == "__main__":
    search_engine = SearchEngine()
    results = search_engine.full_search(ReformulatedQueries(queries=["What is the capital of France?"]))
    print("\n\n")
    print(results[0].body[:100])
    print("\n\n")
    print(results[0].content[:100])
