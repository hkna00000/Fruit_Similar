import flask
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import hnswlib
import pickle

# Load the saved encoder model
encoder = load_model("fruit_encoder_model")

# Initialize and load the HNSW index
f = 1280  # Replace with the actual feature dimension of your embeddings
hnsw_model = hnswlib.Index(space='cosine', dim=f)
hnsw_model.load_index("fruit_hnsw_index.bin")

# Load the index-to-names mapping
with open("index2names.pkl", "rb") as f:
    index2names = pickle.load(f)

# Reinitialize the HNSW object
class HNSW:
    start = 0
    model = None
    index2names = {}

    def __init__(self, model, images):
        self.model = model
        self.index2names = index2names

hnsw = HNSW(hnsw_model, [])

def predict(image_path, encoder, hnsw, k=5):
    # Load and preprocess the image
    img_size = 224
    image = cv2.imread(image_path)
    image = cv2.resize(image, (img_size, img_size))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    
    # Get embeddings
    embeddings = encoder.predict(image)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    # Query the HNSW index
    labels, distances = hnsw.model.knn_query(embeddings, k=k)
    results = [[hnsw.index2names[val] for val in label] for label in labels]
    return results

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'Fruits_Data'  # Replace with the folder containing your dataset images
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Predict similar images
    predictions = predict(filepath, encoder, hnsw)
    # Return filenames with the relative path (without "/images/")
    result_paths = [f'/Fruits_Data/{img_name}' for img_name in predictions[0]]
    return jsonify({'similar_images': result_paths})

# Route to serve images directly from the 'Fruits_Data' folder
@app.route('/Fruits_Data/<path:filename>')
def serve_fruits_data(filename):
    return send_from_directory(DATA_FOLDER, filename)
if __name__ == "__main__":
    app.run(debug=True)