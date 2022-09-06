import requests
import string

def scrap ():
    url = 'https://myfreemp3juices.cc/api/search.php?callback=jQuery21307552220673040206_1662375436837' + 'search.json?page={}&page_size={}&search_term=a'
  
    # data to be sent to api
    data = {
        'q':'Jul',
        'page':'0'
    }
    
    # sending post request and saving response as response object
    r = requests.post(url = url, data = data)
    
    # extracting response text 
    pastebin_url = r.text
    print("The pastebin URL is:%s"%pastebin_url)

    return r.text