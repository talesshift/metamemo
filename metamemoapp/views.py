from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from metamemoapp.models import MetaMemo, MemoItem, MemoContext, MemoNews, NewsCover, NewsItem
from metamemoapp.filters import MemoItemFilter, MemoNewsFilter
from django.core.paginator import Paginator

from datetime import datetime, timedelta
from collections import Counter
from metamemoapp.tasks import download_async,download_img_async
# Create your views here.
def home(request):
    metamemo = MetaMemo.objects.all()
    tags = MemoItem.objects.all().values_list('keyword__word', flat=True)
    tags = Counter(tags)
    tags[None] = 0

    return render(request, 'home.html', {'metamemo' : metamemo, 'tags' : tags.most_common(15)})

def lista(request):
    memoqs = MemoItem.objects.all().order_by('-content_date')
    memofilter = MemoItemFilter(request.GET, queryset=memoqs.prefetch_related('author'))

    memoitem = Paginator(memofilter.qs, 50)
    date = datetime.now()
    #Hackish
    tags = {}
    tags_raw = memofilter.qs.values_list('keyword__word', flat=True)
    tags = Counter(tags_raw)
    tags[None]=0
    
    data = {
        'memofilter' : memofilter,
        'metamemo' : MetaMemo.objects.values_list('name', flat=True),
        'memoitem' : memoitem.page(1),
        'tags' : tags.most_common(10),
        'date' : date
    }
    
    return render(request, 'advsearch.html', {'data' : data})


def search(request, year=None, month=None, day=None):
    if not year:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day

    date = datetime(year, month, day)
    end_date = date+timedelta(1)
    
    memoqs = MemoItem.objects.filter(content_date__gte=date, content_date__lte=end_date).order_by('content_date')
    memofilter = MemoItemFilter(request.GET, queryset=memoqs)

    newsqs = NewsItem.objects.filter(content_date__gte=date, content_date__lte=end_date).order_by('content_date')
    newsfilter = MemoNewsFilter(request.GET, queryset=newsqs)
    
    memoitem = Paginator(memofilter.qs, 50)
    memonews = Paginator(newsfilter.qs, 50)

    memocontext = MemoContext.objects.filter(start_date__lte=date, end_date__gte=date).order_by('start_date')
    newscover = NewsCover.objects.filter(content_date__gte=date, content_date__lte=end_date)

    #Hackish
    tags = {}
    tags_raw = memofilter.qs.values_list('keyword__word', flat=True)
    tags = Counter(tags_raw)
    tags[None]=0
    
    data = {
        'memofilter' : memofilter,
        'metamemo' : MetaMemo.objects.all(),
        'memocontext' : memocontext,
        'memoitem' : memoitem.page(1),
        'memonews' : memonews.page(1),
        'newscovers' : newscover,
        'tags' : tags.most_common(10),
        'date' : date
    }
    
    return render(request, 'search.html', {'data' : data})

def memoitem(request, item_id):
    memoitem = MemoItem.objects.get(pk=item_id)
    return render(request, 'memoitem.html', {'memoitem': memoitem})

def get_media(request, item_id):
    memoitem = MemoItem.objects.get(pk=item_id)

    response = {
        'medias' : [],
    }
    for p in memoitem.medias.all():
            if p.mediatype == 'VIDEO' and p.status in ['INITIAL', 'FAILED_DOWNLOAD']:
                p.status = 'DOWNLOADING'
                p.save(update_fields=['status',])
                download_async.apply_async(kwargs={'url': p.original_url, 'mediatype': 'VIDEO'}, queue='fastlane')
            elif p.mediatype=='IMAGE' and p.status in ['INITIAL', 'FAILED_DOWNLOAD']:
                p.status = 'DOWNLOADING'
                p.save(update_fields=['status',])
                download_img_async.apply_async(kwargs={'url' : p.original_url, 'pk' : p.pk}, queue='fastlane')
            response['medias'].append({'mediatype' : p.mediatype, 'original_url' : p.original_url, 'status' : p.status})
    return JsonResponse(response, status=200)

def content(request, page):
    return render(request, f'content/{page}.html')