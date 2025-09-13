# snapshot.py
# pip install google-generativeai
import os, sys, mimetypes, argparse
import google.generativeai as genai

DEFAULT_MODEL = "gemini-1.5-flash"

def main(image_path: str, model_name: str = DEFAULT_MODEL) -> str:
    """
    Returns the model's answer as a string.
    Raises exceptions on errors instead of exiting the process.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime, _ = mimetypes.guess_type(image_path)
    if not mime:
        mime = "image/jpeg"

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # prompt = (
    #     "You are an assistant.\n"
    #     "If a math problem is given, solve it and return the answer.\n"
    #     "If a non-English text is given, translate it to English and return the entire translation.\n"
    #     "If an image is given, explain what is in the image, what is going on, or anything that may be confusing to the user.\n"
    #     "Try to be as concise as possible while maintaining all the answers and accuracy.\n"
    # )

    prompt = f"""
        You are a compact multimodal assistant used in a real-time Snapshot tool.

        Select ONE best task:

        1) Math: solve and return only the final answer. If there are multiple parts, list each on its own line as (a), (b), ...
        2) Translation: detect language and return the full English translation only. No extra commentary.
        3) Image understanding: explain what the image shows and clarify likely confusing elements. 
        If the image contains text or equations, transcribe the relevant parts and, if applicable, solve or translate them.

        Rules:
        - Be concise (ideally ≤ 3 sentences unless multiple sub-answers are required).
        - No preamble, no markdown, no apologies, no chain-of-thought.
        - Preserve technical symbols, numbers, and proper nouns.
        - For math: include units; avoid unnecessary rounding; if assumptions are required, state them in one short sentence at the end.
        - For translation: output the translated text only.
        - For image: prioritize what the user likely cares about (main subjects, relationships, actions, anomalies, UI labels). Include one brief clarification note only if ambiguity would mislead.

        Output format:
        - Math → just the final answer (and label parts if needed).
        - Translation → just the English translation.
        - Image → 1–3 concise sentences (add a single "Note: ..." line only if essential).
        """


    resp = model.generate_content([prompt, {"mime_type": mime, "data": image_bytes}])
    print((resp.text or "").strip())

# Optional CLI for quick manual testing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snapshot → Gemini")
    parser.add_argument("thought", help="Instruction, e.g. 'translate to English', 'solve', 'describe vibe'")
    parser.add_argument("image", help="Path to an image file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model")
    args = parser.parse_args()
    try:
        print(main(args.thought, args.image, args.model))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
