# main.py
import tkinter as tk
from tkinter import scrolledtext
import wikipedia
import pyttsx3
import threading
import requests
from bs4 import BeautifulSoup

# ---------------- Voice Function ----------------
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------- Context Memory ----------------
context_memory = {}

# ---------------- Fetch Wikipedia Info ----------------
def fetch_wiki_info(query):
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Jarvis is fetching information...\n")
    output_text.config(state='disabled')
    root.update()

    wikipedia.set_lang("en")
    try:
        # Keep previous queries in context
        context_memory['last_query'] = query

        # Search Wikipedia first
        results = wikipedia.search(query)
        if not results:
            msg = "Sorry, no Wikipedia results found."
            update_gui(msg)
            speak(msg)
            return

        # Pick first result
        article_title = results[0]

        # Fetch summary
        try:
            summary = wikipedia.summary(article_title, sentences=5)
            page = wikipedia.page(article_title)
            url = page.url
        except wikipedia.DisambiguationError as e:
            article_title = e.options[0]
            summary = wikipedia.summary(article_title, sentences=5)
            page = wikipedia.page(article_title)
            url = page.url

        # Fetch additional snippet from the first paragraph of page HTML
        additional_text = fetch_additional_snippet(url)

        # Combine summaries for a concise, human-like explanation
        final_text = f"{summary}\n\n{additional_text}" if additional_text else summary

        display_text = f"--- Wikipedia: {url} ---\n\n{final_text}"
        update_gui(display_text)
        speak(final_text)

    except wikipedia.PageError:
        msg = "Sorry, I could not find any page for your query."
        update_gui(msg)
        speak(msg)

    except Exception as e:
        msg = f"An unexpected error occurred: {e}"
        update_gui(msg)
        speak(msg)

# ---------------- Fetch additional snippet from Wikipedia HTML ----------------
def fetch_additional_snippet(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        content_div = soup.find("div", class_="mw-parser-output")
        if not content_div:
            return ""
        paragraphs = content_div.find_all("p")
        for p in paragraphs:
            txt = p.get_text().strip()
            if txt and len(txt) > 50:
                return txt
        return ""
    except:
        return ""

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
    thread = threading.Thread(target=fetch_wiki_info, args=(query,))
    thread.start()

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("Enhanced Wikipedia Jarvis")
root.geometry("850x650")

tk.Label(root, text="Ask Jarvis about anything:").pack(pady=5)
entry = tk.Entry(root, width=80)
entry.pack(pady=5)

submit_btn = tk.Button(root, text="Ask Jarvis", command=on_submit)
submit_btn.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, height=35, width=100, state='disabled', wrap='word')
output_text.pack(pady=10)

root.mainloop()
