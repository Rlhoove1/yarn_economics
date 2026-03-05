import requests
import json
import pandas as pd
import time



url = "https://api.ravelry.com/projects/search.json"
# use ur acess key, define in console so it doenst end up on github 


# initialize dataframe and starting page
frames = []
n = 1
start = time.time()

while True:
    try:
        response = requests.get(url, auth=(uid, pw),params={"page": n, "page_size": 500}, timeout=30 )       
        
        # reset if success
        retry_delay = 5 

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        print(f"Retrying in {retry_delay} seconds")

        # increase wait time after a failure, capped at 5 mins
        time.sleep(retry_delay)
        retry_delay = min(retry_delay * 2, 300) 

    responselist = json.loads(response.text)

    # stop if no projects returned
    if len(responselist['projects']) == 0:
        break

    tmp = pd.json_normalize(responselist['projects'])

    if not tmp.empty:
        frames.append(tmp)
    
    # proof of life
    if n % 5 == 0:
        print(f"Page {n} collected")
    if n == 100:
        break
    n += 1

end = time.time()
print("runtime:", end - start)
df = pd.concat(frames, ignore_index=True)
df.to_csv("project_data.csv", index=False)

#work in progress for how exactly to get *all* the project data on raverly with out the site freaking out 
