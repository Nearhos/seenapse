import streamlit as st
from api.snapshot.snapshot_workflow import capture_screenshot, analyze_image_enhanced
from api.describe_image import store_image_embedding, upload_csv_to_rag, answer_with_rag
from api.text_to_speech import speak_text
import streamlit as st
import requests

system_prompt = (
    "You are a compact multimodal assistant used in a real-time Snapshot tool.\n\n"
    "Select ONE best task:\n\n"
    "1) Math: solve and return only the final answer. If there are multiple parts, list each on its own line as (a), (b), ...\n"
    "2) Translation: detect language and return the full English translation only. No extra commentary.\n"
    "3) Image understanding: explain what the image shows and clarify likely confusing elements. "
    "If the image contains text or equations, transcribe the relevant parts and, if applicable, solve or translate them.\n\n"
    "Rules:\n"
    "- Be concise (ideally ≤ 3 sentences unless multiple sub-answers are required).\n"
    "- No preamble, no markdown, no apologies, no chain-of-thought.\n"
    "- Preserve technical symbols, numbers, and proper nouns.\n"
    "- For math: include units; avoid unnecessary rounding; if assumptions are required, state them in one short sentence at the end.\n"
    "- For translation: output the translated text only.\n"
    "- For image: prioritize what the user likely cares about (main subjects, relationships, actions, anomalies, UI labels). Include one brief clarification note only if ambiguity would mislead.\n\n"
    "Output format:\n"
    "- Math → just the final answer (and label parts if needed).\n"
    "- Translation → just the English translation.\n"
    "- Image → 1–3 concise sentences (add a single 'Note: ...' line only if essential).\n\n"
    "Always take into consideration the profile and preferences of the person described in the knowledge base when answering, tailoring your response to their interests and expertise."
)

API_BASE = "http://ngrokurlhere"  # Replace with your FastAPI server address

def fetch_jumping_jacks():
    try:
        resp = requests.get(f"{API_BASE}/latest/jumping_jacks", timeout=1)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        st.error(f"Error fetching jumping jacks: {e}")
    return None

st.title("Snapshot Workflow")
st.divider()

#jumping_jacks = fetch_jumping_jacks()
st.write("Jumping Jacks (snapshot):")
image_path = capture_screenshot()
st.image(image_path, caption="Snapshot Taken", use_container_width=True)

#store_image_embedding(image_path)
st.write(f"Image embedding stored for {image_path}")
#upload_csv_to_rag("api/knowledge_base.csv")
st.write("CSV of knowledge base uploaded and embedded.")
analysis = analyze_image_enhanced(image_path)
rag_answer = answer_with_rag("what is on the image and how is it related to jocelyn" + system_prompt)
st.write("RAG Answer:")
st.write(rag_answer)
speak_text(rag_answer)
st.write("Spoken the RAG answer using TTS from Eleven Labs.")