import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("800x500")

        self.books = []
        self.load_data()

        # Поля ввода
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=2)
        self.title_entry = tk.Entry(input_frame, width=20)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Автор:").grid(row=0, column=2, padx=5, pady=2)
        self.author_entry = tk.Entry(input_frame, width=20)
        self.author_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=4, padx=5, pady=2)
        self.genre_entry = tk.Entry(input_frame, width=15)
        self.genre_entry.grid(row=0, column=5, padx=5, pady=2)

        tk.Label(input_frame, text="Страниц:").grid(row=0, column=6, padx=5, pady=2)
        self.pages_entry = tk.Entry(input_frame, width=10)
        self.pages_entry.grid(row=0, column=7, padx=5, pady=2)

        # Кнопка добавления
        add_btn = tk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        add_btn.grid(row=0, column=8, padx=10, pady=2)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5)
        self.genre_filter.bind("<KeyRelease>", self.apply_filters)

        tk.Label(filter_frame, text="Страниц >").grid(row=0, column=2, padx=5)
        self.pages_filter = tk.Entry(filter_frame, width=10)
        self.pages_filter.grid(row=0, column=3, padx=5)
        self.pages_filter.bind("<KeyRelease>", self.apply_filters)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.update_table()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages_str:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        if not pages_str.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        pages = int(pages_str)
        self.books.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        })
        self.save_data()
        self.clear_inputs()
        self.update_table()

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def apply_filters(self, event=None):
        self.update_table()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        genre_filter = self.genre_filter.get().strip().lower()
        pages_filter = self.pages_filter.get().strip()

        for book in self.books:
            if genre_filter and genre_filter not in book["genre"].lower():
                continue
            if pages_filter:
                try:
                    if book["pages"] <= int(pages_filter):
                        continue
                except ValueError:
                    pass
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

    def save_data(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
