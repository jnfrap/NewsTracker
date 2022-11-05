from django.http import HttpResponse
from django.template import Template, Context, loader
from NewsTracker.Misc.Tracker import getNews
import os, json

def index(request):
    template = loader.get_template('index.html')
    doc = template.render()
    return HttpResponse(doc)

def response(request):
    # Get GET parameters
    main_url = request.GET['mainUrl']
    url = request.GET['newsUrl']
    news_tag = request.GET['newsTag']
    news_type = request.GET['newsType']
    news_class = request.GET['newsClass']
    news_content_tag = request.GET['contentTag']
    news_content_type = request.GET['contentType']
    news_content_class = request.GET['contentClass']
    imgs_tag = request.GET['imgsTag']
    img_type = request.GET['imgsType']
    imgs_class = request.GET['imgsClass']
    title_tag = request.GET['titleTag']
    title_type = request.GET['titleType']
    title_class = request.GET['titleClass']
    subtitle_tag = request.GET['subtitleTag']
    subtitle_type = request.GET['subtitleType']
    subtitle_class = request.GET['subtitleClass']
    save_path = request.GET['directory']

    # If not exist, create a json with the response named 'newsSites.json', if exist, append the new site
    dirname = os.path.dirname(__file__)+"/Misc/"
    if not os.path.exists(os.path.join(dirname, 'newsSites.json')):
        with open(os.path.join(dirname, 'newsSites.json'), 'w') as f:
            json.dump([{'mainUrl': main_url, 'newsUrl': url, 'newsTag': news_tag, 'newsType': news_type, 'newsClass': news_class, 'contentTag': news_content_tag, 'contentType': news_content_type, 'contentClass': news_content_class, 'imgsTag': imgs_tag, 'imgsType': img_type, 'imgsClass': imgs_class, 'titleTag': title_tag, 'titleType': title_type, 'titleClass': title_class, 'subtitleTag': subtitle_tag, 'subtitleType': subtitle_type, 'subtitleClass': subtitle_class, 'directory': save_path}], f)
    else:
        with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
            data = json.load(f)
        data.append({'mainUrl': main_url, 'newsUrl': url, 'newsTag': news_tag, 'newsType': news_type, 'newsClass': news_class, 'contentTag': news_content_tag, 'contentType': news_content_type, 'contentClass': news_content_class, 'imgsTag': imgs_tag, 'imgsType': img_type, 'imgsClass': imgs_class, 'titleTag': title_tag, 'titleType': title_type, 'titleClass': title_class, 'subtitleTag': subtitle_tag, 'subtitleType': subtitle_type, 'subtitleClass': subtitle_class, 'directory': save_path})
        with open(os.path.join(dirname, 'newsSites.json'), 'w') as f:
            json.dump(data, f)
    
    # Return a h1
    return HttpResponse('<h1>Site added</h1>')

def download(request):
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)
    for site in data:
        getNews(site['mainUrl'], site['newsUrl'], site['newsTag'], site['newsType'], site['newsClass'], site['contentTag'], site['contentType'], site['contentClass'], site['imgsTag'], site['imgsType'], site['imgsClass'], site['titleTag'], site['titleType'], site['titleClass'], site['subtitleTag'], site['subtitleType'], site['subtitleClass'], site['directory'])
    return HttpResponse('<h1>Download finished</h1>')

def allSites(request): # ---------------MEJORAR----------------
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)

    # Data is a json array, so we need to convert it to a Sites array
    sites = []
    for site in data:
        sites.append([site['mainUrl'], site['newsUrl'], site['newsTag'], site['newsType'], site['newsClass'], site['titleTag'], site['titleType'], site['titleClass'], site['subtitleTag'], site['subtitleType'], site['subtitleClass'],site['contentTag'], site['contentType'], site['contentClass'], site['imgsTag'], site['imgsType'], site['imgsClass'], site['directory']])

    # Send the list to the template
    template = loader.get_template('savedSites.html')
    doc = template.render({'sites': sites})
    return HttpResponse(doc)