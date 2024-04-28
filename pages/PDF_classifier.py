import streamlit as st
import pdfplumber
import requests
import json
from src import utility_functions

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

# Page setup
st.title("PDF Document Classifier")

# File uploader allows user to add their own PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Dynamic input for classes
st.subheader("Define Classification Classes")
num_classes = st.number_input("Number of Classes", min_value=1, value=2, step=1)
classes = []

for i in range(int(num_classes)):
    with st.expander(f"Class {i+1}"):
        class_id = st.text_input(f"Class ID {i+1}", value=f"C{i+1}")
        class_name = st.text_input(f"Class Name {i+1}", value=f"Class {i+1}")
        class_description = st.text_area(f"Class Description {i+1}", value=f"Description of class {i+1}")
        classes.append({
            "class_id": class_id,
            "class_name": class_name,
            "class_description": class_description
        })

if st.button("Classify PDF"):
    if uploaded_file is not None and classes:
        text = extract_text_from_pdf(uploaded_file)
        text = 'Here are the contexts of a PDF: ' + text
        payload = json.dumps({
            "query": text,
            "options": {"multilabel": True,
                        "show_reasoning": True},  # Adjust according to your API
            "classes": classes
        })
        result = utility_functions.process_request(payload)
        st.write("Classification Results:")
        st.json(result)
    else:
        st.error("Please upload a PDF file and define at least one class.")

