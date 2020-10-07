from django.shortcuts import render
import requests
import xmltodict
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.request
# Create your views here.

def get_book_details(book_url):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'{ book_url }').text
    return html_content

def home(request):
    if request.method=='POST':
        return render(request,'core/home.html')
    else:
        try:
            book_information = None
            #if 'links' in request.GET:
            #if request.method == 'GET':
            book_url = request.GET.get('links')
            #url= "https://www.goodreads.com/shelf/show/thriller"
            html_content = get_book_details(book_url)
            soup = BeautifulSoup(html_content, 'html.parser')
            #soup.get_text()
            book_information =dict()
            class InvalidGoodreadsURL(Exception):
                def __init__(self, page_title, message="Page not found"):
                        self.page_title = page_title
                        self.message = message
                        super().__init__(self.message)
                def __str__(self):
                    return f'{self.page_title} -> {self.message}'
            page_title=soup.find('title').text
            #print(page_title)
            if "Page not found" in page_title:
                print ("Yes, String found")
                raise InvalidGoodreadsURL(page_title)
                return render(request,'core/home.html',{'error':'broken url'})
            else:
                book_information['title'] = (soup.find('h1',attrs={'id':'bookTitle'}).text).strip()
                book_information['average_rating'] = float((soup.find('span', attrs={'itemprop':'ratingValue'}).text).strip())
                floor=[]
                for item in soup.findAll('div', attrs={'id':'bookMeta'}):
                    floor.append(item.text)
                    #print(floor)
                ratings_cnt=' '.join(map(str, floor))
                ratings_count1=ratings_cnt.strip()
                book_information['ratings_count']=ratings_count1[7:55].strip()
                total_pages = soup.find('span', attrs={'itemprop':'numberOfPages'}).text
                no_of_pages=''
                for i in range(0,len(total_pages),1):
                    if total_pages[i]!=' ':
                        no_of_pages+=total_pages[i]
                    else:
                        break
                book_information['num_pages']=int(no_of_pages)
                link = soup.find('img',attrs={'id':"coverImage"})
                book_information['image_url'] = link["src"]
                pb_year = soup.find_all('nobr',attrs={'class':"greyText"})
                tring=(str(pb_year[0].get_text())).replace(' ','')
                book_information['publication_year']=tring[-6:-2]
                #author_name=soup.find('span',attrs={'itemprop':'name'}).text
                authors_name=[]
                for item in soup.findAll('span', attrs={'itemprop':'name'}):
                    authors_name.append(item.text)
                book_information['authors']=', '.join(map(str, authors_name))
                #print(title.strip())
                #print(float(average_rating.strip()))
                #print(ratings_count1[7:55].strip())
                #print(int(no_of_pages))
                #print(link["src"])
                #print(tring[-6:-2])
                #print(authors)
                print(book_information)
            return render(request,'core/home.html',{'book_INFO':book_information})
        except ValueError:
            return render(request,'core/home.html')

def gdapi(request):
    if request.method=='POST':
        return render(request,'core/home.html')
    else:
        try:

            book_id = request.GET.get('book_id','')
            dev_key = request.GET.get('dev_key','')
            res1='https://www.goodreads.com/book/show/{}.xml?key={}'.format(book_id,dev_key)
            print(res1)
            r = urllib.request.urlopen('https://pythonprogramming.net/sitemap.xml').read()
            soup = BeautifulSoup(r, 'xml')
            tree = ET.parse(r.text)
            root = tree.getroot()
            print(soup.h2)
            return render(request,'core/gdapi.html')

        except ValueError:
            return render(request,'core/gdapi.html')