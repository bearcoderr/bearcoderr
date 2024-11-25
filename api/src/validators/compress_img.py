from django.core.files.base import ContentFile
from django.core.files import File
from PIL import Image
from io import BytesIO

def compress_img(image, desired_width=None, desired_height=None):
    """
    Универсальная функция для сжатия и обрезки изображения.

    :param image: Загружаемое изображение (File)
    :param desired_width: Желаемая ширина изображения (int)
    :param desired_height: Желаемая высота изображения (int)
    :return: Обработанное изображение в формате File
    """
    try:
        # Открываем изображение и получаем его размеры
        im = Image.open(image)
        width, height = im.size

        # Если указана желаемая ширина
        if desired_width is not None:
            # Масштабируем изображение по ширине
            new_width = desired_width
            new_height = int((desired_width / width) * height)
            im = im.resize((new_width, new_height), Image.LANCZOS)

        # Если указана желаемая высота, обрезаем изображение по высоте
        if desired_height is not None:
            if new_height > desired_height:
                # Обрезаем сверху и снизу
                top = (new_height - desired_height) // 2
                bottom = top + desired_height
                im = im.crop((0, top, new_width, bottom))

        # Сохраняем изображение в формате WEBP
        im_bytes = BytesIO()
        im.save(im_bytes, format="WEBP", quality=85)

        # Создаем ContentFile и File для сохранения в модели Django
        image_content_file = ContentFile(im_bytes.getvalue())
        name = image.name.split('.')[0] + f'_{desired_width}x{desired_height}.webp'
        new_image = File(image_content_file, name=name)
        return new_image

    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None
