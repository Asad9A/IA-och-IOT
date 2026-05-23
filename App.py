import streamlit as st
import random

st.title("🤖 Enkel Lokal Chatbot")

responses = {
    "hej": ["Hej!", "Hallå!", "Tjena!"],
    "hur mår du": ["Jag mår bra!", "Bra tack!"],
    "vad heter du": ["Jag är en enkel lokal chatbot"],
}

user_input = st.text_input("Skriv något:")

if st.button("Skicka"):

    text = user_input.lower()

    for key in responses:
        if key in text:
            st.write(random.choice(responses[key]))
            break
    else:
        st.write("Jag förstår inte riktigt.")