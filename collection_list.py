import requests
import json

def get_collection_list(url):
    response = requests.get(url, params={"fo": "json"})
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError("Didn't get an HTTP OK")

def download_libraries_json():
    libraries = "https://www.loc.gov/free-to-use/libraries/"
    items_json = get_collection_list(libraries)
    items = json.loads(items_json)
    with open("./response.json", mode='w', encoding="utf-8") as file:
        output = json.dumps(items["content"], sort_keys = True, indent = 4)
        file.write(output)

