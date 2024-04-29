# Text Classification App

This is Daniel Taylor's submission. The goal is to build a webapp that can classify text into one of a number of categories, passed into an API. I have also built a frontend that can classify, scrape a webpage and classify that, and extract the text from a PDF and classify that.

# What are the files?
1. **Requirements.txt** contains the requirements
2. **Evaluate.txt** is your file, used to evaluate the API
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
3. I chose not to adjust the prompt for the webscrap and pdf classifier, this is largely due to lack of time, and also because I don't know what I'm tuning it to do.
4. The prompt was engineered in the utility_functions.py file, and has been formatted for easy experimentation (comment out or add lines where you need them). Some of the biggest gains in performance was made when I instructed the ai to consider the main intention of the query. 
5. The queries are written in markdown to make them easy for a human to read.
