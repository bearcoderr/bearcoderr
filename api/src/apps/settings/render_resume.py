from src.models.settings import Settings, numberSettings, experienceSettings, skillsSettings, contactSettings, socialSettings
from src.models.services import ServicesSite
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image
import textwrap
import os
from django.conf import settings  # Для получения пути к настройкам Django


def generate_pdf(request):
    try:
        settings_obj = Settings.objects.first()
        if not settings_obj:
            return HttpResponse("Settings not found", status=404)

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'NotoSans-CondensedMedium.ttf')
        if not os.path.exists(font_path):
            return HttpResponse(f"Font file not found: {font_path}", status=404)

        pdfmetrics.registerFont(TTFont('NotoSansCondensed', font_path))
        pdf.setFont('NotoSansCondensed', 12)

        x, y = 50, 750

        # Печать картинки (если есть)
        if settings_obj.imgHome:
            img_path = settings_obj.imgHome.path
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    img = img.convert("RGB")
                    img.thumbnail((150, 150), Image.LANCZOS)
                    img_width, img_height = img.size
                    pdf.drawImage(img_path, x, y - img_height, width=img_width, height=img_height)
                    y -= img_height + 20
                except Exception as e:
                    return HttpResponse(f"Error loading image: {str(e)}", status=500)
            else:
                return HttpResponse(f"Image file not found: {img_path}", status=404)

        # Печать заголовков
        pdf.setFont('NotoSansCondensed', 14)
        pdf.drawString(x, y, "Основная информация")
        y -= 20
        pdf.setFont('NotoSansCondensed', 12)

        # Заголовок
        pdf.drawString(x, y, settings_obj.titleHome)
        y -= 20
        pdf.drawString(x, y, settings_obj.sub_titleHome)
        y -= 30

        # Текст
        wrapped_text = textwrap.wrap(settings_obj.textHome, width=70)
        for line in wrapped_text:
            if y < 50:
                pdf.showPage()
                y = 750
                pdf.setFont('NotoSansCondensed', 12)
            pdf.drawString(x, y, line)
            y -= 15

        draw_line(x, y, 500, pdf)
        y -= 15

        # Заголовок раздела: Числа
        pdf.setFont('NotoSansCondensed', 14)
        pdf.drawString(x, y, "Числа")
        y -= 20
        pdf.setFont('NotoSansCondensed', 12)

        # Печать чисел
        numbers = numberSettings.objects.all()
        for nums in numbers:
            if y < 50:
                pdf.showPage()
                y = 750
                pdf.setFont('NotoSansCondensed', 12)
            pdf.drawString(x, y, f"{nums.numberTitle}{nums.numberDopSimvol} {nums.numberText}")
            y -= 15

        draw_line(x, y, 500, pdf)
        y -= 15

        # Заголовок раздела: Услуги
        pdf.setFont('NotoSansCondensed', 14)
        pdf.drawString(x, y, "Услуги")
        y -= 20
        pdf.setFont('NotoSansCondensed', 12)

        # Печать услуг
        services = ServicesSite.objects.all()
        for service in services:
            if y < 50:
                pdf.showPage()
                y = 750
                pdf.setFont('NotoSansCondensed', 12)
            pdf.drawString(x, y, f"{service.titleServices}")
            y -= 15
            service_text = textwrap.wrap(service.exeptServices, width=100)
            for service_ex in service_text:
                pdf.drawString(x + 10, y, service_ex)
                y -= 15
            y -= 5

        draw_line(x, y, 500, pdf)
        y -= 15

        # Заголовок раздела: Опыт
        pdf.setFont('NotoSansCondensed', 14)
        pdf.drawString(x, y, "Опыт")
        y -= 20
        pdf.setFont('NotoSansCondensed', 12)

        # Печать опыта
        experiences = experienceSettings.objects.all()
        for experience in experiences:
            if y < 50:
                pdf.showPage()
                y = 750
                pdf.setFont('NotoSansCondensed', 12)
            pdf.drawString(x, y,
                           f"{experience.postExperience} в {experience.companyExperience}, {experience.yearExperience}")
            y -= 15
            wrapped_text = textwrap.wrap(experience.textExperience, width=70)
            for line in wrapped_text:
                pdf.drawString(x + 10, y, line)
                y -= 15

        draw_line(x, y, 500, pdf)
        y -= 20

        # Заголовок раздела: Навыки
        pdf.setFont('NotoSansCondensed', 14)
        pdf.drawString(x, y, "Навыки")
        y -= 20
        pdf.setFont('NotoSansCondensed', 12)

        # Печать навыков
        skills = skillsSettings.objects.all()
        skills_str = ", ".join(skill.titleSkills for skill in skills)
        pdf.drawString(x, y, skills_str)
        y -= 20

        draw_line(x, y, 500, pdf)
        y -= 15

        # Заголовок раздела: Контакты
        pdf.setFont('NotoSansCondensed', 14)
        pdf.drawString(x, y, "Контакты")
        y -= 20
        pdf.setFont('NotoSansCondensed', 12)

        # Печать контактов
        contacts = contactSettings.objects.all()
        for contact in contacts:
            if y < 50:
                pdf.showPage()
                y = 750
                pdf.setFont('NotoSansCondensed', 12)
            pdf.drawString(x, y, f"{contact.nameSontact}: {contact.titleSontact}")
            y -= 15

        draw_line(x, y, 500, pdf)
        y -= 15

        # Сохранение PDF
        pdf.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def draw_line(x, y, width, pdf):
    pdf.setStrokeColor(colors.black)  # Устанавливаем цвет линии
    pdf.setLineWidth(1)  # Устанавливаем толщину линии
    pdf.line(x, y, x + width, y)  # Рисуем линию
