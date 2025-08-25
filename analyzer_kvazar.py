import tkinter as tk
from tkinter import filedialog, messagebox
import string
from collections import Counter
import math
import matplotlib.pyplot as plt
import re

# Funkcije za analizu teksta
def clean_text(text):
    text = text.lower()
    for p in string.punctuation:
        text = text.replace(p, "")
    return text

def count_words(text):
    words = clean_text(text).split()
    return len(words)

def count_sentences(text):
    return text.count(".") + text.count("!") + text.count("?")

def get_sentence_length(text):
    words = count_words(text)
    sentences = count_sentences(text)
    if sentences == 0:
        return 0
    return words / sentences

def most_common_words(text, n=5):
    words = clean_text(text).split()
    counter = Counter(words)
    return counter.most_common(n)


# Enkripcija/Dekriptacija
def encrypt_text(text, shift=3):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

def decrypt_text(text, shift=3):
    return encrypt_text(text, -shift)

# Poređenje tekstova
def cosine_similarity(text1, text2):
    words1 = clean_text(text1).split()
    words2 = clean_text(text2).split()
    all_words = set(words1).union(set(words2))
    vec1 = [words1.count(word) for word in all_words]
    vec2 = [words2.count(word) for word in all_words]
    dot = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    mag1 = math.sqrt(sum(v1 ** 2 for v1 in vec1))
    mag2 = math.sqrt(sum(v2 ** 2 for v2 in vec2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def jaccard_index(text1, text2):
    set1 = set(clean_text(text1).split())
    set2 = set(clean_text(text2).split())
    return len(set1 & set2) / len(set1 | set2)


# Pattern Matching

def find_emails(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}'
    return re.findall(pattern, text)

def find_dates(text):
    pattern = r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b'
    return re.findall(pattern, text)

# GUI aplikacija

class TextAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔹 Analiza Teksta - Kvazari 🔹")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f4f7")

        # Fontovi
        self.title_font = ("Helvetica", 16, "bold")
        self.text_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 11, "bold")
        self.result_font = ("Courier", 11)

        # Naslov
        tk.Label(root, text="🌌 Analiza Teksta", font=self.title_font, bg="#f0f4f7", fg="#9b59b6").pack(pady=10)

        # Text area
        self.text_area = tk.Text(root, wrap="word", height=15, width=70, font=self.text_font, bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.text_area.pack(padx=10, pady=10)

        # Dugmad
        button_frame = tk.Frame(root, bg="#f0f4f7")
        button_frame.pack(pady=10)

        btn_style = {"font": self.button_font, "bg": "#9b59b6", "fg": "white", "activebackground": "#b085d0", "width": 20, "bd":0, "relief":"raised"}

        tk.Button(button_frame, text="Učitaj fajl", command=self.load_file, **btn_style).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Sačuvaj (enkriptovano)", command=self.save_encrypted, **btn_style).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Dekriptuj tekst", command=self.decrypt_current, **btn_style).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Analiziraj tekst", command=self.analyze_text, **btn_style).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Prikaži histogram", command=self.show_histogram, **btn_style).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Poredi tekstove", command=self.compare_texts, **btn_style).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Pronađi obrasce", command=self.find_patterns, **btn_style).grid(row=3, column=0, padx=5, pady=5)

        # Rezultati
        self.result_label = tk.Label(root, text="", justify="left", font=self.result_font, bg="#f3e5f5", fg="#9b59b6", bd=2, relief="sunken", anchor="nw")
        self.result_label.pack(padx=10, pady=10, fill="both", expand=True)

        self.loaded_text = ""
        self.second_text = ""

   
    # Metode GUI

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                self.loaded_text = f.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, self.loaded_text)

    def save_encrypted(self):
        text = self.text_area.get("1.0", tk.END)
        encrypted = encrypt_text(text)
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(encrypted)
            messagebox.showinfo("Sačuvano", "Enkriptovan tekst je sačuvan!")

    def decrypt_current(self):
        text = self.text_area.get("1.0", tk.END)
        decrypted = decrypt_text(text)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, decrypted)

    def analyze_text(self):
        text = self.text_area.get("1.0", tk.END)
        words = count_words(text)
        sentences = count_sentences(text)
        avg_len = get_sentence_length(text)
        common = most_common_words(text)

        result = f"Broj riječi: {words}\n"
        result += f"Broj rečenica: {sentences}\n"
        result += f"Prosječna dužina rečenice: {avg_len:.2f}\n"
        result += "Najčešće riječi:\n"
        for w, c in common:
            result += f" - {w}: {c}\n"

        self.result_label.config(text=result)

    def show_histogram(self):
        text = self.text_area.get("1.0", tk.END)
        common = most_common_words(text, n=5)
        if not common:
            messagebox.showerror("Greška", "Nema dovoljno teksta za histogram.")
            return
        words, counts = zip(*common)

        plt.bar(words, counts, color="#1f4e79")
        plt.title("Top 5 riječi", fontsize=14)
        plt.xlabel("Riječ", fontsize=12)
        plt.ylabel("Frekvencija", fontsize=12)
        plt.show()

    def compare_texts(self):
        if not self.loaded_text:
            messagebox.showerror("Greška", "Prvo učitaj fajl!")
            return
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                self.second_text = f.read()

            cos_sim = cosine_similarity(self.loaded_text, self.second_text)
            jaccard = jaccard_index(self.loaded_text, self.second_text)

            result = f"Cosine similarity: {cos_sim:.3f}\n"
            result += f"Jaccard index: {jaccard:.3f}"
            messagebox.showinfo("Poređenje Tekstova", result)

    def find_patterns(self):
        text = self.text_area.get("1.0", tk.END)
        emails = find_emails(text)
        dates = find_dates(text)

        result = "Pronađeni obrasci:\n"
        if emails:
            result += "E-mail adrese:\n"
            for e in emails:
                result += f" - {e}\n"
        else:
            result += "E-mail adrese: Nema\n"

        if dates:
            result += "Datumi:\n"
            for d in dates:
                result += f" - {d}\n"
        else:
            result += "Datumi: Nema\n"

        self.result_label.config(text=result)


# START PROGRAMA
if __name__ == "__main__":
    root = tk.Tk()
    app = TextAnalyzerApp(root)
    root.mainloop()