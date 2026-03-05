import requests
import json
import pandas as pd
import time



url = "https://api.ravelry.com/projects/search.json"
# use ur acess key, define in console so it doenst end up on github 


# initialize dataframe and starting page
frames = []
n = 1

n = 1
frames = []
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

        # check for empty or bad response
        if response.status_code != 200 or not response.text.strip():
            print(f"Warning: empty or bad response at page {n}, retrying in {retry_delay}s")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 300)
            continue

        # parse JSON safely
        try:
            responselist = response.json()
        except json.JSONDecodeError:
            print(f"Warning: JSON decode error at page {n}, retrying in {retry_delay}s")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 300)
            continue

        # stop if no projects returned
        if len(responselist.get("projects", [])) == 0:
            print(f"No projects returned at page {n}, stopping.")
            break

        tmp = pd.json_normalize(responselist["projects"])
        if not tmp.empty:
            frames.append(tmp)

        # proof of life
        if n % 5 == 0:
            print(f"Page {n} collected, total rows: {sum(len(f) for f in frames)}")

        n += 1
        retry_delay = 5  # reset retry delay after success
        time.sleep(0.5)  # polite delay

        if n == 100:  # optional stop
            break

    except requests.exceptions.RequestException as e:
        print(f"Connection error at page {n}: {e}, retrying in {retry_delay}s")
        time.sleep(retry_delay)
        retry_delay = min(retry_delay * 2, 300)

end = time.time()
print("runtime:", end - start)
df = pd.concat(frames, ignore_index=True)
df.to_csv("project_data.csv", index=False)

#work in progress for how exactly to get *all* the project data on raverly with out the site freaking out 
