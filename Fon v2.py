import requests
import json
import os
import time
import ctypes  # Для смены обоев на Windows
from PIL import Image, ImageDraw, ImageFont

PEXELS_API_KEY = "RKmPslYy2nPRdVDBhA1m7ENlyr8JSyL4jN3UVSyAPaKxI0ypvbR35D9J"
UNSPLASH_API_KEY = "M09KW0f7OgtT3yaKk9c2dKx4wNxUmWd1XFl5FygooOY"

IMAGE_PATH = "background.jpg"
FONT_PATH = "arial.ttf"

def search_pexels_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": PEXELS_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        if data["photos"]:
            photo_url = data["photos"][0]["src"]["original"]
            download_image(photo_url)
            print("Изображение успешно загружено с Pexels.")
            return True
        else:
            print("Не найдено изображений на Pexels.")
            return False
    except Exception as e:
        print(f"Ошибка при получении изображения с Pexels: {e}")
        return False

def search_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        photo_url = data["urls"]["full"]
        download_image(photo_url)
        print("Изображение успешно загружено с Unsplash.")
        return True
    except Exception as e:
        print(f"Ошибка при получении изображения с Unsplash: {e}")
        return False

def download_image(url):
    """Загружает изображение по указанному URL."""
    response = requests.get(url)
    with open(IMAGE_PATH, "wb") as f:
        f.write(response.content)

def get_image(query):
    print(f"Ищем изображение по запросу: {query}...")
    if search_pexels_image(query):
        return True
    print("Pexels недоступен, пробуем Unsplash...")
    if search_unsplash_image(query):
        return True
    print("Не удалось загрузить изображение.")
    return False

def get_quote():
    url = "https://api.forismatic.com/api/1.0/"
    params = {"method": "getQuote", "format": "json", "lang": "ru"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        quote = data["quoteText"]
        author = data.get("quoteAuthor", "Неизвестный автор")
        return f"{quote} — {author}"
    except Exception as e:
        print(f"Ошибка при получении цитаты: {e}")
        return "Иногда лучший способ начать — просто начать."

def add_text_to_image(image_path, text):
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_PATH, 48)

        image_width, image_height = image.size

        # Разбиваем текст на строки
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_width, _ = draw.textbbox((0, 0), test_line, font=font)[2:]

            if text_width <= image_width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
        y = (image_height - total_text_height) // 2

        # Отрисовываем каждую строку с тенью и основным текстом
        for line in lines:
            text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
            x = (image_width - text_width) // 2

            # Тень (чёрный цвет, немного смещённая позиция)
            draw.text((x + 2, y + 2), line, font=font, fill="black")

            # Основной текст (белый цвет)
            draw.text((x, y), line, font=font, fill="white")

            y += text_height

        image.save(IMAGE_PATH)
        print("Текст успешно добавлен на изображение.")
    except Exception as e:
        print(f"Ошибка при добавлении текста на изображение: {e}")


def set_wallpaper(image_path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(image_path), 0)
        print("Обои успешно установлены.")
    except Exception as e:
        print(f"Ошибка при установке обоев: {e}")

def main():
    while True:
        quote = get_quote()
        print(f"Цитата: {quote}")

        query = "nature" if "природа" in quote.lower() else "motivation"

        if get_image(query):
            add_text_to_image(IMAGE_PATH, quote)
            set_wallpaper(IMAGE_PATH)

        print("Ожидание 2 минуты...")
        time.sleep(120)

if __name__ == "__main__":
    main()
