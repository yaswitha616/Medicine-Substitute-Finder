import os
from flask import Flask, request, render_template
import google.generativeai as genai
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
import pickle
import PIL.Image

app = Flask(__name__)

# --- Load Models and Data ONCE at startup ---
# This part is time-consuming, so we do it only once
try:
    # Configure GenAI
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set!")
    genai.configure(api_key=GOOGLE_API_KEY)
    vision_model = genai.GenerativeModel('gemini-pro-vision')

    # Load Sentence Transformer and data
    df = pd.read_csv("data/medicinedataset.csv")
    transformer_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    with open('models/medicine-embeddings.pkl', "rb") as fIn:
        embeddings = pickle.load(fIn)
except Exception as e:
    print(f"Error loading models or data: {e}")
    # Handle error appropriately in a real app
    
# --- Helper Function for finding substitutes ---
def find_substitutes(prompt, df, model, embeddings):
    try:
        prompt_embedding = model.encode(prompt, convert_to_tensor=True)
        hits = util.semantic_search(prompt_embedding, embeddings, top_k=5)
        if not hits or not hits[0]:
            return "No close substitute found."
        substitute_indices = [hit['corpus_id'] for hit in hits[0]]
        substitute = df.iloc[substitute_indices[0]]['substitutes']
        return substitute
    except Exception as e:
        print(f"Error finding substitute for '{prompt}': {e}")
        return "Error during search."

# --- Web Routes ---
@app.route('/')
def index():
    # Just display the main page
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def handle_image_upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('index.html', title="Error", results={"error": "No file selected."})
    
    file = request.files['file']
    try:
        # 1. Get medicines from image using Gemini
        img = PIL.Image.open(file.stream)
        prompt = "From the provided image, list only the medicine names and their dosages. Separate each medicine with a newline. Exclude all other text."
        response = vision_model.generate_content([prompt, img])
        
        medicines = response.text.strip().split('\n')
        
        # 2. Find alternatives for each medicine
        alternatives = {}
        for medicine in medicines:
            if medicine: # Ensure it's not an empty string
                alternatives[medicine] = find_substitutes(medicine, df, transformer_model, embeddings)
        
        return render_template('index.html', title="Prescription Analysis Results", results=alternatives)
    except Exception as e:
        print(f"Error processing image: {e}")
        return render_template('index.html', title="Error", results={"error": "Could not process the uploaded image."})

@app.route('/find_substitute', methods=['POST'])
def handle_text_input():
    medicine_name = request.form.get('medicine')
    if not medicine_name:
        return render_template('index.html', title="Error", results={"error": "No medicine name entered."})
    
    try:
        # Find substitute for the single medicine
        substitute = find_substitutes(medicine_name, df, transformer_model, embeddings)
        results = {medicine_name: substitute}
        return render_template('index.html', title="Substitute Search Result", results=results)
    except Exception as e:
        print(f"Error processing text input: {e}")
        return render_template('index.html', title="Error", results={"error": "Could not process the request."})

if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible within the Docker container
    app.run(host='0.0.0.0', port=5000)
