from flask import Flask, request, jsonify, send_from_directory
from api.quote import generate_quote
from api.tokenization import tokenize_text
from api.summarize import scrape_and_summarize
from api.nl2sql import askquestion
from api.vectorsearch import search
from api.ragapi import ragsearch
from api.ragapi import getresume
from api.dictate import transcribe_audio


from openai import AzureOpenAI
import os

api_key= os.environ.get('API_KEY')
api_base =  os.environ.get('API_BASE') # "https://ai-dictate.openai.azure.com/"  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
api_version = os.environ.get('API_VERSION') # '2023-05-15'  # this might change in the future
deployment_name = os.environ.get('DEPLOYMENT_NAME') # ai-dictate

client = AzureOpenAI(
    azure_endpoint=api_base,
    api_version=api_version,
    api_key = api_key
)

app = Flask(__name__, static_folder='static', static_url_path='/')

@app.route('/quote', methods=['POST'])
def quote():
    return generate_quote(request, client, deployment_name)

@app.route("/tokenize", methods=["POST"])
def tokenize():
    return tokenize_text(request, deployment_name)

@app.route('/summarize', methods=['GET'])
def summarize():
    return scrape_and_summarize(request, client, deployment_name)

@app.route('/ask_question', methods=['POST'])
def ask():    
    return askquestion(request, client, deployment_name)  

@app.route('/vectorsearch', methods=['POST'])
def vectorsearch():
    return search(request)    

@app.route('/rag', methods=['POST'])
def rag():    
    return ragsearch(request, client, deployment_name)   

@app.route('/dictate', methods=['POST'])
def dictate():                                 
    return transcribe_audio(request, client, deployment_name)  

@app.route('/resume', methods=['GET'])
def resume():
    return getresume(request)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)    
