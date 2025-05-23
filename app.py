# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bsoSi2k9h455-YGzF-xPULHpDlz-ikJU
"""

# app.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Summarizer function
def summarize_chat_log(text):
    user_messages = []
    ai_messages = []

    lines = text.strip().split('\n')
    for line in lines:
        match = re.match(r"(User|AI)\s*:\s*(.+)", line)
        if match:
            speaker = match.group(1)
            message = match.group(2).strip()
            if speaker == "User":
                user_messages.append(message)
            elif speaker == "AI":
                ai_messages.append(message)

    user_count = len(user_messages)
    ai_count = len(ai_messages)
    exchange_count = user_count + ai_count

    all_text = user_messages + ai_messages
    stop_words = stopwords.words('english')
    tfidf = TfidfVectorizer(stop_words=stop_words, max_features=5)
    tfidf_matrix = tfidf.fit_transform(all_text)
    top_keywords = tfidf.get_feature_names_out()

    if top_keywords.any():
        main_topic = ", ".join(top_keywords[:2])
        topic_summary = f"The user asked mainly about {main_topic} and related topics."
    else:
        topic_summary = "The conversation was general without a clear specific topic."

    return {
        "exchange_count": exchange_count,
        "topic_summary": topic_summary,
        "keywords": list(top_keywords),
        "user_messages": user_messages,
        "ai_messages": ai_messages,
    }

# Streamlit UI
st.title("🧠 AI Chat Log Summarizer")
st.write("Upload a `.txt` file containing a chat log between User and AI.")

uploaded_file = st.file_uploader("Upload Chat Log (.txt)", type="txt")

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    result = summarize_chat_log(content)

    st.subheader("Conversation Summary")
    st.markdown(f"- **Total exchanges**: {result['exchange_count']}")
    st.markdown(f"- **Topic**: {result['topic_summary']}")
    st.markdown(f"- **Top Keywords**: {', '.join(result['keywords'])}")

    st.subheader("Conversation Preview")
    for u, a in zip(result['user_messages'], result['ai_messages']):
        st.text(f"User: {u}")
        st.text(f"AI: {a}")