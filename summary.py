"""
Module for G_2 Summarizing Model, that summarizes the given query.

For simplification purposes, we will use a LLM-based to generate the set of summaries Sum_j.
Probably in prod this is a more complex pipeline.
"""

from pydantic import Field
import instructor
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

SUMMARIZING_PROMPT = """
You are a model specialized in summarizing website content.

TASK: 
    You will be given a website content and you need to summarize it.
    The summary should be concise and informative.
    The summary should be in the same language as the website content.
"""

class Summary(BaseModel):
    """
    Represents the summary of a given website content.
    """
    summary: str = Field(..., description="Summary of the website content.")
    source: str = Field(..., description="Source of the website content.")

class SummarizingModel:
    def __init__(self):
        self.client = instructor.from_provider(model="groq/llama-3.3-70b-versatile")

    def summarize(self, content: str, source: str) -> Summary:
        """
        Describes the summarizing model (G2) of the paper.
        """
        print(f"Summarizing content {content[:50]} from {source}\n\n")

        user_prompt = f"""
        Website Content: ### {content} ###
        """

        res = self.client.chat.completions.create(
            response_model=str,
            messages=[
                {"role": "system", "content": SUMMARIZING_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        print(f"\n\nSummary: {res[:50]}\n\n")

        return Summary(summary=res, source=source)

if __name__ == "__main__":
    summarizer = SummarizingModel()
    content = """
    Paris[a] is the capital and largest city of France, with an estimated city population of 2,047,602 in an area of 105.4 km2 (40.7 sq mi), and a metropolitan population of 13,239,090 as of January 2026.[3] Located on the river Seine in the centre of the Île-de-France region, it is the largest metropolitan area and fourth-most populous city in the European Union (EU). Nicknamed the City of Light, partly because of its role in the Age of Enlightenment, Paris has been one of the world's major centres of finance, diplomacy, commerce, culture, fashion, and gastronomy since the 17th century.

    Administratively, Paris is divided into twenty arrondissements (districts), each having their own cultural identity. Haussmann's renovation of Paris, which created new boulevards, parks, and public works, gave birth to a modern city known as the "capital of the 19th century". Paris is a major railway, motorway, and air-transport hub; in 2024 Charles de Gaulle Airport was the EU's busiest airport. Paris has one of the most sustainable transportation systems in the world and is one of only two cities that have received the Sustainable Transport Award twice.[5] Its Art Nouveau-decorated Métro has become a symbol of the city. Paris is known for its museums and architectural landmarks: the Musée d'Orsay, Musée Marmottan Monet, and Musée de l'Orangerie are noted for their collections of French Impressionist art, while the Musée National d'Art Moderne, Musée Rodin, and Musée Picasso are noted for their collections of modern and contemporary art. Parts of the city along the Seine have been designated as a UNESCO World Heritage Site since 1991.

    The President of France and both houses of the French Parliament sit in Paris. Paris is home to several United Nations organisations, including UNESCO, as well as other international organisations such as the OECD, the International Bureau of Weights and Measures (in neighbouring Saint-Cloud), the International Energy Agency, the Organisation internationale de la Francophonie, the International Federation for Human Rights, and the Fédération internationale de l'Automobile, along with European bodies such as the European Space Agency, the European Banking Authority, and the European Securities and Markets Authority. The city hosts many sporting events, such as the French Open, and is the home of the association football club Paris Saint-Germain and the rugby union club Stade Français. Paris has also hosted the Summer Olympics three times. 
    """ # Wikipedia Paris page

    summary = summarizer.summarize(content, "https://en.wikipedia.org/wiki/Paris")
    print(summary.summary)
    print(summary.source)
