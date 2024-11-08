import os
import ctypes
import time
import requests
from PIL import Image, ImageDraw, ImageFont

# Путь к временному изображению
WALLPAPER_PATH = "C:\\Users\\Public\\quote_wallpaper.png"

def get_random_quote():
    """Получает случайную цитату с API Forismatic."""
    try:
        response = requests.get(
            "https://api.forismatic.com/api/1.0/",
            params={"method": "getQuote", "format": "json", "lang": "ru"},
        )
        if response.status_code == 200:
            data = response.json()
            quote = data["quoteText"]
            author = data.get("quoteAuthor", "Неизвестный автор")
            return f"{quote} — {author}"
        else:
            return "Не удалось получить цитату."
    except Exception as e:
        return f"Ошибка: {str(e)}"

def wrap_text(text, font, max_width):
    """Автоматически переносит строки, чтобы текст помещался в заданную ширину."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = font.getbbox(test_line)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)

def generate_image(quote):
    """Создаёт изображение с текстом и сохраняет его."""
    img = Image.new('RGB', (1920, 1080), color='black')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 48)

    wrapped_text = wrap_text(quote, font, 1800)
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    position = (
        (img.width - text_width) // 2,
        (img.height - text_height) // 2,
    )

    draw.multiline_text(position, wrapped_text, font=font, fill="white", align="center")
    img.save(WALLPAPER_PATH)

def set_wallpaper():
    """Устанавливает картинку как обои на рабочий стол (только Windows)."""
    ctypes.windll.user32.SystemParametersInfoW(20, 0, WALLPAPER_PATH, 3)

def main():
    """Основной цикл программы, обновляющий обои каждые 2 минуты."""
    while True:
        quote = get_random_quote()  # Получаем цитату на русском
        generate_image(quote)  # Генерируем изображение с цитатой
        set_wallpaper()  # Устанавливаем изображение как обои
        time.sleep(120)  # Ждём 2 минуты

if __name__ == "__main__":
    main()
