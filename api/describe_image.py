import cv2
import numpy as np
from mss import mss
from datetime import datetime
from PIL import Image
import os
from dotenv import load_dotenv
import cohere
from pymongo import MongoClient
import base64
from io import BytesIO
import pandas as pd

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
co = cohere.ClientV2(COHERE_API_KEY) if COHERE_API_KEY else None

def get_mongo():
    client = MongoClient(MONGODB_URI)
    db = client["rag_db"]
    return db

def capture_screenshot():
    """Capture a screenshot and save as image file"""
    sct = mss()
    monitor = {"top": 140, "left": 25, "width": 400, "height": 600}
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Screenshot saved as: {filename}")
    return filename

def image_to_base64(img_path):
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"

def embed_image(img_path):
    if not co:
        raise ValueError("COHERE_API_KEY not found in environment variables")
    base64_img = image_to_base64(img_path)  
    res = co.embed(
        model="embed-v4.0",
        input_type="search_document",
        embedding_types=["float"],
        images=[base64_img],  
    )
    return res.embeddings.float[0]

def store_image_embedding(img_path, metadata=None):
    db = get_mongo()
    embedding = embed_image(img_path)
    doc = {
        "image_path": img_path,
        "embedding": embedding,
        "metadata": metadata or {},
    }
    result = db["image_embeddings"].insert_one(doc)
    print(f"Stored image embedding for {img_path} with _id: {result.inserted_id}")
    return result.inserted_id

def embed_text(text):
    if not co:
        raise ValueError("COHERE_API_KEY not found in environment variables")
    res = co.embed(
        model="embed-v4.0",
        input_type="search_document",
        embedding_types=["float"],
        texts=[text],
    )
    return res.embeddings.float[0]

def store_text_embedding(text, metadata=None):
    db = get_mongo()
    embedding = embed_text(text)
    doc = {
        "text": text,
        "embedding": embedding,
        "metadata": metadata or {},
    }
    result = db["text_embeddings"].insert_one(doc)
    print(f"Stored text embedding with _id: {result.inserted_id}")
    return result.inserted_id

def upload_csv_to_rag(csv_path):
    """Embed all rows from a CSV and store in MongoDB"""
    df = pd.read_csv(csv_path, delimiter=",", encoding="utf-8", engine="python")
    for idx, row in df.iterrows():
        text = str(row.get("content", "")).strip()
        metadata = row.to_dict()
        store_text_embedding(text, metadata)
    print(f"Uploaded and embedded CSV: {csv_path}")

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

def answer_with_rag(prompt, top_n=2):
    """
    Answer a question using RAG with Cohere and context from MongoDB (images + text).
    """
    # Embed the query
    query_emb = co.embed(
        model="embed-v4.0",
        input_type="search_query",
        texts=[prompt],
        embedding_types=["float"],
    ).embeddings.float[0]

    db = get_mongo()
    image_docs = list(db["image_embeddings"].find({}))
    text_docs = list(db["text_embeddings"].find({}))

    # Score images
    image_scores = []
    for doc in image_docs:
        score = cosine_similarity(query_emb, doc["embedding"])
        image_scores.append((score, doc))
    image_scores.sort(reverse=True, key=lambda x: x[0])

    # Score texts
    text_scores = []
    for doc in text_docs:
        score = cosine_similarity(query_emb, doc["embedding"])
        text_scores.append((score, doc))
    text_scores.sort(reverse=True, key=lambda x: x[0])

    # Get top N from each
    top_images = [doc for _, doc in image_scores[:top_n]]
    top_texts = [doc for _, doc in text_scores[:top_n]]

    # Prepare context for Cohere
    context = []
    for doc in top_texts:
        context.append({"type": "text", "text": doc["text"]})
    for doc in top_images:
        base64_img = image_to_base64(doc["image_path"])
        context.append({"type": "image_url", "image_url": {"url": base64_img}})

    # Generate answer
    response = co.chat(
        model="command-a-vision-07-2025",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}] + context
            }
        ]
    )
    answer = response.message.content[0].text if response.message.content else ""
    print("RAG Answer:", answer)
    return answer

# Example usage:
# img_path = capture_screenshot()
# store_image_embedding(img_path)
# upload_csv_to_rag("knowledge_base.csv")
# answer_with_rag("Who is jocelyn?")