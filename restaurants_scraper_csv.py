# This script scraping restaurants data for Bonn city from Tripadvisor website

import requests, csv, re, base64
from bs4 import BeautifulSoup

# website that we want to scrape restaurants data from it
website_url = 'https://www.tripadvisor.de'

# pages list that contain pagination pages that evert page contain 30 restauratns pages
# first item is the first page in pagination that not contain pagination number
pages_list = ['https://www.tripadvisor.de/Restaurants-g187370-Bonn_North_Rhine_Westphalia.html']

# this is tow part that represent pagination url 
# after 'oa' come number that represents pagination number
url1 = 'https://www.tripadvisor.de/RestaurantSearch-g187370-oa'
url2 = '-Bonn_North_Rhine_Westphalia.html'

# the results for search in Bonn city is 18 pages, every page contain 30 restauratns pages
counter = 18
pagination_number = 30

# loop 17 times to form paginations pages URLs and put them in pages list
for i in range(1,counter):
    link = url1+str(pagination_number)+url2
    pagination_number = pagination_number + 30
    if link not in pages_list:
        pages_list.append(link)
    link = ''

# the website dose not respond to normal requests , so add headers to response to the request
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

# restaurants pages list that contain URLs for every restaurant page in the website fot Bonn city
restaurants_pages = []

# loop over pages list to extract every restaurant page in the website fot Bonn city
for page_url in pages_list:
    response = requests.get(page_url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', {"class": "aWhIG _S ygNMs Vt u Gi"}):
        if link not in restaurants_pages:
            restaurants_pages.append(link.get('href'))

restaurants_pages_url = []
for page in restaurants_pages:
        full_page_link = website_url + page
        restaurants_pages_url.append(full_page_link)


# CSV file to save restaurants data in it
csv_file = open('restaurants_data.csv', 'a',encoding='UTF8', newline='')
writer = csv.writer(csv_file)
# write header row 
writer.writerow(['Name','Food Types','Address','Phone','Email','Website','Menu'])

counter = 1
for page_url in restaurants_pages_url:
    response = requests.get(page_url,headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        restaurant_name = soup.find('h1', {"class": "HjBfq"}).string

        food_types_in_tags = soup.find_all('a', {"class": "dlMOJ"})
        food_types_list = []
        food_types = ''
        if food_types_in_tags:
            food_types_in_tags.pop(0)
            for food_type in food_types_in_tags:
                food_types_list.append(food_type.string)
        food_types = ','.join(food_types_list)

        restaurant_address = soup.find('a', {"href": "#MAPVIEW"}).string

        r_phone = soup.find_all('a', {"class": "BMQDV _F G- wSSLS SwZTJ"})
        restaurant_phone = ''
        if len(r_phone) > 0:
            restaurant_phone = soup.find_all('a', {"class": "BMQDV _F G- wSSLS SwZTJ"})[1].string

        restaurant_website_menu = soup.find_all('a', {"class": "YnKZo Ci Wc _S C AYHFM"})
        restaurant_website = ''
        restaurant_menu = ''
        if restaurant_website_menu:
            res_website_menu = []
            for link in restaurant_website_menu:
                data_encoded_url = link.get('data-encoded-url')
                link_url = base64.b64decode(data_encoded_url).decode('utf-8')[4:-4]
                res_website_menu.append(link_url)
            if res_website_menu:
                restaurant_website = res_website_menu[0] 
                if len(res_website_menu)>1:
                    restaurant_menu = res_website_menu[1]

        restaurant_email = ''
        restaurant_email_tag = soup.find('a', {"href": re.compile('mailto:')})
        if restaurant_email_tag:
            restaurant_email = restaurant_email_tag.get('href')[7:][:-10]
            
        row = [restaurant_name,food_types,restaurant_address,restaurant_phone,restaurant_email,restaurant_website,restaurant_menu]
        writer.writerow(row)
 
        restaurant_name = ''
        food_types = ''
        restaurant_address = ''
        restaurant_phone = ''
        restaurant_website = ''
        restaurant_menu = ''
        restaurant_email = ''
            
        
        print(str(counter)+':'+'#'*100)
        print(row)
        counter = counter+1
        
csv_file.close()