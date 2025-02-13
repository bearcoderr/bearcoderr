from src.models.news import news, newsCategory, newsTag, Formsnews
import csv
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slugnews': ('titlenews',)}
    list_display = ['id', 'titlenews', 'dataNews']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name="import_csv"),
            path('export-csv/', self.admin_site.admin_view(self.export_csv), name="export_csv"),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == 'POST' and request.FILES.get('file'):
            try:
                csv_file = request.FILES['file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                for row in reader:
                    if not row.get('contentnews'):
                        print(f"Пропускаем строку, где отсутствует contentnews: {row}")
                        continue

                    try:
                        category = newsCategory.objects.get(id=row['category_id']) if row['category_id'] else None

                        news.objects.create(
                            imgnews=row['imgnews'] if row['imgnews'] else None,
                            titlenews=row['titlenews'],
                            slugnews=row['slugnews'],
                            contentnews=row['contentnews'],
                            published_at=row.get('published_at'),
                            dataNews=row.get('dataNews'),
                            countView=int(row.get('countView', 0)),
                            category=category,
                            text_twitter=row.get['text_twitter']
                        )

                    except newsCategory.DoesNotExist:
                        print(f"Ошибка: Категория с ID {row.get('category_id')} не найдена")
                    except KeyError as e:
                        print(f"Ошибка: отсутствует ключ {e}")
                    except Exception as e:
                        print(f"Ошибка при обработке строки {row}: {e}")

                return JsonResponse({"message": "Данные успешно импортированы!"})

            except Exception as e:
                print(f"Ошибка при загрузке CSV: {e}")
                return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"error": "Ошибка загрузки CSV"}, status=500)

    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="news_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Slug', 'Content', 'Image Path', 'Category', 'Published At', 'Data News', 'Count Views'])

        for item in news.objects.all():
            writer.writerow([
                item.titlenews,
                item.slugnews,
                item.contentnews,
                item.imgnews,
                item.category.titleCategory if item.category else 'N/A',
                item.published_at,
                item.dataNews,
                item.countView
            ])

        return response

    class Media:
        js = ('admin/js/import_csv.js',)

admin.site.register(news, NewsAdmin)



@admin.register(newsCategory)
class newsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slagCategory': ('titleCategory',)}
    list_display = ['titleCategory']

@admin.register(newsTag)
class newsTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slagTag': ('titleTag',)}
    list_display = ['titleTag']

@admin.register(Formsnews)
class FormsnewsAdmin(admin.ModelAdmin):
    list_display = ['nameComm', 'emailComm', 'time_create', 'post']
