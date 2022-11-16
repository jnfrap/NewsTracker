import requests, urllib.request, json, os, shutil, traceback, ssl
from bs4 import BeautifulSoup

def getNews(main_url, url, news_tag, news_type, news_class, news_content_tag, news_content_type, news_content_class, imgs_tag, img_type, imgs_class, title_tag, title_type, title_class, subtitle_tag, subtitle_type, subtitle_class, directory):
    #Relative path
    dirname = os.path.dirname(__file__)
    # Save patch
    save_path = dirname+'/output/'+directory+'/'
    # Create output folder if not exists
    if not os.path.exists(os.path.join(dirname, 'output')):
        os.makedirs(os.path.join(dirname, 'output'), exist_ok=True)

    # Create the folder to save the news if not exists
    os.makedirs(os.path.join(dirname+'/output', directory), exist_ok=True)

    # Delete all files in dirname+'\\output\\'+directory+'\\'
    """for filename in os.listdir(dirname+'/output/'+directory+'/'):
        file_path = os.path.join(dirname+'/output/'+directory+'/', filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))"""

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

    # If output.json exists, get all the titles from the file and store it in an array
    titlesInJson = []
    if os.path.exists(save_path+'output.json'):
        with open(save_path+'output.json') as json_file:
            data = json.load(json_file)
            for d in data:
                titlesInJson.append(d['title'])

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
            # Check if the title is in the json file
            if titlesInJson.count(titleText) == 0:
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
                # If contentText contains the title or the subtitle, remove it
                if contentText.find(titleText) != -1:
                    contentText = contentText.replace(titleText, '')
                if contentText.find(subtitleText) != -1:
                    contentText = contentText.replace(subtitleText, '')
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

    # Get the number of news in main
    news_number = len(main)

    # If the json file has content, reassign the id and add the new news
    phId = -1
    if os.path.exists(save_path+'output.json'):
        print('File exists')
        with open(save_path+'output.json') as json_file:
            data = json.load(json_file)
            for d in data:
                d['id'] = phId
                phId -= 1
            phId = 0
            for d in data:
                main.append(d)
            for m in main:
                m['id'] = phId
                phId += 1
    
    imgNewsCount = news_number

    # Change the images name and save it in the folder
    for filename in os.listdir(save_path):
        if filename.endswith(".jpg"):
            # Get the id of the image, is the first number of the name
            id = int(filename.split('_')[1])
            id = id+imgNewsCount
            # Rename the image
            os.rename(save_path+filename, save_path+filename.split('_')[0]+'_'+str(id)+'_'+filename.split('_')[2])

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
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(url, save_path+"img_"+str(idf)+"_"+str(n)+'.jpg')
            n+=1
        except:
            traceback.print_exc()
            pass