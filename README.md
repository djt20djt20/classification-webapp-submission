# Text Classification App

This is Daniel Taylor's submission. The goal is to build a webapp that can classify text into one of a number of categories, passed into an API. I have also built a frontend that can classify, scrape a webpage and classify that, and extract the text from a PDF and classify that.

# What are the files?
1. **requirements.txt** contains the requirements
2. **evaluate.py** is your file, used to evaluate the API
3. **Development Notebook.ipynb** is the jupyter notebook used to develop the API
4. **test_data** contains all of the test data (case_1.json ...)
5. **src.utility_functions.py** contains the functions to generate the outputs, including the calls to OpenAI
6. **Hello.py** is the first page of the streamlit app
7. **pages.PDF_classifier**... are the extra pages in the streamlit app

# How to evaluate the model
In order to test the model, please follow the following steps:
1. Insert your own API key into line 84 of the **src.utility_functions.py** file
2. Create a new virtual environment
3. Install the requirements in the **requirements.txt** file (pip install -r requirements.txt) 
2. Deploy the API by typing **python api.py** in the command line while in this folder
3. Run **python evaluate.py** to evaluate the api (or run your own script)

# Design choices
1. I chose to make two API calls to OpenAI, one for classification, and another for reason. I did this because I was concerned that one of the main ways the model might fail is if it outputs the wrong code, or outputs the code in an incorrect format. Making two calls made it easier to give clear instructions.
2. I chose to not allow any codes in that are in an incorrect format. It might be possible to programatically extract the classification code, but I thought this would introduce risks as I'd have to think through a lot of edge cases.
3. I chose not to deploy the API. Had I done so, I would have used Heroku or Railway. 
4. I chose not to adjust the prompt for the webscrape and pdf classifier in the front end, this is largely due to lack of time, and also because I don't know what I'm tuning it to do.
5. The prompt was engineered in the utility_functions.py file, and has been formatted for easy experimentation (comment out or add lines where you need them). Some of the biggest gains in performance was made when I instructed the AI to consider the main intention of the query. 
6. The queries are written in markdown to make them easy for a human to read.
7. The output isn't deterministic - one question in test 3 is going between correct and fail -> I've tried setting temperature to 0 and a very low number, and neither mhave fixed it

# Reflection
- If I did this task again, I would have deployed the API somewhere and sent you the link, and would have focussed more on the API rather than the front end, because, with hindsight, I think this is more of what you wanted in the task
- I would also have had seperate repos for the API and the streamlit app, and have the streamlit app call the API, rather than have them bound together like they are now.