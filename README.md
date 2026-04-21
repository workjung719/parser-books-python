# Parser: books.toscrape.com

Учебный парсер каталога книг с сайта books.toscrape.com на Python.  
Проходит все страницы каталога, собирает название, цену, рейтинг и ссылку на обложку, сохраняет результат в Excel.

## Стек

- Python 3.11+
- requests
- beautifulsoup4
- pandas + openpyxl

## Запуск

```bash
pip install -r requirements.txt
python parser.py
```

Результат — файл `books.xlsx` в корне проекта.

## Что парсится

- Название книги
- Цена
- Рейтинг (1-5 звёзд)
- Ссылка на обложку
- URL страницы книги

## Результат

Парсится ~1000 книг со всех страниц каталога за ~1 минуту.