import requests
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np


def auth():
    return os.environ.get("bearer_token")


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
formatted_list_as_array = np.array(formatted_list)
# print(formatted_list_as_array)
data = pd.DataFrame(formatted_list,index=formatted_list_as_array[:,0])
data.columns = ["Name", "Number of Followers", "Number of Tweets"]
plt.figure()
data.plot(kind="bar", sort_columns=True)
plt.show()
# data.columns = ["Name", "Followers", "Tweets"]
# data.to_csv("Funhaus Twitter Data.csv", index=False)
