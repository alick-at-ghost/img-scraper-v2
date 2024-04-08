import json
import re
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup


# checks whether URL is image
def is_url_image(image_url):
    try:
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        if r.headers["content-type"] in image_formats:
            return True
    except:
        print("An exception occurred")


# takes a JS script object and parses for the first relevant URL.
def parse_urls(script):
    #split initial html output
    output_script = str(script).split('var m=')[1].split(';var a=m;')[0]
    # look for key to split off of
    output_json = json.loads(output_script)

    image_search_keys = list(output_json.keys())
    for i in image_search_keys:
        parsed_javascript = output_script.split(i)[1]
        urls = re.findall(r'(https?://[^\s]+)', parsed_javascript)[0]
        final_url = re.findall(r'\[(.*?)\]', urls)[0].split('"')[1]
        if is_url_image(final_url):
            print(final_url)
        continue
    
url = 'https://www.google.com/search?q=fear+of+god+sweat+pants+black&udm=2'

# load page
asession = AsyncHTMLSession()
response = await asession.get(url)
await response.html.arender()
resp=response.html.raw_html

# initialize BS
soup = BeautifulSoup(resp, 'html.parser')
# find all scripts
scripts = soup.find_all('script')

final_url = ''
for script in scripts:
    if 'function(){google.kEXPI=' in str(script):
        final_url = parse_urls(script)
    

print(final_url)
