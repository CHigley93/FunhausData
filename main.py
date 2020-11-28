import requests
import pandas as pd
import json
import matplotlib.pyplot as plt


def auth():
    return "Bearer token goes here"


def create_url(names):
    usernames = "usernames=" + names
    user_fields = "user.fields=description,created_at,public_metrics,username"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


funhaus_list = ["FunHausTeam", "ElyseWillems", "JamesWillems", "SirLarr", "brucegreene", "jonsmiff", "charalanahzard"]
formatted_list = []
bearer_token = auth()
for name in funhaus_list:
    url = create_url(name)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    formatted_list.append([json_response.get("data")[0].get("name"),
                           json_response.get("data")[0].get("public_metrics").get("followers_count"),
                           json_response.get("data")[0].get("public_metrics").get("tweet_count")])

data = pd.DataFrame(formatted_list)
plt.figure()
# data.columns = ["Name", "Followers", "Tweets"]
# data.to_csv("Funhaus Twitter Data.csv", index=False)
