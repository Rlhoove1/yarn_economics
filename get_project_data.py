import requests
import json
import pandas as pd

url = "https://api.ravelry.com/projects/search.json"
# use ur acess key 
uid, pw = "", ""
response = requests.get(url, auth=(uid, pw),params={"page": 1, "page_size": 500} )
responselist = json.loads(response.text)
df = pd.json_normalize(responselist['projects'])
df

#work in progress for how exactly to get *all* the project data on raverly with out the site freaking out 
