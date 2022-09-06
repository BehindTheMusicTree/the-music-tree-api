import requests
import string
import json

def scrap ():
    url = 'https://myfreemp3juices.cc/api/search.php?callback=jQuery21307552220673040206_1662375436837' + 'search.json?page={}&page_size={}&search_term=a'
  
    # data to be sent to api
    data = {
        'q':'Jul',
        'page':'0'
    }
    
    # sending post request and saving response as response object
    responseText = requests.post(url = url, data = data).text
    songsJsonText = "{" + responseText.split("{",2)[2]
    songsJsonText = songsJsonText[:len(songsJsonText) - 4]
    caca = "caca"
    caca = caca[:len(caca) - 2]
    print("caca: " + caca) # json.dumps(json.loads(r.text), indent=4))
    print("Response: " + songsJsonText) # json.dumps(json.loads(r.text), indent=4))
    # print("Response: " + responseText) # json.dumps(json.loads(r.text), indent=4))

    return json.loads(songsJsonText)