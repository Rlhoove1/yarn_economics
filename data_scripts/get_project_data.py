import requests
import json
import pandas as pd
import time



url = "https://api.ravelry.com/projects/search.json"
# use ur acess key, define in console so it doenst end up on github 
uid, pw = "read-9add40de0449b103573f7fc8b71c002d", "AmETw80XYOTeWthpmGBbcmSqjCcVHwnq3dvvkVYi"

# initialize dataframe and starting page
response = requests.get(url, auth=(uid, pw),params={ "page": 1, "page_size": 500} )
responselist = json.loads(response.text)
#print(response.text)url = "https://api.ravelry.com/projects/search.json"
df = pd.json_normalize(responselist["projects"])

n = 2
start = time.time()

while True:
    try:
        response = requests.get(
            url,
            auth=(uid, pw),
            params={"page": n, "page_size": 500},
            timeout=(3, 10)
        )
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)
        time.sleep(30)
        continue

    responselist = json.loads(response.text)

    # stop if no projects returned
    if len(responselist['projects']) == 0:
        break

    tmp = pd.json_normalize(responselist['projects'])
   
    if df.empty:
        df = tmp
    else:
        df = pd.concat([df, tmp], ignore_index=True)
    # proof of life
    if n % 10 == 0:
        print(f"Page {n} collected, rows so far: {len(df)}")
    if n == 100:
        break
    n += 1

end = time.time()
print("runtime:", end - start)

df.to_csv("project_data.csv", index=False)

#work in progress for how exactly to get *all* the project data on raverly with out the site freaking out 
