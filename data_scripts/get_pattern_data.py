import requests
import json
import pandas as pd
url = "https://api.ravelry.com/patterns/search.json"
uid, pw = "", ""
response = requests.get(url, auth=(uid, pw),params={"page": 2, "page_size": 100} )
responselist = json.loads(response.text)
df = pd.json_normalize(responselist['patterns'])
df
