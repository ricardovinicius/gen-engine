import streamlit as st
import time
from engine import GenerativeEngine
from query import QuerySetGenerator
from search_engine import SearchEngine
from summary import SummarizingModel
from response import ResponseGenerator

st.set_page_config(page_title="Generative Engine", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .stTextInput > div > div > input {
        caret-color: #ff4b4b;
    }
    .stButton > button {
        background-color: #ff4b4b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_engine():
    generator = QuerySetGenerator()
    search_engine = SearchEngine()
    summary_generator = SummarizingModel()
    response_generator = ResponseGenerator()
    return GenerativeEngine(generator, search_engine, summary_generator, response_generator)

def main():
    st.title("Generative Engine 🔍")
    st.markdown("### Ask a question and get a comprehensive answer backed by web search.")
    
    with st.spinner("Initializing engine..."):
        engine = get_engine()

    query = st.text_input("Enter your query:", placeholder="e.g., What is the capital of France?", key="query_input")

    if query:
        st.divider()
        with st.status("Processing query...", expanded=True) as status:
            st.write("Generating response...")
            
            try:
                start_time = time.time()
                response = engine.generate(query)
                end_time = time.time()
                status.update(label=f"Done in {end_time - start_time:.2f}s", state="complete", expanded=False)
                
                st.subheader("Answer")
                st.markdown(response.response)
                
                if response.sources:
                    st.divider()
                    st.subheader("Sources")
                    for i, source in enumerate(response.sources, 1):
                        st.markdown(f"{i}. [{source}]({source})")
                        
            except Exception as e:
                status.update(label="Error occurred", state="error")
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
