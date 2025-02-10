import streamlit as st
import openai
import os
from dotenv import load_dotenv


load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")


# Initialize Streamlit chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to generate an image using DALL·E
def generate_image(prompt):
    detailed_prompt = (
        f"A photorealistic, highly detailed product design of {prompt}. "
        "The product should be centered on a pure white background, without any text, labels, or additional elements. "
        "Focus solely on the object, ensuring no diagrams, annotations, or extra features. "
        "The image should look like a high-quality product photo ready for a catalog."
    )
    
    client = openai.Client()
    response = client.images.generate(
        model="dall-e-3",
        prompt=detailed_prompt,
        size="1024x1024"
    )
    
    return response.data[0].url

# Streamlit UI
st.set_page_config(page_title="Biomimetic Chatbot", layout="centered")

st.title("🌱 Biomimetic Design Chatbot")
st.write("Describe a biomimetic concept, and I'll generate the image!")

# Display chat history with Streamlit's built-in chat element
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:  # "assistant"
        with st.chat_message("assistant"):
            st.image(message["content"], use_container_width=True)

# Chat input for user messages (Enter key to send)
user_input = st.chat_input("Enter a biomimetic design concept...")

# Process input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate AI response
    with st.spinner("Generating image..."):
        image_url = generate_image(user_input)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": image_url})
    
    # Display chatbot's response immediately
    with st.chat_message("assistant"):
        st.image(image_url, use_container_width=True)