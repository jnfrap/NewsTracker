import os, json, threading, time, datetime
from NewsTracker.Misc.Tracker import getNews

# If not exists, create the file Misc/NewsSites.json in blanck
dirname = os.path.dirname(__file__)+"/Misc/"
if not os.path.exists(os.path.join(dirname, 'newsSites.json')):
    with open(os.path.join(dirname, 'newsSites.json'), 'w') as f:
        f.write("[]")

# Get the json array from the file
with open(os.path.join(dirname, 'newsSites.json'), 'r') as f:
    sites = json.load(f)

# Get all parameters for each site on the json file
sitesFormated = []
for site in sites:
    mainUrl = site['mainUrl']
    newsUrl = site['newsUrl']
    newsTag = site['newsTag']
    newsType = site['newsType']
    newsClass = site['newsClass']
    titleTag = site['titleTag']
    titleType = site['titleType']
    titleClass = site['titleClass']
    subtitleTag = site['subtitleTag']
    subtitleType = site['subtitleType']
    subtitleClass = site['subtitleClass']
    contentTag = site['contentTag']
    contentType = site['contentType']
    contentClass = site['contentClass']
    imgsTag = site['imgsTag']
    imgsType = site['imgsType']
    imgsClass = site['imgsClass']
    directory = site['directory']
    schedule = site['schedule']
    activate = site['activate']
    id = site['id']

    # Create a boolean variable and set it to True if activate is 'on'
    if activate == 'on':
        activate = True
    else:
        activate = False

    # Convert id to int
    id = int(id)

    # Save all parameters in sitesFormated
    sitesFormated.append([mainUrl, newsUrl, newsTag, newsType, newsClass, contentTag, contentType, contentClass, imgsTag, imgsType, imgsClass, titleTag, titleType, titleClass, subtitleTag, subtitleType, subtitleClass, directory, schedule, activate, id])



    
# Thread
def run_test():
    while True: # Loop forever
        for site in sitesFormated:
            # If the site is activated
            if site[19]:
                # Get actual hour and minute
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute

                # Get the hour and minute from the schedule
                schedule = site[18]
                schedule = schedule.split(':')
                scheduleHour = int(schedule[0])
                scheduleMinute = int(schedule[1])

                # If actual hour and minute are less then the schedule hour and minute
                if hour < scheduleHour or (hour == scheduleHour and minute < scheduleMinute):
                    getNews(site[0], site[1], site[2], site[3], site[4], site[5], site[6], site[7], site[8], site[9], site[10], site[11], site[12], site[13], site[14], site[15], site[16], site[17])

        # Wait 10 minutes
        time.sleep(600)

thread = threading.Thread(target=run_test)
thread.start()