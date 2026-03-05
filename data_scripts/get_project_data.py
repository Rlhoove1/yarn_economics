import requests
import json
import pandas as pd

url = "https://api.ravelry.com/projects/search.json"
# use ur acess key, define in console so it doenst end up on github 
uid, pw = "read-9add40de0449b103573f7fc8b71c002d", "AmETw80XYOTeWthpmGBbcmSqjCcVHwnq3dvvkVYi"



url = "https://api.ravelry.com/projects/search.json"
uid, pw = "read-9add40de0449b103573f7fc8b71c002d", "AmETw80XYOTeWthpmGBbcmSqjCcVHwnq3dvvkVYi"

# initialize dataframe and starting page
df = pd.DataFrame()   
n = 1

while True:
    response = requests.get(
        url,
        auth=(uid, pw),
        params={"page": n, "page_size": 500}
    )

    responselist = json.loads(response.text)

    # stop if no projects returned
    if len(responselist['projects']) == 0:
        break

    tmp = pd.json_normalize(responselist['projects'])

    df = pd.concat([df, tmp], ignore_index=True)

    # proof of life
    if n % 10 == 0:
        print(f"Page {n} collected, rows so far: {len(df)}")
    if n == 20:
        break
    n += 1


df.to_csv("full_project_data.csv", index=False)

#work in progress for how exactly to get *all* the project data on raverly with out the site freaking out 
