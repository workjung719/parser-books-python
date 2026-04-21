import requests
from bs4 import BeautifulSoup # импортируем именно BeautifulSoup из библиотеки bs4
import time  # нужен чтобы делать паузы между запросами
import pandas as pd 

# Словарь для перевода рейтинга из слова в цифру
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def get_books_from_page(url):
    """
    Функция принимает адрес страницы,
    возвращает список словарей с данными книг.
    """
    response = requests.get(url)
    response.encoding = "utf-8"

    # Передаём HTML в BeautifulSoup — он его "разжёвывает" и делает удобным для поиска
    # "html.parser" — это встроенный в Python инструмент разбора HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим ВСЕ карточки книг на странице
    # Каждая книга обёрнута в тег <article class="product_pod">
    books = soup.find_all("article", class_="product_pod")

    page_books = []  # пустой список — будем добавлять книги сюда
    
    for book in books:
        # Название лежит в теге <h3> внутри тега <a>, в атрибуте title
        title  = book.find("h3").find("a")["title"]

        # Цена лежит в теге <p class="price_color">
        price  = book.find("p", class_="price_color").text.strip()

        # Рейтинг хранится хитро — в классе тега <p class="star-rating Three">
        # Слово после "star-rating" и есть рейтинг
        rating = RATING_MAP.get(book.find("p", class_="star-rating")["class"][1], 0)

        # Ссылка на обложку — в теге <img>, атрибут src
        # Но там относительный путь, поэтому добавляем начало адреса сайта
        img_src = book.find("img")["src"]
        img_url = "https://books.toscrape.com/" + img_src.replace("../", "")
        
        # Словарь — это как строка в будущей таблице Excel
        page_books.append({
            "Название":  title,
            "Цена":      price,
            "Рейтинг":   rating,
            "Обложка":   img_url
        })
    
    return page_books

# --- Главный цикл ---
all_books = []  # здесь соберём книги со ВСЕХ страниц

for page_num in range(1, 51):  # от 1 до 50 включительно
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    
    books = get_books_from_page(url)
    all_books.extend(books)  # extend добавляет все элементы списка, а не список в список
    
    print(f"Страница {page_num}/50 — собрано книг: {len(all_books)}")
    
    time.sleep(0.5)  # пауза 0.5 сек — чтобы не перегружать сервер

print(f"\nГотово! Всего книг: {len(all_books)}")

# Превращаем список словарей в таблицу (DataFrame)
# Pandas сам разберётся — ключи словарей станут названиями колонок
df = pd.DataFrame(all_books)

# Сохраняем в Excel
# index=False — не добавлять лишнюю колонку с номерами строк
df.to_excel("books.xlsx", index=False)

print("Файл books.xlsx сохранён!")