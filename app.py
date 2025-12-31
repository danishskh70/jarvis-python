# main.py
import tkinter as tk
from tkinter import scrolledtext
import wikipedia
import pyttsx3
import threading
from transformers import pipeline

# ---------------- Voice Function ----------------
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------- Load smaller summarizer ----------------
# This model is ~300 MB, CPU-friendly
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")

# ---------------- Context Memory ----------------
context_memory = {}

# ---------------- Fetch and Summarize Wikipedia ----------------
def fetch_and_summarize(query):
    update_gui("Jarvis is fetching information from Wikipedia...\n")
    wikipedia.set_lang("en")

    try:
        context_memory['last_query'] = query

        # Search Wikipedia
        results = wikipedia.search(query)
        if not results:
            msg = "Sorry, no Wikipedia results found."
            update_gui(msg)
            speak(msg)
            return

        article_title = results[0]

        try:
            content = wikipedia.page(article_title).content
            url = wikipedia.page(article_title).url
        except wikipedia.DisambiguationError as e:
            article_title = e.options[0]
            content = wikipedia.page(article_title).content
            url = wikipedia.page(article_title).url

        # Keep first 500–600 words for summarization
        content_excerpt = " ".join(content.split()[:600]).strip()

        # If content too short, skip summarization
        if len(content_excerpt.split()) < 50:
            summary = content_excerpt
        else:
            summary = summarizer(
                content_excerpt, max_length=120, min_length=30, do_sample=False
            )[0]['summary_text']

        display_text = f"--- Wikipedia: {url} ---\n\n{summary}"
        update_gui(display_text)
        speak(summary)

    except wikipedia.PageError:
        msg = "Sorry, I could not find any page for your query."
        update_gui(msg)
        speak(msg)

    except Exception as e:
        msg = f"An unexpected error occurred: {e}"
        update_gui(msg)
        speak(msg)

# ---------------- Thread-safe GUI update ----------------
def update_gui(text):
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state='disabled')
    root.update()

# ---------------- GUI Callback ----------------
def on_submit():
    query = entry.get()
    thread = threading.Thread(target=fetch_and_summarize, args=(query,))
    thread.start()

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("Optimized AI-Style Wikipedia Jarvis")
root.geometry("850x650")

tk.Label(root, text="Ask Jarvis about anything:").pack(pady=5)
entry = tk.Entry(root, width=80)
entry.pack(pady=5)

submit_btn = tk.Button(root, text="Ask Jarvis", command=on_submit)
submit_btn.pack(pady=5)

output_text = scrolledtext.ScrolledText(
    root, height=35, width=100, state='disabled', wrap='word'
)
output_text.pack(pady=10)

root.mainloop()
