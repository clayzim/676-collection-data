import requests
import json
import csv

def get_collection_list(url):
    response = requests.get(url, params={"fo": "json"})
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError("Didn't get an HTTP OK")

def download_collection_json(url, outfile):
    items_json = get_collection_list(url)
    items = json.loads(items_json)
    with open(outfile, mode='w', encoding="utf-8") as file:
        output = json.dumps(items["content"], sort_keys = True, indent = 4)
        file.write(output)

def create_csv_list_from_json(infile, outfile):
    with open(infile, mode='r', encoding="utf-8") as response:
        content = json.load(response)

    items = content["set"]["items"]

    with open(outfile, mode='w', encoding="utf-8") as csv_file:
        output = csv.writer(csv_file)

        output.writerow(["image", "link", "title"])
        for item in items:
            image = item["image"] if "image" in item else "NO_IMAGE"
            link = item["link"] if "link" in item else "NO_LINK"
            title = item["title"] if "title" in item else "NO_TITLE"
            output.writerow([image, link, title])

def extract_libraries_list():
    libraries_url = "https://www.loc.gov/free-to-use/libraries/"
    json_filename = "./ftu-libraries-set-info.json"
    csv_filename = "./ftu-libraries-set-list.csv"
    download_collection_json(libraries_url, json_filename)
    create_csv_list_from_json(json_filename, csv_filename)

extract_libraries_list()