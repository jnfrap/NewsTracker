import requests, urllib.request, json, os, shutil
from bs4 import BeautifulSoup

#Config class with the data of each news site
class Config:
    def __init__(self, main_url, url, news_tag, news_type, news_class, news_content_tag, news_content_type, news_content_class, imgs_tag, img_type, imgs_class, title_tag, title_type, title_class, subtitle_tag, subtitle_type, subtitle_class, save_path):
        self.main_url = main_url
        self.url = url
        self.news_tag = news_tag
        self.news_type = news_type
        self.news_class = news_class
        self.news_content_tag = news_content_tag
        self.news_content_type = news_content_type
        self.news_content_class = news_content_class
        self.imgs_tag = imgs_tag
        self.img_type = img_type
        self.imgs_class = imgs_class
        self.title_tag = title_tag
        self.title_type = title_type
        self.title_class = title_class
        self.subtitle_tag = subtitle_tag
        self.subtitle_type = subtitle_type
        self.subtitle_class = subtitle_class
        self.save_path = save_path

#Relative path
dirname = os.path.dirname(__file__)

# Delete the content of the folder output
folder = dirname+'\\output'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

#Create and fill the config list
configs = []
#Create the folder to save the news
os.makedirs(os.path.join(dirname+'\\output', 'Albacete'), exist_ok=True)
configs.append(Config('https://www.albacete.es', 'https://www.albacete.es/es/noticias', 'div', 'class', 'layout-content', 'div', 'class', 'layout__region--first', 'div', 'class','ps_post_contenido', 'h1', 'class', 'page-title', 'div', 'class', 'field field--name-field-subtitulo field--type-string field--label-hidden field__item', dirname+'\\output\\Albacete\\'))
os.makedirs(os.path.join(dirname+'\\output', 'Villarobledo'), exist_ok=True)
configs.append(Config('https://www.villarrobledo.com', 'https://www.villarrobledo.com/noticias.php', 'ul', 'class', 'listado', 'div', 'class', 'detalle', 'div', 'id', 'carrusel', 'p', 'class', 'titulo', 'div', 'class', 'entradilla', dirname+'\\output\\Villarobledo\\'))
os.makedirs(os.path.join(dirname+'\\output', 'Tomelloso'), exist_ok=True)
configs.append(Config('http://www.tomelloso.es/', 'http://www.tomelloso.es/prensa/', 'table', 'class', 'table', 'div', 'class', 'article-content', 'section', 'class', 'article-intro', 'h1', 'class', 'article-title', 'span', 'style', "font-size: 14pt; font-family: Arial, 'sans-serif';", dirname+'\\output\\Tomelloso\\'))

####################################################################################################
####################################################################################################

for config in configs:
    main_url = config.main_url
    url = config.url
    news_tag = config.news_tag
    news_type = config.news_type
    news_class = config.news_class
    news_content_tag = config.news_content_tag
    news_content_type = config.news_content_type
    news_content_class = config.news_content_class
    imgs_tag = config.imgs_tag
    img_type = config.img_type
    imgs_class = config.imgs_class
    title_tag = config.title_tag
    title_type = config.title_type
    title_class = config.title_class
    subtitle_tag = config.subtitle_tag
    subtitle_type = config.subtitle_type
    subtitle_class = config.subtitle_class
    save_path = config.save_path

    headers = {
        'cache-control': "no-cache"
        }

    # Not check ssl
    requests.packages.urllib3.disable_warnings()

    # Get the html of the page
    response = requests.request("GET", url, headers=headers, verify=False)

    # Parse the response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the div with the class layout-content
    div = soup.find(news_tag, attrs={news_type: news_class})

    # Get all the links from the div
    links = div.find_all('a')

    # Print all the url, store in an array, controlling exceptions
    urls = []
    for link in links:
        try:
            # If url contains the main url, add to the array
            if link['href'].find(main_url) != -1:
                # If the url is not in the array, add it
                if urls.count(link['href']) == 0:
                    urls.append(link['href'])
            else:
                # If the url is not in the array, add it
                if urls.count(main_url+link['href']) == 0:
                    urls.append(main_url+link['href'])
        except:
            pass

    # Get the rest response of the urls and store it in an array
    responses = []
    for url in urls:
        try:
            response = requests.request("GET", url, headers=headers, verify=False)
            responses.append(response)
        except:
            pass

    # Parse the responses and get the main tag controlling exceptions
    main = []
    images_urls = []
    main_id = 0
    for response in responses:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Get the title
            title = soup.find(title_tag, attrs={title_type: title_class})
            titleText = title.text
            # Get the content
            try:
                div = soup.find(news_content_tag, attrs={news_content_type: news_content_class})
                contentText = div.text
            except:
                contentText = ''
            # Get the subtitle
            try:
                subtitle = soup.find(subtitle_tag, attrs={subtitle_type: subtitle_class})
                subtitleText = subtitle.text
            except:
                subtitleText = ''
            main.append({'id': main_id, 'title': titleText, 'subtitle': subtitleText, 'content': contentText})
            # Get the div with the images
            imgdiv = soup.find(imgs_tag, attrs={img_type: imgs_class})
            # Get all the images from the div
            images = imgdiv.find_all('img')
            for image in images:
                try:
                    # If url contains the main url, add to the array
                    if image['src'].find(main_url) != -1:
                        # If the image is already in images_urls, don't add it
                        if image['src'] not in images_urls:
                            images_urls.append({"id": main_id, 'url': image['src'], 'title': title.text})
                    else:
                        # If the image is already in images_urls, don't add it
                        if main_url+image['src'] not in images_urls:
                            images_urls.append({"id": main_id, 'url': main_url+image['src'], 'title': title.text})
                except:
                    pass
            main_id += 1
        except:
            pass

    # Save titles and content in a json file
    with open(save_path+'output.json', 'w', encoding='utf-8') as f:
        json.dump(main, f, ensure_ascii=False, indent=4)

    # Download all the images
    n=0
    placeholder_id = 0
    for image in images_urls:
        url = image['url']
        try:
            idf = image['id']
            if idf != placeholder_id:
                n=0
                placeholder_id = idf
            urllib.request.urlretrieve(url, save_path+"img_"+str(idf)+"_"+str(n)+'.jpg')
            n+=1
        except:
            pass