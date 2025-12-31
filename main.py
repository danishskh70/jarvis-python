# main.py
import tkinter as tk
from tkinter import scrolledtext
import threading
import wikipedia
from transformers import pipeline
import re
import pyttsx3

# ---------------- MEMORY ----------------
context = {
    "topic": None
}

user_preferences = {
    "answer_length": "long",   # long | short
    "tone": "simple"
}

# ---------------- TEXT TO SPEECH ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- SUMMARIZER (LIGHTWEIGHT) ----------------
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-6-6"
)

# ---------------- HELPERS ----------------
def end_on_sentence(text):
    if "." in text:
        return text.rsplit(".", 1)[0] + "."
    return text

def simplify(text):
    replacements = {
        "utilize": "use",
        "approximately": "about",
        "demonstrates": "shows",
        "facilitates": "helps",
        "numerous": "many",
        "individuals": "people",
        "objective": "goal",
        "methodology": "method"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def assistant_tone(text, topic):
    intro = f"Here’s a clear explanation of {topic}:\n\n"
    outro = "\n\nIf you want, you can ask for examples, uses, advantages, or future trends."
    return intro + text + outro

# ---- SAFE TRUNCATION ----
def safe_truncate(text, max_words=650):
    words = text.split()
    return " ".join(words[:max_words])

# ---------------- FOLLOW-UP LOGIC ----------------
FOLLOW_UP_WORDS = {
    "applications", "uses", "examples",
    "advantages", "disadvantages", "future"
}

def normalize_query(query):
    q = query.lower().strip()
    q = re.sub(r"\b(19|20)\d{2}\b", "", q).strip()

    if q in FOLLOW_UP_WORDS and context["topic"]:
        return f"{context['topic']} {q}"

    if q == "ai":
        return "Artificial intelligence"

    if "cors" in q:
        return "Cross-origin resource sharing"

    return query

# ---------------- CORE ASSISTANT ----------------
def fetch_and_respond(query):
    wikipedia.set_lang("en")

    try:
        search_query = normalize_query(query)
        results = wikipedia.search(search_query)

        if not results:
            reply("Sorry, I couldn’t find useful information on that.")
            ask_button.config(state="normal")
            return

        try:
            page = wikipedia.page(results[0])
        except wikipedia.DisambiguationError as e:
            page = wikipedia.page(e.options[0])

        context["topic"] = page.title
        content = page.content

        text = safe_truncate(content, max_words=650)

        if user_preferences["answer_length"] == "long":
            max_len, min_len = 260, 130
        else:
            max_len, min_len = 150, 60

        summary = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )[0]["summary_text"]

        summary = end_on_sentence(simplify(summary))
        final_answer = assistant_tone(summary, context["topic"])

        reply(final_answer)
        speak(summary)

    except Exception as e:
        reply(f"An unexpected error occurred: {e}")

    finally:
        ask_button.config(state="normal")

# ---------------- GUI ----------------
def reply(text):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")

def on_ask():
    query = input_box.get().strip()
    if not query:
        return

    ask_button.config(state="disabled")  # prevent overlap
    threading.Thread(
        target=fetch_and_respond,
        args=(query,),
        daemon=True
    ).start()

root = tk.Tk()
root.title("Jarvis – Personal Assistant")
root.geometry("900x620")

tk.Label(root, text="Ask Jarvis:").pack(pady=5)

input_box = tk.Entry(root, width=85)
input_box.pack(pady=5)

ask_button = tk.Button(root, text="Ask", command=on_ask)
ask_button.pack(pady=5)

output_box = scrolledtext.ScrolledText(
    root,
    height=30,
    width=105,
    wrap="word",
    state="disabled"
)
output_box.pack(pady=10)

root.mainloop()