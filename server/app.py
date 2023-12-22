import pandas as pd
import umap.umap_ as umap
from transformers import pipeline
import csv
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer
import os
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import cohere
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

# env reference to COHERE_API_KEY
COHERE_API_KEY = os.environ['COHERE_API_KEY']

app = Flask(__name__)
CORS(app, origins='http://localhost:3000')
co = cohere.Client(COHERE_API_KEY)

transcription_map = {}
with open('df.csv', newline='') as csvfile:
    fragments = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(fragments)
    for row in fragments:
        id, filename, transcription, context, people = row
        transcription_map[transcription] = filename

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
transcriptions = list(transcription_map.keys())
embeddings = model.encode(transcriptions)

embeddings = {transcription_map[paragraph]: embedding for paragraph, embedding in zip(transcriptions, embeddings)}
embeddings.values()

reducer = umap.UMAP()
scaler = StandardScaler()
scaled_data = scaler.fit_transform(list(embeddings.values()))
reduced_data = reducer.fit_transform(scaled_data)

context_map = {}
with open('df.csv', newline='') as csvfile:
    fragments = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(fragments)
    for row in fragments:
        id, filename, transcription, context, people = row
        context_map[context] = filename

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
contexts = list(context_map.keys())
context_embeddings = model.encode(contexts)

context_embeddings = {context_map[paragraph]: embedding for paragraph, embedding in zip(contexts, context_embeddings)}
context_embeddings.values()

c_scaled_data = scaler.fit_transform(list(context_embeddings.values()))
reduced_context_data = reducer.fit_transform(c_scaled_data)

print("finished loading")

@app.route('/api/test', methods=["POST", "GET"])
def test():
    return jsonify({'results': 'successfully loaded test endpoint'})

@app.route('/api/branch', methods=["POST", "GET"])
def branch():
    query = request.form['query']
    user_input_embedding = model.encode(query)

    user_input_embedding = user_input_embedding.reshape(1, -1)

    transcription_similarities = cosine_similarity(user_input_embedding, list(embeddings.values()))
    context_similarities = cosine_similarity(user_input_embedding, list(context_embeddings.values()))

    transcription_weight = 0.6
    context_weight = 0.4

    max_len = max(len(transcription_similarities[0]), len(context_similarities[0]))
    transcription_similarities = np.pad(transcription_similarities, ((0, 0), (0, max_len - len(transcription_similarities[0]))), 'constant')
    context_similarities = np.pad(context_similarities, ((0, 0), (0, max_len - len(context_similarities[0]))), 'constant')

    combined_similarities = (transcription_weight * transcription_similarities + context_weight * context_similarities)

    most_similar_indices = combined_similarities.argsort()[0][::-1]
    most_similar_indices = most_similar_indices[:2]

    ARTICLE = []

    final_similarities = []
    df = pd.read_csv('df.csv')
    for idx in most_similar_indices:
        info = df.iloc[idx]
        # article_dict = {
        #     'context': info.to_dict().get('Context'),
        #     'transcription': info.to_dict().get('Transcription'),
        #     'transcription': info.to_dict().get('Transcription')
        # }
        ARTICLE.append(f"you are a conversational AI that can search through memories, with access to transcripts and visual contexts. answer the query: '{query}', using the visual context: ")
        ARTICLE.append(info.to_dict().get('Context'))
        ARTICLE.append(f"Transcription: ")
        ARTICLE.append(info.to_dict().get('Transcription'))
        if info.to_dict().get('People') != 'no one':
            ARTICLE.append(f"and people's names present in the video: ")
            ARTICLE.append(info.to_dict().get('People'))
        final_similarities.append(info.to_dict())
    
    co_summary = co.summarize(text=' '.join(ARTICLE))

    return jsonify({'results': final_similarities, 'summary': co_summary })


if __name__ == '__main__':
    app.run(debug=True, port=2000)