import requests, time
from bs4 import BeautifulSoup
from selenium import webdriver

# INFO: > Paste the list url in Constants
#       > install: python3.10 -m pip install requests==2.27.1 selenium==4.1.3 bs4==0.0.1 
#       > run:     python3.10 scrap_senscritique.py
#       > read:    top_<list_name>.csv    

# Constants
debug = False
scroll_delay = 0.5
url = "https://www.senscritique.com/films/tops/top111"

# Selenium
user_agent = "Mozilla/5.0"
service = webdriver.chrome.service.Service('./chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
print(driver.title)
pages=[]
last_height = driver.execute_script("return document.body.scrollHeight") # Get scroll height
while True:
    pages.append(driver.page_source)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to bottom
    time.sleep(scroll_delay) # Wait to load page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
try:
    list_ = url.split('/resultats/')[1].split('/')[0]
except:
    print("Couldn't parse the list name, Please give a list name:")
    list_ = input("> ")
films = {}
with open(f"top_film_{list_}.csv","w") as output:
    page = pages[-1] #
    soup = BeautifulSoup(page, 'html.parser')
    for div in soup.find_all("div"):
        try:
            title = div.find('a').get('href')
        except Exception as e:
            title = ""
            if debug: print(">>>>>>>> div:", div, e)
        if '/film/' in title:
            film_url = "https://www.senscritique.com" + title
            film_name = title.replace('/film/','').split('/')[0]
            if film_name not in films:
                print(f"Processing: {film_name}")
                films[film_name]={'url':film_url,'directorName':'','genre':'','duration':'','datetime':'',
                                  'ratingValue':'','ratingCount':'','reviewCount':'','notes':'','love':'',
                                  'wanted':'','resume':''}
            url = film_url
            headers = {'User-Agent': user_agent}
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            tracks = []
            for section in soup.find_all("section", {"class": "pvi-productDetails"}):
                for ul in section.find_all('ul'):
                    for li in ul.find_all("li", {"class": "pvi-productDetails-item"}):
                        genre=""
                        for span in li.find_all('span'):
                            if span.get('itemprop') == 'name':
                                directorName = span.getText()
                                films[film_name].update({"directorName": directorName})
                            if span.get('itemprop') == 'genre':
                                genre = genre + span.getText() + ", "       
                        if len(genre) > 2: 
                            genre = genre[:-2]
                            films[film_name].update({"genre": genre})
                        for meta in li.find_all('meta'):
                            if meta.get('itemprop') == 'duration':
                                duration = li.getText().strip(' \n\t\r')
                                films[film_name].update({"duration": duration})
                        for time in li.find_all('time'):
                            datetime=time.get('datetime')
                            films[film_name].update({"datetime": datetime})
                for p in section.find_all('p', {"class": "pvi-productDetails-resume"}):
                    resume = p.getText().replace("Lire la suite","").strip(' \n\t\r')
                    if len(resume) > 20:
                        films[film_name].update({"resume": resume})    
            for div2 in soup.find_all("div", {"class": "pvi-product-scrating"}):
                for tag in div2.find_all('span'):
                    ratingValue = "n/a"
                    if tag.get('itemprop') == 'ratingValue':
                        ratingValue = tag.getText()
                        films[film_name].update({"ratingValue": ratingValue})
                for tag in div2.find_all('meta'):
                    ratingCount = "n/a"
                    reviewCount = "n/a"
                    if tag.get('itemprop') == 'ratingCount':
                        ratingCount = tag.get('content')
                        films[film_name].update({"ratingCount": ratingCount})
                    if tag.get('itemprop') == 'reviewCount':
                        reviewCount = tag.get('content')
                        films[film_name].update({"reviewCount": reviewCount})
                    details = tag.find('ul',{"class": "pvi-scrating-details"})
                    li_list=[]
                    notes = "n/a"
                    love = "n/a"
                    wanted = "n/a"
                    try:
                        for li in details.find_all('li'):
                            li_val = li.find('b',{"class": "pvi-stats-number"}).get_text()
                            li_list.append(li_val)
                    except Exception as e:
                        if debug: print(">>>>>>>> li_list:", details, e)
                    
                    if len(li_list)==3:
                        notes = li_list[0]
                        love = li_list[1]
                        wanted = li_list[2]
                        films[film_name].update({"notes": notes,
                                                 "love": love,
                                                 "wanted": wanted})
    if debug: print(films) 
    for film_name, v in films.items():
        output.write(
            f"{film_name}|"
            f"{v['directorName']}|"
            f"{v['genre']}|"
            f"{v['datetime']}|"
            f"{v['duration']}|"
            f"{v['ratingValue']}|"
            f"{v['ratingCount']}|"
            f"{v['reviewCount']}|"
            f"{v['notes']}|"
            f"{v['love']}|"
            f"{v['wanted']}|"
            f"{v['resume']}\n")