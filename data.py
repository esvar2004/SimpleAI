from openai import OpenAI
import streamlit as st
import pandas as pd
client = OpenAI(api_key = '')

def load_data(file):
    data = pd.read_csv(file, low_memory = False)
    return data

def query_dataset(query, data):
    prompt = (
        f"Given the following columns of the provided dataset: {', '.join(data.columns)}, {query}."
        f"Analyze the dataset to find the specific result that the user is asking for."
        #f"Explain the process of how you derived the result using the actual data."
        #f"In your explanation, remember to display the actual values the user is looking for, not placeholders."
        f"Make sure to provide the exact values from the dataset, not placeholders."
        f"Conclude your response with the precise answer derived from the data."
        f"If the query isn't related to the dataset the user is querying, tell them the information isn't available."
    )

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You have to perform analytics on the dataset I will be providing and return the correct answer to the user's query."},
            {"role": "user", "content": prompt}
        ]
    )

    completion = response.choices[0].message.content
    return completion

st.title('Querying Dataset with Plain English')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)
    st.write("Preview of the Dataset:")
    st.write(data.head())

    # User input for queries
    query = st.text_input('What is your query?')

    if query:
        result = query_dataset(query, data)
        st.write(result)