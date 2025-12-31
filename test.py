# main.py
import tkinter as tk
import wikipedia
import pyttsx3
import threading

# ---------------- Voice Function ----------------
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------- Fetch Wikipedia Info ----------------
def fetch_wiki_info(query):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Jarvis is fetching information from Wikipedia...\n")
    root.update()

    wikipedia.set_lang("en")
    try:
        # Search Wikipedia first to get relevant article
        results = wikipedia.search(query)
        if not results:
            msg = "Sorry, no Wikipedia results found for your query."
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, msg)
            root.update()
            speak(msg)
            return

        # Pick the first search result
        article_title = results[0]

        # Get summary and page URL
        try:
            summary = wikipedia.summary(article_title, sentences=5)
            page = wikipedia.page(article_title)
            url = page.url
        except wikipedia.DisambiguationError as e:
            # Pick first option automatically if disambiguation occurs
            article_title = e.options[0]
            summary = wikipedia.summary(article_title, sentences=5)
            page = wikipedia.page(article_title)
            url = page.url

        # Update GUI
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"--- Wikipedia: {url} ---\n\n{summary}")
        root.update()

        # Speak content
        speak(summary)

    except wikipedia.PageError:
        msg = "Sorry, I could not find any page for your query."
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, msg)
        root.update()
        speak(msg)

    except Exception as e:
        msg = f"An unexpected error occurred: {e}"
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, msg)
        root.update()
        speak(msg)

# ---------------- GUI Callback ----------------
def on_submit():
    query = entry.get()
    thread = threading.Thread(target=fetch_wiki_info, args=(query,))
    thread.start()

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("Wikipedia Jarvis")
root.geometry("800x600")

tk.Label(root, text="Ask Jarvis about anything:").pack(pady=5)
entry = tk.Entry(root, width=80)
entry.pack(pady=5)

submit_btn = tk.Button(root, text="Ask Jarvis", command=on_submit)
submit_btn.pack(pady=5)

output_text = tk.Text(root, height=30, width=95)
output_text.pack(pady=10)

root.mainloop()
