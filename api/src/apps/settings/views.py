from django.views.generic.base import View
from django.shortcuts import render, redirect
from .repository import SettingsRepository
from src.domain.settings.services import SettingsServices
from src.domain.services.services import ServicesServices
from src.apps.services.repository import ServicesRepository

from src.domain.settings.dto import FormSettingsDTO
from .forms import formsHome
from .tasks import send_email
import threading

# Подключаем Блог
from src.domain.news.services import NewsService
from src.apps.news.repository import NewsRepository

# Подключаем Работы
from src.apps.worck.repository import WorkRepository
from src.domain.worck.services import WorkService
from django.http import JsonResponse

class ViewHomes(View):

    ## Выводим данные из БД ##
    def get(self, request):
        # Создаем экземпляр репозитория
        settings_repository = SettingsRepository()

        services_repository = ServicesRepository()
        services_services = ServicesServices(services_repository)

        # Передаем репозиторий в сервис
        settings_services = SettingsServices(settings_repository=settings_repository)
        request.page_title = settings_services.get_settings().titleHome

        news_repository = NewsRepository()
        news_services = NewsService(news_repository)

        form = formsHome()

        # Подключаем категории работ
        work_repository = WorkRepository()
        work_service = WorkService(work_repository=work_repository)
        work_categories = work_service.get_work_category_list()
        
        # Все превью работ

        # Получаем все превью работ
        work_previews = work_service.get_work_all()

        # Получаем настройки через сервис
        context = {
            'form': form,
            'settings': settings_services.get_settings(),
            'services': services_services.get_services_list(),
            'news_list': news_services.get_news_list()[:3],
            'work_categories': work_categories,
            'work_previews': work_previews
        }

        # Рендерим шаблон с переданным контекстом
        return render(request, 'settings/index.html', context)

    def post(self, request):
        form = formsHome(request.POST)
        if form.is_valid():
            # Преобразуем данные формы в DTO
            form_dto = FormSettingsDTO(
                nameFormsHome=form.cleaned_data['nameFormsHome'],
                emailFormsHome=form.cleaned_data['emailFormsHome'],
                callFormsHome=form.cleaned_data['callFormsHome'],
                massageFormsHome=form.cleaned_data['massageFormsHome']
            )

            # Создаем репозиторий и сервис для обработки формы
            settings_repository = SettingsRepository()
            settings_services = SettingsServices(settings_repository=settings_repository)

            # Сохраняем данные через сервис
            settings_services.post_fotms_settings(form_dto)

            # Уведомление об успешной отправке
            request.session['message'] = 'Ваша заявка успешно отправлена!'

            # Перенаправляем на главную страницу или другую страницу
            return redirect('thanks')  # Или другой путь

        # Если форма не валидна, возвращаем ошибку и повторно рендерим страницу
        settings_repository = SettingsRepository()
        settings_services = SettingsServices(settings_repository=settings_repository)

        context = {
            'form': form,
            'settings': settings_services.get_settings(),
        }

        return render(request, 'settings/index.html', context)

class ThanksView(View):
    def get(self, request):

        request.page_title = 'Спасибо за заявку!'
        request.page_description = 'Я свяжусь с вами в течении дня!'

        return render(request, 'settings/contact_thanks.html')


class sendEmail(View):
    def get(self, request):
        threading.Thread(target=send_email, args=("bearcoderr@gmail.com",)).start()

        return render(request, 'settings/index.html')


class WorkView(View):
    def get(self, request, work_id):
        work_repository = WorkRepository()
        work_service = WorkService(work_repository=work_repository)
        work_item = work_service.get_work_item(work_id)

        # Return JSON response with work item details
        return JsonResponse(work_item.__dict__, safe=False)
