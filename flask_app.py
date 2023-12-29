import openai
import json
import os
from flask import Flask, render_template, request

# Function to load data from a JSON file
def load_data(filename='data/papers_data.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to process the user's query (can be extended for more processing)
def process_query(query):
    return query

# Function to generate an answer using OpenAI's API
def generate_answer(query, data, openai_api_key):
    openai.api_key = openai_api_key

    # Build a prompt for the OpenAI API by including the user's question
    prompt = f"{query}\n\nRelevant Information:\n"
    for paper in data:
        prompt += f"Title: {paper['title']}\nSummary: {paper['summary']}\n\n"

    # Use the OpenAI API to generate a text-based answer
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Load your OpenAI API key from an environment variable
openai_api_key = os.getenv("openai_api_key")
if not openai_api_key:
    print("OpenAI API key not found. Please set the 'openai_api_key' environment variable.")
else:
    print("OpenAI API key loaded successfully.")

# Load the processed papers data from the JSON file
papers_data = load_data()

# Create a Flask web application
app = Flask(__name__)

# Define a route for the home page (both GET and POST requests)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the user's question from the form submitted on the webpage
        user_question = request.form['question']

        try:
            # Generate an answer using OpenAI's API
            answer = generate_answer(user_question, papers_data, openai_api_key)
        except:
            # Handle exceptions (e.g., invalid OpenAI API key)
            answer = 'Please check your OpenAI API key.'

        # Render the HTML template with the user's question and the answer
        return render_template('index.html', question=user_question, answer=answer)
    
    return render_template('index.html')

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)