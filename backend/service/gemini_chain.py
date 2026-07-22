import os 
from google import genai
from dotenv import load_dotenv
from backend.service.vector_store import VectorStore

load_dotenv()  # Load environment variables from .env file


system_message=(
    
    """
    You are an AI shopping assistant.

Rules:

1. Answer only what the user asks.
2. Keep responses short and natural.
3. If user asks price → give only price.
4. If user asks description → give description.
5. If user asks recommendation → provide comparisons.
6. Do not dump unnecessary information.
7. Sound like a real shopping assistant.
    

    """
)

def get_relevant_context(query):
    results = VectorStore.similarity_search(query, k=5)

    if not results:
        return "No relevant products found."

    context = ""

    for result in results:
        metadata = result.metadata
        # print("PAGE:", result.page_content)
        # print("META:", result.metadata)
        # print(result.metadata)
        context += f"""
Product Name: {metadata.get('ProductName', 'N/A')}
Brand: {metadata.get('ProductBrand', 'N/A')}
Price: ₹{metadata.get('Price', 'N/A')}
Gender: {metadata.get('Gender', 'N/A')}
Description: {result.page_content}

"""

    return context

import time

def generate_response(query, history):
    t = time.time()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    print("Client created:", time.time() - t)

    history.append(f"User: {query}")

    t = time.time()
    context = get_relevant_context(query)
    print("Context fetched:", time.time() - t)

    prompt = (
        system_message
        + "\n".join(history)
        + f"\n\nContext:\n{context}\n\nUser: {query}\nAssistant:"
    )

    t = time.time()
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )
    print("Gemini response:", time.time() - t)

    history.append(f"Assistant: {response.text}")

    return response.text, history