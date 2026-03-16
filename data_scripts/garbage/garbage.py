import requests
import json
import pandas as pd
import time


# there are 32,016,181 entires as of mar 5 and naturally i want them all

uid, pw = "read-0ea4f9f35434b031dbcf2acbe301c226", "tlSskeRXLNybZBFYzE2gZaAL7K2Fh/eXPnLuHly9"
url = "https://api.ravelry.com/projects/search.json"
# use ur acess key, define in console so it doenst end up on github 


# initialize

n = 1
retry_delay = 5
start = time.time()

while True:
    try:
        response = requests.get(
            url,
            auth=(uid, pw),
            params={"page": n, "page_size": 500},
            timeout=30
        )

        # check for bad response and time delay (cap at 5 min) to try again
        if response.status_code != 200:
            print(f"Warning: empty or bad response at page {n}, retrying in {retry_delay}s")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 300)
            continue

        # catch api giving an empty json error
        try:
            responselist = json.loads(response.text)
        except json.JSONDecodeError:
            print(f"Warning: JSON decode error at page {n}, retrying in {retry_delay}s")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 300)
            continue

  
        df = pd.json_normalize(responselist['projects'])
        # append to CSV incrementally
        df.to_csv("project_data_test.csv", mode="a", index=False)


        # proof of life
        if n % 50 == 0:
            print(f"Page {n} collected, total rows:")

        n += 1
        #reset retry delay after success 
        retry_delay = 5 

        #delay to be "polite"
        time.sleep(0.5) 

        if n == 20:
            break

    except requests.exceptions.RequestException as e:
        print(f"Connection error at page {n}: {e}, retrying in {retry_delay}s")
        time.sleep(retry_delay)
        retry_delay = min(retry_delay * 2, 300)

end = time.time()
print("runtime:", end - start)
#df = pd.concat(frames, ignore_index=True)
#df.to_csv("project_data.csv", index=False)

#work in progress for how exactly to get *all* the project data on raverly with out the site freaking out 
