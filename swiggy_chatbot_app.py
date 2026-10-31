import os
import re
import pandas as pd
import streamlit as st
from langchain_xai import ChatXAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Page config
st.set_page_config(
    page_title="Swiggy Restaurant Q&A",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better look
st.markdown("""
<style>
    .stChatMessage { font-size: 1.05rem; }
    .block-container { padding-top: 1.5rem; }
    h1 { color: #fc8019; }
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Swiggy Restaurant Q&A Chatbot")
st.caption("Ask anything about restaurants in Koramangala, HSR, BTM & nearby areas")

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("XAI API Key", type="password", help="Get it from https://console.x.ai/")
    if api_key:
        os.environ["XAI_API_KEY"] = api_key
        st.success("API key set")
    else:
        st.warning("Enter your XAI API key to start chatting")

    st.divider()
    st.markdown("**Example questions**")
    examples = [
        "Highest rated restaurants in Koramangala?",
        "Biryani places under Rs.400",
        "Which area has the most restaurants?",
        "Best value North Indian restaurants",
        "Ice cream shops with rating above 4.5",
        "Average cost for two in HSR",
        "Compare biryani options in Koramangala vs BTM"
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.example_query = ex

# Load data (cached)
@st.cache_data
def load_data():
    # Try both possible locations
    for path in [
        "swiggy_cleaned-2.csv",
        "swiggy_cleaned.csv",
        "swiggy_cleaned-2.csv",
        "swiggy_cleaned.csv"
    ]:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    st.error("Cleaned CSV not found. Please place swiggy_cleaned-2.csv in the same folder.")
    return None

df = load_data()

if df is None:
    st.stop()

# Create chunks
@st.cache_data
def create_chunks(df):
    def row_to_chunk(row):
        rating = row['Rating'] if pd.notna(row['Rating']) else "Not available"
        return (
            f"Restaurant: {row['Shop_Name']}. "
            f"Cuisines: {row['Cuisine']}. "
            f"Location: {row['Location']}. "
            f"Area: {row['Area']}. "
            f"Rating: {rating}. "
            f"Cost for Two: Rs.{row['Cost_for_Two']}. "
            f"Cost Bucket: {row['Cost_Bucket']}."
        )
    return [row_to_chunk(row) for _, row in df.iterrows()]

chunks = create_chunks(df)

# Retrieval function
def retrieve_chunks(query: str, chunks: list, top_k: int = 10):
    query_lower = query.lower()
    query_words = set(re.findall(r'\w+', query_lower))
    
    scored = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        matches = sum(1 for w in query_words if w in chunk_lower and len(w) > 2)
        if matches > 0:
            scored.append((matches, chunk))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [chunk for _, chunk in scored[:top_k]]
    
    if not top_chunks:
        top_chunks = chunks[:top_k]
    
    return top_chunks

# Improved prompt
SYSTEM_MSG = """You are an expert data analyst assistant specializing in restaurant data from Swiggy (Bangalore areas: Koramangala, HSR, BTM, Jayanagar).

You answer questions using ONLY the restaurant data provided in the context. Do not invent data.

## How to Handle Questions

**For simple lookups** (specific restaurant, rating, cost):
- Answer directly with the facts.

**For complex / analytical questions** (comparisons, rankings, aggregations, filters, "best", "average", "how many", "which area", multi-condition):
1. Carefully analyze the relevant restaurant records in the context.
2. Perform the required filtering, counting, sorting, or calculation mentally.
3. Present a clear, structured answer.
4. When listing restaurants, use a clean format (bullet or numbered list) showing: Name | Area | Rating | Cost for Two.
5. If you calculate averages, counts, or comparisons, briefly show your reasoning or the key numbers.

**Rules**:
- Prefer precise numbers over vague statements.
- If the data is insufficient to fully answer, say what you can answer and what is missing.
- Use "Rs." for costs.
- Keep answers concise but complete.
- If multiple restaurants match, list the top relevant ones (usually up to 8–10).
- For "best value" or similar: consider both high rating and lower cost.
- Never make up restaurants, ratings, or costs that are not in the provided data.

Always base your answer strictly on the restaurant records given."""

HUMAN_MSG = """Restaurant Records:
{context}

Question: {question}

Think step by step if the question is complex, then provide the final answer:"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle example query from sidebar
if "example_query" in st.session_state:
    prompt = st.session_state.example_query
    del st.session_state.example_query
else:
    prompt = st.chat_input("Ask about restaurants (e.g. best biryani under 400)...")

if prompt:
    if not api_key and not os.getenv("XAI_API_KEY"):
        st.error("Please enter your XAI API Key in the sidebar first.")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing restaurant data..."):
            try:
                llm = ChatXAI(
                    model="grok-4-latest",
                    temperature=0.1,
                    max_tokens=1500
                )

                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", SYSTEM_MSG),
                    ("human", HUMAN_MSG)
                ])

                chain = prompt_template | llm | StrOutputParser()

                relevant = retrieve_chunks(prompt, chunks, top_k=12)
                context = "\n".join(relevant)

                response = chain.invoke({
                    "context": context,
                    "question": prompt
                })

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                error_msg = f"Error: {str(e)}\n\nPlease check your API key and try again."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer info
with st.sidebar:
    st.divider()
    st.caption(f"📊 Dataset: {len(df)} restaurants")
    st.caption(f"Areas: {', '.join(df['Area'].unique())}")
