from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView
from src.models.news import news, newsCategory, newsTag, gallerynews
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

#Отправка формы
from .forms import FeedbackCreateForm


class newsDetailCategory(View):
    def get(self, request, category_slug):
        news_category = get_object_or_404(newsCategory, slagCategory=category_slug)
        news_list = news.objects.filter(category=news_category)
        news_list_tag = newsTag.objects.all()
        news_list_recent = news.objects.order_by('-datanews')[:3]
        category = newsCategory.objects.all()

        paginator = Paginator(news_list, 10)  # По 10 новостей на каждой странице
        page_number = request.GET.get('page')

        try:
            news_list = paginator.page(page_number)
        except PageNotAnInteger:
            news_list = paginator.page(1)
        except EmptyPage:
            news_list = paginator.page(paginator.num_pages)

        return render(request, 'news/blog.html', {
            'news_category': news_category,
            'news_list': news_list,
            'news_list_tag': news_list_tag,
            'news_list_recent': news_list_recent,
            'category': category,
        })

class newsDetailTag(View):
    def get(self, request, tag_slug):
        news_tag = get_object_or_404(newsTag, slagTag=tag_slug)
        news_list = news.objects.filter(tags=news_tag)
        news_list_recent = news.objects.order_by('-datanews')[:3]
        category = newsCategory.objects.all()

        paginator = Paginator(news_list, 10)  # По 10 новостей на каждой странице
        page_number = request.GET.get('page')

        try:
            news_list = paginator.page(page_number)
        except PageNotAnInteger:
            news_list = paginator.page(1)
        except EmptyPage:
            news_list = paginator.page(paginator.num_pages)

        news_list_tag = newsTag.objects.all()  # Получаем все объекты newsTag для вывода в шаблоне

        return render(request, 'news/blog.html', {
            'news_tag': news_tag,
            'news_list': news_list,
            'news_list_tag': news_list_tag,
            'news_list_recent': news_list_recent,
            'category': category,
        })


class newsListView(View):
    def get(self, request):
        news_list = news.objects.order_by('-datanews')
        news_list_tag = newsTag.objects.all()
        news_list_recent = news.objects.order_by('-datanews')[:3]
        category = newsCategory.objects.all()

        category_counts = {}
        for categor in category:
            category_counts[categor.titleCategory] = news.objects.filter(category=categor).count()

        paginator = Paginator(news_list, 10)  # По 10 новостей на каждой странице
        page_number = request.GET.get('page')

        try:
            news_list = paginator.page(page_number)
        except PageNotAnInteger:
            news_list = paginator.page(1)
        except EmptyPage:
            news_list = paginator.page(paginator.num_pages)


        return render(request, 'news/blog.html', {
            'news_list': news_list,
            'news_list_recent': news_list_recent,
            'news_list_tag': news_list_tag,
            'category': category,
            'category_counts': category_counts,
        })
class newsDetailView(View):
    def get(self, request, category_slug, slug):
        news_item = get_object_or_404(news, category__slagCategory=category_slug, slugnews=slug)
        return render(request, 'news/blog-details.html', {
            'news_item': news_item,
        })



class newsDetailView(View):
    def get(self, request, category_slug, slug):
        news_info = get_object_or_404(news, slugnews=slug)
        related_tags = newsTag.objects.filter(news=news_info.id)
        foto = gallerynews.objects.filter(news=news_info.id)
        return render(request, 'news/blog-details.html', {
            'news_info': news_info,
            'related_tags': related_tags,
            'foto': foto,
        })

class SearchResultsView(ListView):
    model: news
    template_name = 'news/search_results.html'
    context_object_name = 'news_search'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return news.objects.filter(titlenews__icontains=query)
        return news.objects.all()


def share_facebook(request):
    # Логика для шаринга на Facebook
    post_url = request.build_absolute_uri()  # Получаем текущий URL страницы
    facebook_url = f'https://www.facebook.com/sharer/sharer.php?u={post_url}'
    return redirect(facebook_url)

def share_twitter(request):
    # Логика для шаринга на Twitter
    post_url = request.build_absolute_uri()  # Получаем текущий URL страницы
    twitter_url = f'https://twitter.com/intent/tweet?url={post_url}'
    return redirect(twitter_url)

def share_linkedin(request):
    # Логика для шаринга на LinkedIn
    post_url = request.build_absolute_uri()  # Получаем текущий URL страницы
    linkedin_url = f'https://www.linkedin.com/sharing/share-offsite/?url={post_url}'
    return redirect(linkedin_url)

def share_pinterest(request):
    # Логика для шаринга на Pinterest
    post_url = request.build_absolute_uri()  # Получаем текущий URL страницы
    pinterest_url = f'https://www.pinterest.com/pin/create/button/?url={post_url}'
    return redirect(pinterest_url)


def FeedbackCreateView(request):
    if request.method == 'POST':
        form = FeedbackCreateForm(request.POST)
        if form.is_valid():
            forms_home_instance = form.save()
        return redirect('forms_home_thanks')
    else:
        form = FeedbackCreateForm()
    return render(request, 'settings/index.html', {
        'form': form,
        })

def contact_thanks_view(request):
    return render(request, 'settings/contact_thanks.html')



def rss_feed(request):
    news_items = news.objects.all().order_by('-datanews')[:20]  # Получаем последние 20 новостей

    # Собираем абсолютные URL для изображений каждой новости
    for item in news_items:
        if item.imgnews:  # Проверяем, что изображение существует
            item.img_url = request.build_absolute_uri(item.imgnews.url)
        else:
            item.img_url = ''  # Если изображения нет, присваиваем пустую строку

    context = {
        'news_items': news_items,
        'request': request,
    }

    rendered_xml = render_to_string('news/rss_feed.xml', context)
    response = HttpResponse(content_type='application/rss+xml')
    response['Content-Disposition'] = 'attachment; filename="rss_feed.xml"'
    response.write(rendered_xml.encode('utf-8'))
    return response