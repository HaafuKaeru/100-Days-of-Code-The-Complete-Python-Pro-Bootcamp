import requests
from datetime import datetime


USERNAME = "haafukaeru"
TOKEN = "haafukaerutoken"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# create the user
# rsp = requests.post(url=pixela_endpoint, json=user_params)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": "graph1",
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "ajisai",
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# create a graph
# rsp = requests.post(url=graph_endpoint, json=graph_config, headers=headers)

cycling_graph_endpoint = f"{graph_endpoint}/{graph_config['id']}"

today = datetime.now()
print(today)

entry = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "34"
}

# add a new entry
# rsp = requests.post(url=cycling_graph_endpoint, json=entry, headers=headers)

yesterday = datetime(year=2026, month=6, day=18)

update_params = {
    "quantity": "453",
}

# update an existing entry
# rsp = requests.put(url=cycling_graph_endpoint+f"/{yesterday.strftime('%Y%m%d')}", json=update_params, headers=headers)


# delete an exisitng entry
rsp = requests.delete(url=cycling_graph_endpoint+f"/{yesterday.strftime('%Y%m%d')}", headers=headers)
print(rsp.text)