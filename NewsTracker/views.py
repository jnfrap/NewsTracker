from django.http import HttpResponse
from django.template import Template, Context, loader
from NewsTracker.Misc.Tracker import getNews
import os, json, shutil, traceback

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
            json.dump([{'mainUrl': main_url, 'newsUrl': url, 'newsTag': news_tag, 'newsType': news_type, 'newsClass': news_class, 'contentTag': news_content_tag, 'contentType': news_content_type, 'contentClass': news_content_class, 'imgsTag': imgs_tag, 'imgsType': img_type, 'imgsClass': imgs_class, 'titleTag': title_tag, 'titleType': title_type, 'titleClass': title_class, 'subtitleTag': subtitle_tag, 'subtitleType': subtitle_type, 'subtitleClass': subtitle_class, 'directory': save_path, 'schedule': '12:00', 'activate': 'off', 'd_limit': '3', 'n_limit': '-1', 'id': '0'}], f)
    else:
        with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
            data = json.load(f)
        data.append({'mainUrl': main_url, 'newsUrl': url, 'newsTag': news_tag, 'newsType': news_type, 'newsClass': news_class, 'contentTag': news_content_tag, 'contentType': news_content_type, 'contentClass': news_content_class, 'imgsTag': imgs_tag, 'imgsType': img_type, 'imgsClass': imgs_class, 'titleTag': title_tag, 'titleType': title_type, 'titleClass': title_class, 'subtitleTag': subtitle_tag, 'subtitleType': subtitle_type, 'subtitleClass': subtitle_class, 'directory': save_path, 'schedule': '12:00', 'activate': 'off', 'd_limit': '3', 'n_limit': '-1', 'id': str(len(data))})
        with open(os.path.join(dirname, 'newsSites.json'), 'w') as f:
            json.dump(data, f)

    # Return a script to send a success alert and reload the page
    return HttpResponse('<script>alert("Site added successfully"); window.location.href = "/";</script>')

def download(request):
    # Get the sites from newsSites.json and download it with getNews()
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)
    for site in data:
        getNews(site['mainUrl'], site['newsUrl'], site['newsTag'], site['newsType'], site['newsClass'], site['contentTag'], site['contentType'], site['contentClass'], site['imgsTag'], site['imgsType'], site['imgsClass'], site['titleTag'], site['titleType'], site['titleClass'], site['subtitleTag'], site['subtitleType'], site['subtitleClass'], site['directory'], int(site['d_limit']), int(site['n_limit']))
    
    # Compress the Misc/output folder and send it to the user to download
    shutil.make_archive('output', 'zip', os.path.join(dirname, 'output'))
    with open('output.zip', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=output.zip'
        return response

def allSites(request):
    # Get the content of newsSites.json
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)

    # Data is a json array, so we need to convert it to a string array
    sites = []
    for site in data:
        sites.append([site['mainUrl'], site['newsUrl'], site['newsTag'], site['newsType'], site['newsClass'], site['titleTag'], site['titleType'], site['titleClass'], site['subtitleTag'], site['subtitleType'], site['subtitleClass'],site['contentTag'], site['contentType'], site['contentClass'], site['imgsTag'], site['imgsType'], site['imgsClass'], site['directory'], site['id']])

    # Send the list to the template
    template = loader.get_template('savedSites.html')
    doc = template.render({'sites': sites})
    return HttpResponse(doc)

def deleteSite(request):
    # Get the parameter
    id = request.GET['site']
    
    # Get the json
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)
    
    # Delete the site
    for site in data:
        if site['id'] == id:
            data.remove(site)
            break
    
    # Reassign the ids
    for i in range(len(data)):
        data[i]['id'] = str(i)

    # Save the json
    with open(os.path.join(dirname, 'newsSites.json'), 'w') as f:
        json.dump(data, f)

    # Return a script to reload the page
    return HttpResponse('<script>window.location.href = "/allSites";</script>')

def testSite(request):
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

    try:
        # Get the news
        getNews(main_url, url, news_tag, news_type, news_class, news_content_tag, news_content_type, news_content_class, imgs_tag, img_type, imgs_class, title_tag, title_type, title_class, subtitle_tag, subtitle_type, subtitle_class, save_path, -1, -1)

        # Compress the Misc/output/save_path folder and send it to the user to download
        shutil.make_archive('output', 'zip', os.path.join(os.path.dirname(__file__)+"/Misc/output/", save_path))

        # Return output.zip
        with open('output.zip', 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=output.zip'
            return response
    except:
        # Download a file with the error
        with open('error.txt', 'w') as f:
            f.write(traceback.format_exc())
        with open('error.txt', 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=error.txt'
            return response

def settings(request):
    # Get newsSites.json, get the fields newsUrl, schedule, activate, d_limit, n_limit. Save it in variables
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)

    sites = []
    for site in data:
        sites.append([site['id'], site['newsUrl'], site['schedule'], site['activate'], site['d_limit'], site['n_limit']])
    
    # Send sites to the template
    template = loader.get_template('settings.html')
    doc = template.render({'sites': sites})
    return HttpResponse(doc)

def saveSettings(request):
    # Get the parameters
    id = request.GET['id']
    schedule = request.GET['schedule']
    ndays = request.GET['days']
    nnews = request.GET['news']
    try:
        activate = request.GET['activate']
    except:
        activate = 'off'

    # Get the json
    dirname = os.path.dirname(__file__)+"/Misc/"
    with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
        data = json.load(f)

    # Change the values of the json
    for i in range(len(data)):
        if data[i]['id'] == id:
            data[i]['schedule'] = schedule
            data[i]['activate'] = activate
            data[i]['d_limit'] = ndays
            data[i]['n_limit'] = nnews
            break

    # Save the json
    with open(os.path.join(dirname, 'newsSites.json'), 'w') as f:
        json.dump(data, f)

    # Return a script to reload the page
    return HttpResponse('<script>window.location.href = "/settings";</script>')