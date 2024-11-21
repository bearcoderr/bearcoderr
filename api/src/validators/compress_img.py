from django.core.files.base import ContentFile
from django.core.files import File
from PIL import Image
from io import BytesIO


def compress_img(image):
    try:
        # Открываем изображение и получаем его размеры
        im = Image.open(image)
        width, height = im.size

        # Проверяем, если одно измерение превышает 1000 пикселей
        if width > 1000 or height > 1000:
            # Вычисляем новые размеры с сохранением пропорций
            aspect_ratio = width / height
            if aspect_ratio > 1:
                new_width = min(width, 1000)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = min(height, 1000)
                new_width = int(new_height * aspect_ratio)

            # Масштабируем изображение до новых размеров
            im = im.resize((new_width, new_height))

        # Сохраняем изображение в формате WEBP
        im_bytes = BytesIO()
        im.save(im_bytes, format="WEBP", quality=100)

        # Создаем ContentFile и File для сохранения в модели Django
        image_content_file = ContentFile(im_bytes.getvalue())
        name = image.name.split('.')[0] + f'_{new_width}x{new_height}.webp'
        new_image = File(image_content_file, name=name)
        return new_image

    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None
