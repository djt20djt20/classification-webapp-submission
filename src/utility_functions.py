import json
import pandas as pd
from openai import OpenAI
import streamlit as st

def create_markdown_prompt(query, df_classes, multilabel):
    """
    Generates a markdown-formatted prompt for querying the OpenAI API based on the user's query and classification options.
    
    Parameters:
        query (str): The user's query to be classified.
        df_classes (pd.DataFrame): A DataFrame containing the details of possible classes including their IDs, names, and descriptions.
        multilabel (bool): A flag indicating whether multiple labels can be applied to the query.
        
    Returns:
        str: A formatted string that serves as a prompt for the OpenAI API to classify the input query.
    """
    prompt = f"## Query\nHere is a user-generated query: **{query}**\n\n"
    prompt += "\n\nYou are going to classify this query."
    prompt += "\n\nYou are going to classify this query based on the context it pertains to (e.g., music, food etc.)."
    prompt += "\n\nConsider the primary action or goal of the query. The user is seeking information on how to perform a task or make something. Classify based on this primary goal."
    #prompt += "\n\nConsider carefully the primary goal of the classification."
    #prompt += "\n\nDo not classify based on purely on casual associations. For example, a query that mentions the place Cheddar in a question about taxes shouldn't be classified as Cheese."
    prompt += "\n\nBelow are the possible classes."
    prompt += "\n\n## Classes and Descriptions\n"
    for index, row in df_classes.iterrows():
        prompt += f"- **Class ID: {row['class_id']}** Class Name:({row['class_name']}): {row['class_description']}\n"
    prompt += "\n## Instructions\nIdentify the main intent of the user's query. Consider the nuances in phrasing that might indicate the user's real intent."
    prompt += "\n\nConsider the negation in user statements carefully. A statement like 'do not send me chocolate' should be classified as a negative response even though it contains affirmative words such as 'do' and 'send'."
    if multilabel:
        prompt += "\n## Notes\nYou can choose multiple class IDs."
        prompt += "\n\nOutput the ClassID codes separated by comma (for example T1, CC1)."
        prompt += "\n\nThe output requirements are very import. Do not output anything else (for example ClassID: T1 or ClassID:T1.)"
        prompt += "\n\nNever output anything else (for example, a word like sausages)."
    else: 
        prompt += "\n\n## Notes\nOnly choose one class ID."
        prompt += "\n\nOutput only the code ClassID code (for example A1)."
        prompt += "\n\nThe output requirements are very import. Never output anything else like ClassID: T1 or ClassID:T1 ."
    prompt += "\n\nIf no choices are acceptable, respond with '<blank>'."
    prompt += "\n\nNever respond with 'No answers are acceptable'."
    #prompt += "\n\nAnswer with what you think the user intends, rather than strict linguistic categories."
    return prompt


def create_reason_prompt(query, df_classes, multilabel, classification):
    """
    Creates a markdown-formatted prompt to request a reasoning explanation for each classification of a query.
    
    Parameters:
        query (str): The user's query that was classified.
        df_classes (pd.DataFrame): A DataFrame containing class details used in the classification.
        multilabel (bool): Indicates if the classification allowed multiple labels.
        classification (str): The classification results provided by the model.
        
    Returns:
        str: A formatted prompt requesting reasoning for the classification decisions made by the model.
    """
    prompt = ""f"## Setup\nWe asked the following question to OpenAI: **{query}** with the following classes and descriptions.\n\n"
    prompt += "## Classes and Descriptions\n"
    for _, row in df_classes.iterrows():
        prompt += f"- **Class ID: {row['class_id']}** Class Name:({row['class_name']}): {row['class_description']}\n"
    prompt += f"\nThe model responded with: **{classification}**"
    if multilabel:
        prompt += "\n\n## Notes\nFor each ClassID in the answer, explain the reason this item was considered relevent."
        prompt += "\n\nRespond with one sentence for each ClassID."
        prompt += "\n\nRespond only in the format: - Class ID 'A1': reason"
        prompt += "\n\nFollow the previous instruction exactly"
        prompt += "\n\nSeperate each sentence with a full stop."
    else:
        prompt += "\n## Notes\nFor the ClassID, explain the reason this item was considered relevent."
        prompt += "\n\nRespond only in the format: - Class ID 'A1': reason"
        prompt += "\n\nFollow the previous instruction exactly"

    return prompt

def query_openai(prompt, temperature = 0, model_name =  "gpt-3.5-turbo"): 
    """
    Queries the OpenAI API with a specified prompt and returns the response.
    
    Parameters:
        prompt (str): The prompt to send to the OpenAI API for processing.
        
    Returns:
        dict: The API response containing the classification results or error message.
    """
    client = OpenAI(api_key=st.secrets['open_ai_key'])
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=temperature,
        )
        if 'choices' not in response or not response['choices']:
            raise ValueError("Invalid response from API: No choices available")
        return response
    except Exception as e:
        return {"error": f"An error occurred when querying the API: {str(e)}"}


def validate_input(payload):
    required_keys = {'query', 'options', 'classes'}
    if not required_keys.issubset(payload.keys()):
        raise ValueError("Missing required keys in the input payload")

    if 'multilabel' not in payload['options']:
        raise ValueError("Missing 'multilabel' in options")

    if not isinstance(payload['classes'], list) or not all('class_id' in cls and 'class_name' in cls for cls in payload['classes']):
        raise ValueError("Classes must be a list of dicts with 'class_id' and 'class_name'")


def process_request(payload, temperature = 0, model_name =  "gpt-3.5-turbo"):
    """
    Processes a classification request by generating appropriate prompts, querying the OpenAI API, and formatting the response.
    
    Parameters:
        payload (str): JSON string containing the user query, classification options, and classes.
        
    Returns:
        dict: A dictionary containing the classification results and any reasoning or errors.
    """
    try:
        validate_input(payload) 
        payload = json.loads(payload)
        if 'show_reasoning' not in payload['options'].keys():
            reasoning = True
        else:
            reasoning = payload['options']['show_reasoning']
        classes = pd.DataFrame(payload['classes'])
        prompt = create_markdown_prompt(payload['query'], classes, payload['options']['multilabel'])
        response = query_openai(prompt,temperature,model_name)
        classification = response.choices[0].message.content
        if classification == '<blank>':
            return {
                        "result": [],
                        "reasoning": "The model found no acceptable classifications"
                    }
        classification = classification.replace(' ', '').split(',')
        if not all([item in classes['class_id'].tolist() for item in classification]):
            return {
                        "result": [],
                        "reasoning": "The model found no acceptable classifications"
                    }
        if not reasoning:
            return {
                "result": classification,
                "reasoning": None
            } 
        else:
            reason_prompt = create_reason_prompt(payload['query'], classes, payload['options']['multilabel'], classification)
            reason_response = query_openai(reason_prompt)
            reason_text = reason_response.choices[0].message.content
            return {
                    "result": classification,
                    "reasoning": reason_text
                  } 
    except Exception as e:
        return {'error': "Unexpected error occurred", "details": str(e)}

