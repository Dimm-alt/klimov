import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Имя файла для хранения данных
DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        """Инициализация приложения: создаём окно, поля, таблицу"""
        self.root = root
        self.root.title("Моя библиотека фильмов")
        self.root.geometry("750x450")
        
        # Список для хранения фильмов
        self.movies = []
        self.load_data()  # Загружаем сохранённые фильмы
        
        self.create_input_fields()   # Поля для ввода
        self.create_filter_fields()  # Поля для фильтрации
        self.create_table()          # Таблица для списка фильмов
        
        self.refresh_table()  # Показываем фильмы в таблице
    
    def create_input_fields(self):
        """Создаём поля для добавления нового фильма"""
        # Название фильма
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Жанр
        tk.Label(self.root, text="Жанр:").grid(row=0, column=2, padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Год выпуска
        tk.Label(self.root, text="Год:").grid(row=1, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self.root, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Рейтинг
        tk.Label(self.root, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5)
        self.rating_entry = tk.Entry(self.root, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        tk.Button(self.root, text="Добавить фильм", command=self.add_movie,
                  bg="lightgreen", width=20).grid(row=2, column=0, columnspan=4, pady=10)
    
    def create_filter_fields(self):
        """Создаём поля для фильтрации фильмов"""
        frame = tk.LabelFrame(self.root, text="Фильтрация", padx=5, pady=5)
        frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
        
        tk.Label(frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.filter_genre = tk.Entry(frame, width=15)
        self.filter_genre.grid(row=0, column=1, padx=5)
        self.filter_genre.bind("<KeyRelease>", self.apply_filters)  # Фильтруем при вводе
        
        tk.Label(frame, text="Фильтр по году:").grid(row=0, column=2, padx=5)
        self.filter_year = tk.Entry(frame, width=8)
        self.filter_year.grid(row=0, column=3, padx=5)
        self.filter_year.bind("<KeyRelease>", self.apply_filters)
        
        tk.Button(frame, text="Сбросить фильтры", command=self.clear_filters,
                  bg="lightgray").grid(row=0, column=4, padx=10)
    
    def create_table(self):
        """Создаём таблицу для отображения фильмов"""
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        
        # Настраиваем заголовки и ширину столбцов
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        
        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=4, column=4, sticky="ns", pady=10)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Настройка растягивания таблицы при изменении размера окна
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def load_data(self):
        """Загружает фильмы из JSON-файла при запуске"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except:
                self.movies = []  # Если файл повреждён, начинаем с пустого списка
    
    def save_data(self):
        """Сохраняет фильмы в JSON-файл"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)
    
    def add_movie(self):
        """Добавляет новый фильм с проверкой корректности данных"""
        # Получаем данные из полей ввода
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()
        
        # Проверка: все ли поля заполнены
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        # Проверка: год должен быть целым числом
        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        
        # Проверка: рейтинг от 0 до 10
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return
        
        # Добавляем фильм в список
        self.movies.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })
        
        self.save_data()          # Сохраняем в файл
        self.clear_inputs()       # Очищаем поля ввода
        self.refresh_table()      # Обновляем таблицу
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")
    
    def clear_inputs(self):
        """Очищает все поля ввода"""
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
    
    def apply_filters(self, event=None):
        """Применяет фильтры при вводе текста в поля фильтрации"""
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()
        self.refresh_table(genre_filter, year_filter)
    
    def clear_filters(self):
        """Очищает фильтры и показывает все фильмы"""
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.refresh_table()
    
    def refresh_table(self, genre_filter="", year_filter=""):
        """Обновляет таблицу с учётом фильтров"""
        # Удаляем старые строки из таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
     
        
        filtered_movies = self.movies
        
        if genre_filter:
            # Оставляем только фильмы, содержащие текст в жанре
            filtered_movies = [m for m in filtered_movies 
                              if genre_filter in m["genre"].lower()]
        
        if year_filter and year_filter.isdigit():
            # Оставляем только фильмы указанного года
            year = int(year_filter)
            filtered_movies = [m for m in filtered_movies 
                              if m["year"] == year]
        
       
        for movie in filtered_movies:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
