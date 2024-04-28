import streamlit as st
from src import utility_functions
import json

def parse_input(json_input):
    try:
        data = json.loads(json_input)
        return data, None
    except json.JSONDecodeError as e:
        return None, str(e)
    
st.title('Text Classification App')

user_query = st.text_input("Enter your text here:")

options = {"multilabel": st.checkbox("Allow multiple labels"),
           "show_reasoning": True}

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

if st.button("Classify"):
    if user_query and classes:
        payload = json.dumps({
            "query": user_query,
            "options": options,
            "classes": classes
        })
        #st.text("JSON payload to be sent:")
        #st.write(payload)
        st.subheader("Result")
        result = utility_functions.process_request(payload)
        st.write(result)
    else:
        st.error("Please enter the query and define at least one class.")
