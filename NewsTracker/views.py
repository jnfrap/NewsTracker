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

def allSites(request):
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)

    # Data is a json array, so we need to convert it to a string array
    sites = []
    for site in data:
        sites.append([site['mainUrl'], site['newsUrl'], site['newsTag'], site['newsType'], site['newsClass'], site['titleTag'], site['titleType'], site['titleClass'], site['subtitleTag'], site['subtitleType'], site['subtitleClass'],site['contentTag'], site['contentType'], site['contentClass'], site['imgsTag'], site['imgsType'], site['imgsClass'], site['directory']])

    # Send the list to the template
    template = loader.get_template('savedSites.html')
    doc = template.render({'sites': sites})
    return HttpResponse(doc)

def deleteSite(request): # ------------------->> NOT WORKING
    # Get the parameter
    site = request.GET['site']
    # Site is a string, so we need to convert it to a list
    site = site.split(',')

    # For each element in the list, remove the ' and the []
    for i in range(len(site)):
        site[i] = site[i].replace("'", "")
        site[i] = site[i].replace("[", "")
        site[i] = site[i].replace("]", "")
        site[i] = site[i].strip()
    
    # Get the json
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)
    
    # Compare the site with the json and delete it if it's the same
    for i in range(len(data)):
        if data[i]['mainUrl'] == site[0] and data[i]['newsUrl'] == site[1] and data[i]['newsTag'] == site[2] and data[i]['newsType'] == site[3] and data[i]['newsClass'] == site[4] and data[i]['titleTag'] == site[5] and data[i]['titleType'] == site[6] and data[i]['titleClass'] == site[7] and data[i]['subtitleTag'] == site[8] and data[i]['subtitleType'] == site[9] and data[i]['subtitleClass'] == site[10] and data[i]['contentTag'] == site[11] and data[i]['contentType'] == site[12] and data[i]['contentClass'] == site[13] and data[i]['imgsTag'] == site[14] and data[i]['imgsType'] == site[15] and data[i]['imgsClass'] == site[16] and data[i]['directory'] == site[17]:
            data.pop(i)
            break
    
    # Save the json
    with open(os.path.join(dirname, 'newsSites.json'), 'w') as f:
        json.dump(data, f)

    # Return a h1
    return HttpResponse('<h1>Site deleted</h1>')