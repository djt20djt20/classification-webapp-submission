import streamlit as st
import requests
from base64 import b64decode
from bs4 import BeautifulSoup
import json
from src import utility_functions
import streamlit as st

def scrape_website(url):
    """Scrape the given URL and return the plain text content."""
    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=(st.secrets['zyte_key'], ""),
        json={"url": url, "httpResponseBody": True}
    )
    http_response_body = b64decode(api_response.json()["httpResponseBody"])
    soup = BeautifulSoup(http_response_body, 'html.parser')
    return soup.get_text(separator='\n', strip=True)


# Page setup
st.title('URL Content Classifier')

# URL input
user_url = st.text_input("Enter the URL to scrape:")

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
if st.button("Scrape and Classify"):
    if user_url and classes:
        scraped_text = scrape_website(user_url)
        scraped_text = 'Here are the contexts of a scraped website: ' + scraped_text
        payload = json.dumps({
            "query": scraped_text,
            "options": {"multilabel": True,
                        "show_reasoning": True},  # Adjust according to your API
            "classes": classes
        })
        result = utility_functions.process_request(payload)
        st.write("Scraped and Classified Content:")
        st.json(result)
    else:
        st.error("Please provide a URL and define at least one category.")

